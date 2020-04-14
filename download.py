#! /usr/bin/env python3

import requests
import shutil
import json
from lxml.etree import HTML
from base64 import b64decode
from sys import argv
from config import IPA_DOWNLOAD_DIR
from parse_ipa import unzip, find_url_scheme

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://www.i4.cn/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def download_i4_ipa(url):
    req = requests.get(url)
    sel = HTML(req.content)
    title = sel.xpath('//div[@class="title"]/div[@class="h1"]/text()')[0]
    encoded = sel.xpath('//a[contains(@class, "install")]/@data-download')[0]
    decoded = b64decode(encoded).decode('utf8')
    print("%s: %s" % (title, decoded))
    json_dict = json.loads(decoded)
    download_url = json_dict['path']
    
    resp = requests.get(download_url, headers=headers, stream=True)
    assert(resp.status_code == 200)
    ipa_file_path = IPA_DOWNLOAD_DIR + '%s.ipa' % title
    with open(ipa_file_path, 'wb') as ipa:
        print('下载「%s」IPA 文件中...' % title)
        resp.raw.decode_content=True
        shutil.copyfileobj(resp.raw, ipa)
    print('%s 下载完成' % title)
    
    return title

def main():
    apps = argv[1:]
    for app in apps:
        ipa_filename = download_i4_ipa(app)
        unzip(ipa_filename)
        find_url_scheme(ipa_filename)

if __name__ == '__main__':
    main()

