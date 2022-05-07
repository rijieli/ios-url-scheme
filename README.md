# iOS URL Scheme Parse

Language: **en-US** / [zh-CN](https://github.com/rijieli/ios-url-scheme/blob/master/README%5BZH%5D.md)

This script is used to parse the URL Scheme in iOS IPA files and can be used for iOS Shortcuts automation operations. Before using this script, it is recommended to search the application name directly in [Sharecuts](https://sharecuts.cn/apps) to avoid duplication of work, and you are welcome to contact the community administrator to submit any URL Scheme that is not included.

## Installing Dependencies

```
$ pip3 install -r requirements.txt
```

## Usage

* Get IPA files, then create a directory named `ipa_file`
* run `python3 parse_ipa.py`

## Example Output
```
$ python3 parse_ipa.py
App Name: OpenCourse
URL Schemes: ['neteaseVopen', 'wx55ad9609a9e87513', 'yxffe9005aacb94b60892f4918160ef12c', 'tencent100857527', 'wb1023607621']
```

## How to get IPA File

### 1. iMazing App

iMazing: https://imazing.com

iMazing is a popular iPhone manage tool, on its app manage feature, you can search and download apps, then right-click on the downloaded item and select export `.ipa` file。

### 2. Apple Configurator 2

Apple Configurator 2: https://apps.apple.com/cn/app/id1037126344

Apple Configurator is a macOS app provided by apple. Like iMazing, search and download apps, but **stop at installing confirmation menu**, open Configurator's cache directory you will see the IPA file. **Note: Stop before it installs to your phone**, if you click yes, Configurator will clean cached IPA files。

The directory goes here:
```
~/Library/Group\ Containers/K36BKF7T3D.group.com.apple.configurator/Library/Caches/Assets/TemporaryItems/MobileApps/
```

### 3. PlayCover

PlayCover is an M1 Mac sideload tool，they provide some IPA。

PlayCover IPA: [ipa.playcover.workers.dev](https://ipa.playcover.workers.dev/0:/)

### 4. i4.cn

First use link below search app name(replace keyword with name）：

```
https://www.i4.cn/index_search.action?type=1&model=1&k={keyword}
```

Get app page link such as `https://www.i4.cn/app_detail_151375.html`

Then run `download.py {page link}`

Example：

```
$ python3 download.py https://www.i4.cn/app_detail_151375.html
QQ: {"versionid":"838238560","icon":"http://d.image.i4.cn/image/icon/2020/10/22/11/444934666/z1603338422005_818817.jpg","code":1,"shortversion":"8.4.10","id":151375,"bundleid":"com.tencent.mqq","name":"QQ","path":"http://pc.i4.cn/1_151375","minversion":"9.0","sizebyte":217140651,"longversion":"8.4.10.666","itunesid":444934666,"pkagetype":1}
Downloading「QQ」IPA file...
QQ downloaded
App Name: QQ QQ
URL Schemes: ['mqqMsg2Tim', 'mqqtribe', 'mqqflyticket', 'mqqapi', 'mqqqzoneapi', 'mqqreservedapi', 'mqq', 'mqqopensdkapi', 'mqqOpensdkSSoLogin', 'wtloginmqq', 'wtloginmqq2', 'wtloginmqq3', 'mqqapiwallet', 'mqqopensdkapiV2', 'mqqwpa', 'mqqopensdkapiV3', 'wxf0a80d0ac2e82aa7', 'mqqwallet', 'mqqgamebindinggroup', 'mqqopensdkfriend', 'mqqvoipivr', 'mqqopensdkdataline', 'mqqopensdkgrouptribeshare', 'mqqwpaopenid', 'mqqconnect', 'mqqwalletv2', 'prefs', 'mqqopensdkapiV4', 'mqqconferenceflyticket', 'qqstory', 'kandianugc', 'wxeaef4303c20f3dea', 'wx820b0a1e23f2c841', 'wxcb89b8fc34e4e304', 'mqqv765', 'wx34b037fdb0f655ee', 'mqqopensdkavatar', 'mqqopensdkminiapp', 'mqqopensdklaunchminiapp', 'mqqopensdkproxylogin', 'mqqthirdappgroup', 'mqqavshare', 'mqqnewfriend', 'wx76a769350165bcff', 'mqqwebview', 'wx1d0f5457c7556472', 'wb94065651']
```

## References

[https://github.com/chinsyo/i4download](https://github.com/chinsyo/i4download)

## License

MIT
