#!/usr/bin/env python3

import argparse
import itertools
import json
import os
import shutil
import subprocess
import sys
import threading

from config import IPA_DOWNLOAD_DIR


def supports_color(stream):
    return stream.isatty() and "NO_COLOR" not in os.environ


def color(text, *codes, stream=sys.stdout):
    if not codes or not supports_color(stream):
        return text
    return "\033[%sm%s\033[0m" % (";".join(str(code) for code in codes), text)


def fail(message, code=1):
    print(color("error:", 1, 31, stream=sys.stderr) + " " + message, file=sys.stderr)
    raise SystemExit(code)


def confirm(prompt, assume_yes):
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        return False
    answer = input(color(prompt + " [Y/n] ", 1, 33)).strip().lower()
    return answer in ("", "y", "yes")


class Spinner:
    def __init__(self, message):
        self.message = message
        self._stop = threading.Event()
        self._thread = None

    def __enter__(self):
        if not sys.stderr.isatty():
            print(self.message, file=sys.stderr)
            return self
        sys.stderr.write("\033[?25l")
        sys.stderr.flush()

        def run():
            for frame in itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
                if self._stop.wait(0.08):
                    break
                sys.stderr.write(
                    "\r\033[K%s %s"
                    % (color(frame, 36, stream=sys.stderr), self.message)
                )
                sys.stderr.flush()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop.set()
        if self._thread is not None:
            self._thread.join()
        if sys.stderr.isatty():
            sys.stderr.write("\r\033[K\033[?25h")
            sys.stderr.flush()


def ipatool_json(*args, allow_fail=False):
    completed = subprocess.run(
        ["ipatool", "--format", "json", *args],
        capture_output=True,
        text=True,
    )
    payload = None
    for line in (completed.stdout + completed.stderr).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
    assert payload is not None, (
        completed.stdout or completed.stderr or "ipatool produced no output"
    )
    if payload.get("success") is False and not allow_fail:
        fail(payload.get("error", "ipatool failed"))
    return payload


def ok(message):
    print(color("✓", 1, 32) + " " + message)


def obfuscate(text):
    def mask(part):
        if len(part) <= 1:
            return part
        if len(part) == 2:
            return part[0] + "*"
        return part[0] + "*" * (len(part) - 2) + part[-1]

    local, sep, domain = text.partition("@")
    return mask(local) + sep + mask(domain)


def search_and_download(term, limit):
    with Spinner("Searching the App Store…"):
        payload = ipatool_json("search", term, "-l", str(limit))
    apps = payload.get("apps") or []
    if not apps:
        print(color("No results for ", 33) + color(term, 1, 33))
        return
    headers = ("#", "Name", "Bundle ID", "Version", "Price")
    rows = []
    for index, app in enumerate(apps, 1):
        price = app.get("price") or 0
        rows.append(
            (
                str(index),
                app.get("name") or "",
                app.get("bundleID") or "",
                app.get("version") or "",
                "Free" if price == 0 else "$%s" % price,
            )
        )
    widths = [
        max(len(headers[column]), max(len(row[column]) for row in rows))
        for column in range(5)
    ]
    columns = shutil.get_terminal_size((80, 24)).columns
    overflow = sum(widths) + 8 - columns
    if overflow > 0:
        widths[1] = max(8, widths[1] - overflow)

    def cell(text, width):
        if len(text) <= width:
            return text.ljust(width)
        if width <= 1:
            return text[:width]
        return (text[: width - 1] + "…").ljust(width)

    print()
    print(
        color(
            "  ".join(headers[i].ljust(widths[i]) for i in range(5)),
            2,
        )
    )
    for row in rows:
        print(
            "  ".join(
                (
                    color(cell(row[0], widths[0]), 1, 36),
                    color(cell(row[1], widths[1]), 1),
                    color(cell(row[2], widths[2]), 2),
                    cell(row[3], widths[3]),
                    color(cell(row[4], widths[4]), 32 if row[4] == "Free" else 33),
                )
            )
        )
    print()
    choice = input(
        color("Select [1-%d] (empty to search again): " % len(apps), 1, 36)
    ).strip()
    if not choice:
        return
    try:
        app = apps[int(choice) - 1]
    except (ValueError, IndexError):
        print(color("Invalid selection.", 31))
        return
    bundle_id = app.get("bundleID")
    assert bundle_id, "missing bundle identifier"
    filename = "%s.ipa" % bundle_id
    output_path = os.path.abspath(os.path.join(IPA_DOWNLOAD_DIR, filename))
    label = "%s %s" % (app.get("name") or bundle_id, app.get("version") or "")
    print()
    print(color("↓", 1, 36) + " Downloading " + color(label.strip(), 1))
    command = [
        "ipatool",
        "download",
        "-b",
        bundle_id,
        "-o",
        output_path,
        "--purchase",
    ]
    try:
        if sys.stdout.isatty():
            subprocess.run(command, check=True)
        else:
            with Spinner("Downloading %s…" % label.strip()):
                subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        fail("download failed (exit %d)" % error.returncode)
    ok("Saved " + color(output_path, 2))
    from parse_ipa import find_url_scheme

    with Spinner("Parsing IPA…"):
        display_name, schemes = find_url_scheme(filename)
    print(color("App Name", 2) + "     " + color(display_name, 1))
    if schemes:
        print(
            color("URL Schemes", 2)
            + "  "
            + ", ".join(color(scheme, 36) for scheme in schemes)
        )
    else:
        print(color("URL Schemes", 2) + "  " + color("none found", 33))
    print()


def main(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Search the App Store, download an IPA to apps/, and parse URL Schemes.",
        epilog="Examples:\n  python3 get.py\n  python3 get.py WeChat\n  python3 get.py -l 20 Telegram",
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="search term; omit to enter interactive mode",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        metavar="N",
        help="maximum search results (default: 10)",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="assume yes for Homebrew/ipatool install prompts",
    )
    args = parser.parse_args(argv)

    if sys.platform != "darwin":
        fail("this tool requires macOS")

    os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get(
        "PATH", ""
    )

    print(color("iOS URL Scheme", 1, 36))
    print()

    if shutil.which("ipatool") is None:
        if shutil.which("brew") is None:
            if not confirm("Homebrew is not installed. Install it now?", args.yes):
                fail("Homebrew is required to install ipatool")
            print(color("Installing Homebrew…", 33))
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True,
                check=True,
            )
            os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get(
                "PATH", ""
            )
            assert shutil.which("brew"), "Homebrew installed but brew was not found in PATH"
            ok("Homebrew installed")
        if not confirm("ipatool is not installed. Install it with Homebrew now?", args.yes):
            fail("ipatool is required")
        print(color("Installing ipatool…", 33))
        subprocess.run(["brew", "install", "ipatool"], check=True)
        assert shutil.which("ipatool"), "ipatool installed but was not found in PATH"
        ok("ipatool installed")

    with Spinner("Checking ipatool…"):
        version = subprocess.run(
            ["ipatool", "--version"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        account = ipatool_json("auth", "info", allow_fail=True)
    ok(version or "ipatool")

    if account.get("success") is not True:
        email = input(color("Apple ID email: ", 1, 36)).strip()
        assert email, "Apple ID email is required"
        subprocess.run(["ipatool", "auth", "login", "-e", email], check=True)
        ok("Signed in as " + obfuscate(email))
    else:
        ok(
            "Signed in as "
            + obfuscate(account.get("email") or account.get("name") or "Apple ID")
        )

    os.makedirs(IPA_DOWNLOAD_DIR, exist_ok=True)
    print()

    if args.query:
        search_and_download(" ".join(args.query), args.limit)
        return 0

    if not sys.stdin.isatty():
        fail("no search term provided (not a TTY)")

    while True:
        term = input(color("Search: ", 1, 36)).strip()
        if not term:
            return 0
        search_and_download(term, args.limit)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        if sys.stderr.isatty():
            sys.stderr.write("\r\033[K\033[?25h")
        print()
        sys.exit(130)
    except EOFError:
        print()
        sys.exit(1)
