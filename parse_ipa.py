import zipfile, os, sys
from config import IPA_UNZIP_DIR
from config import IPA_DOWNLOAD_DIR

import biplist

## 解压缩文件

def unzip(filename):

    zf = zipfile.ZipFile(IPA_DOWNLOAD_DIR + filename + ".ipa")
    try:
        zf.extractall(path=IPA_UNZIP_DIR + filename)
    except RuntimeError as e:
        print(e)
    zf.close()

    print("IPA 文件「" + filename + "」解压完毕")

    return filename

# 寻找 urlscheme

def find_url_scheme(filename):
    plist_path = IPA_UNZIP_DIR+filename+"/Payload/"
    app_file_name = os.listdir(plist_path)[0]
    plist_path += app_file_name
    plist_path += "/info.plist"

    try:
        plist_file = biplist.readPlist(plist_path);

        if "CFBundleURLTypes" in plist_file:
            urls = plist_file["CFBundleURLTypes"]
            for urlscheme in urls:
                if "CFBundleURLSchemes" in urlscheme:
                    print(urlscheme["CFBundleURLSchemes"])
        else:
            print("「" + filename + "」可能未配置 URL Scheme，请手动检查 plist 文件: " )
            print(plist_path)
    except biplist.InvalidPlistException as e:
        print(e)
    return plist_path
