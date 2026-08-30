import os
import plistlib
import zipfile

from config import IPA_DOWNLOAD_DIR


def find_url_scheme(filename):
    path = IPA_DOWNLOAD_DIR + filename
    if ".ipa" not in filename:
        path += ".ipa"
    try:
        with zipfile.ZipFile(path) as zf:
            plist_name = next(
                name
                for name in zf.namelist()
                if name.lower().endswith("/info.plist")
                and name.split("/")[0] == "Payload"
                and name.split("/")[1].endswith(".app")
            )
            plist_file = plistlib.load(zf.open(plist_name))
        result = []
        display_name = ""
        if "CFBundleDisplayName" in plist_file:
            display_name += plist_file["CFBundleDisplayName"] + " "
        if "CFBundleName" in plist_file:
            display_name += plist_file["CFBundleName"]
        if "CFBundleURLTypes" in plist_file:
            for urlscheme in plist_file["CFBundleURLTypes"]:
                if "CFBundleURLSchemes" in urlscheme:
                    result += urlscheme["CFBundleURLSchemes"]
        return display_name.strip(), result
    except (StopIteration, zipfile.BadZipFile, plistlib.InvalidFileException, FileNotFoundError) as e:
        print(e)
    return "", []


def parse_downloaded_file():
    for filename in os.listdir(IPA_DOWNLOAD_DIR):
        if ".ipa" in filename:
            display_name, result = find_url_scheme(filename)
            print("App Name: " + display_name)
            print("URL Schemes: " + str(result))


if __name__ == "__main__":
    parse_downloaded_file()
