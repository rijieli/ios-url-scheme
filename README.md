# iOS URL Scheme 解析

## 安装依赖

```
$ pip3 install -r requirements.txt
```

## 使用方式
### 通过 iMazing 或者老版 iTunes 下载 IPA
将 IPA 文件放在 ipa_file 目录下，然后运行
```
$ python3 parse_ipa.py
App Name: 网易公开课 OpenCourse
URL Schemes: ['neteaseVopen', 'wx55ad9609a9e87513', 'yxffe9005aacb94b60892f4918160ef12c', 'tencent100857527', 'wb1023607621']
```

### 通过爱思下载 IPA 文件
首先通过下方链接搜索应用名称

```
https://www.i4.cn/index_search.action?type=1&model=1&k={keyword}
```

然后复制其中一个链接，以 QQ 为例

```
https://www.i4.cn/app_detail_151375.html
```

最后运行脚本解析 IPA 文件中的 URL Scheme，结果中所有 list 都是可用的 URL Scheme。

```
$ python3 download.py  https://www.i4.cn/app_detail_151375.html
QQ: {"versionid":"835524672","icon":"http://d.image.i4.cn/image/icon/2020/04/14/12/444934666/z1586839082329_020411.jpg","code":1,"shortversion":"8.3.3","id":151375,"bundleid":"com.tencent.mqq","name":"QQ","path":"http://pc.i4.cn/1_151375","minversion":"9.0","sizebyte":354169281,"longversion":"8.3.3.615","itunesid":444934666,"pkagetype":1}
下载「QQ」IPA 文件中...
QQ 下载完成
IPA 文件「QQ」解压完毕
['mqqMsg2Tim']
['mqqtribe']
['mqqflyticket']
['mqqapi', 'mqqqzoneapi', 'mqqreservedapi']
['mqq']
['mqqopensdkapi']
['mqqOpensdkSSoLogin']
['wtloginmqq']
['wtloginmqq2']
['wtloginmqq3']
['mqqapiwallet']
['mqqopensdkapiV2']
['mqqwpa']
['mqqopensdkapiV3']
['wxf0a80d0ac2e82aa7']
['mqqwallet']
['mqqgamebindinggroup']
['mqqopensdkfriend']
['mqqvoipivr']
['mqqopensdkdataline']
['mqqopensdkgrouptribeshare']
['mqqwpaopenid']
['mqqconnect']
['mqqwalletv2']
['prefs']
['mqqopensdkapiV4']
['mqqconferenceflyticket']
['qqstory']
['kandianugc']
['wxeaef4303c20f3dea']
['wx820b0a1e23f2c841']
['wxcb89b8fc34e4e304']
['mqqv765']
['wx34b037fdb0f655ee']
['mqqopensdkavatar']
['mqqopensdkminiapp']
['mqqopensdklaunchminiapp']
['mqqthirdappgroup']
['mqqavshare']
['mqqnewfriend']
['wx76a769350165bcff']
['mqqwebview']
```

## 参考资料

[https://github.com/chinsyo/i4download](https://github.com/chinsyo/i4download)

## License

MIT
