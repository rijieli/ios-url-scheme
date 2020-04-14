import zipfile, os, sys
from config import IPA_UNZIP_DIR
from config import IPA_DOWNLOAD_DIR

import biplist

## 解压缩文件

def unzip(filename):

    ziped_file = IPA_DOWNLOAD_DIR + filename

    if "\.ipa" in filename:
        ziped_file += ".ipa"
    
    try:
        zf = zipfile.ZipFile(ziped_file)
        zf.extractall(path=IPA_UNZIP_DIR + filename)
        zf.close()
    except RuntimeError as e:
        print(e)
    except zipfile.BadZipFile as bzfe:
        print("!!!! 解压失败 BadZipFile 错误: " + str(filename))
        
    return filename

# 寻找 urlscheme

def find_url_scheme(filename):

    try:
        plist_path = IPA_UNZIP_DIR+filename+"/Payload/"
        app_file_name = os.listdir(plist_path)[0]
        plist_path += app_file_name
        plist_path += "/info.plist"
        plist_file = biplist.readPlist(plist_path);

        result = []

        display_name = ""

        if "CFBundleDisplayName" in plist_file:
            display_name += plist_file["CFBundleDisplayName"] + " "
        if "CFBundleName" in plist_file:
            display_name += plist_file["CFBundleName"]

        print("App Name: " + display_name)

        if "CFBundleURLTypes" in plist_file:
            urls = plist_file["CFBundleURLTypes"]
            for urlscheme in urls:
                if "CFBundleURLSchemes" in urlscheme:
                    result += urlscheme["CFBundleURLSchemes"]
        else:
            print("「" + filename + "」可能未配置 URL Scheme，请手动检查 plist 文件: " )
            print(plist_path)
        
        print("URL Schemes: " + str(result))
    except biplist.InvalidPlistException as e:
        print(e)
    except FileNotFoundError as nfe:
        print(nfe)
    return plist_path

def parse_downloaded_file():
    file_name_list = os.listdir(IPA_DOWNLOAD_DIR)
    for filename in file_name_list:
        if "ipa" in filename:
            unzip(filename)
            find_url_scheme(filename)


parse_downloaded_file()