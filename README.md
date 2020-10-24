# iOS URL Scheme 解析

该脚本用来解析 iOS IPA 文件中的 URL Scheme，可以用在快捷指令自动化操作。在使用该脚本前，优先推荐在[捷径社区](https://sharecuts.cn/apps)直接搜索应用名称，避免重复劳动，有未收录的 URL Scheme 也欢迎联系社区管理员进行提交。

## 安装依赖

```
$ pip3 install -r requirements.txt
```

## 使用方式

获取 IPA 文件之后，将 IPA 文件放置在 `ipa_file` 目录下，然后执行 `python3 parse_ipa.py`。下载 IPA 文件有以下两种方式。

### 通过 iMazing 或者老版 iTunes 下载 IPA
将 IPA 文件放在 ipa_file 目录下，然后运行
```
$ python3 parse_ipa.py
App Name: 网易公开课 OpenCourse
URL Schemes: ['neteaseVopen', 'wx55ad9609a9e87513', 'yxffe9005aacb94b60892f4918160ef12c', 'tencent100857527', 'wb1023607621']
```

### 通过爱思下载 IPA 文件
首先通过下方链接搜索应用名称：

```
https://www.i4.cn/index_search.action?type=1&model=1&k={keyword}
```

然后打开页面复制一个链接，以 QQ 为例：

```
https://www.i4.cn/app_detail_151375.html
```

最后运行脚本下载 IPA 文件并解析 URL Scheme，结果中 URL Schemes 均为可用的 URL Scheme。

一个完整的解析过程如下：

```
$ python3 download.py  https://www.i4.cn/app_detail_151375.html
QQ: {"versionid":"838238560","icon":"http://d.image.i4.cn/image/icon/2020/10/22/11/444934666/z1603338422005_818817.jpg","code":1,"shortversion":"8.4.10","id":151375,"bundleid":"com.tencent.mqq","name":"QQ","path":"http://pc.i4.cn/1_151375","minversion":"9.0","sizebyte":217140651,"longversion":"8.4.10.666","itunesid":444934666,"pkagetype":1}
下载「QQ」IPA 文件中...
QQ 下载完成
App Name: QQ QQ
URL Schemes: ['mqqMsg2Tim', 'mqqtribe', 'mqqflyticket', 'mqqapi', 'mqqqzoneapi', 'mqqreservedapi', 'mqq', 'mqqopensdkapi', 'mqqOpensdkSSoLogin', 'wtloginmqq', 'wtloginmqq2', 'wtloginmqq3', 'mqqapiwallet', 'mqqopensdkapiV2', 'mqqwpa', 'mqqopensdkapiV3', 'wxf0a80d0ac2e82aa7', 'mqqwallet', 'mqqgamebindinggroup', 'mqqopensdkfriend', 'mqqvoipivr', 'mqqopensdkdataline', 'mqqopensdkgrouptribeshare', 'mqqwpaopenid', 'mqqconnect', 'mqqwalletv2', 'prefs', 'mqqopensdkapiV4', 'mqqconferenceflyticket', 'qqstory', 'kandianugc', 'wxeaef4303c20f3dea', 'wx820b0a1e23f2c841', 'wxcb89b8fc34e4e304', 'mqqv765', 'wx34b037fdb0f655ee', 'mqqopensdkavatar', 'mqqopensdkminiapp', 'mqqopensdklaunchminiapp', 'mqqopensdkproxylogin', 'mqqthirdappgroup', 'mqqavshare', 'mqqnewfriend', 'wx76a769350165bcff', 'mqqwebview', 'wx1d0f5457c7556472', 'wb94065651']
```

## 参考资料

[https://github.com/chinsyo/i4download](https://github.com/chinsyo/i4download)

## License

MIT
