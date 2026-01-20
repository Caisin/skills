# Uni-App-Core - Tutorials

**Pages:** 2

---

## iOS平台Capabilities配置 | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/tutorial/app-ios-capabilities#associateddomains.md

**Contents:**
- # iOS平台Capabilities配置
- # HBuilderX4.18及以上版本
- # HBuilderX4.18以前版本
- # 通用链接（Universal Link）配置教程
  - # 第一步：开启Associated Domains服务
  - # 第二步：配置Associated Domains（域名）
    - # uni-app/5+ App项目
    - # uni-app x项目
    - # 本地离线打包
  - # 第三步：服务器配置apple-app-site-association文件

在XCode中可给工程添加设置Capabilities，如图所示：

配置后，会更新XCode工程的.entitlements和Info.plist文件，此文章介绍如何在HBuilderX中配置iOS平台的Capabilities。

注意：uni-app x 项目只支持此方式配置

将 XCode 工程中的 .entitlements 文件中的内容配置到 iOS原生应用配置文件和资源 的 UniApp.entitlements 文件，详情参考：配置文件UniApp.entitlements

将 XCode 工程中的 Info.plist 文件中的内容配置到 iOS原生应用配置文件和资源 的 Info.plist 文件，详情参考：配置文件 Info.plist

将XCode工程中的 .entitlements 和 Info.plist 文件中的内容转换为json格式数据配置到manifest.json文件中，使得HBuilderX云端打包工程设置相应的Capabilities。

打开项目的manifest.json文件，在源码视图中进行配置

示例源码如下，请查看 pre > code 标签中的内容

其中entitlements数据（json）将转换成XCode工程中entitlements文件的数据（字典格式） plists节点数据将转换成XCode工程中Info.plist文件的数据（字典格式）

为了简化配置使用通用链接，推荐使用UniCloud快速生成通用链接，详情参考：一键生成iOS通用链接

Universal Link是苹果在WWDC 2015上提出的iOS 9的新特性之一。此特性类似于深层链接，并能够方便地通过打开一个Https链接来直接启动您的客户端应用(手机有安装App)。对比起以往所使用的URL Sheme, 这种新特性在实现web-app的无缝链接时能够提供极佳的用户体验。 使用前请阅读苹果官方文档 使用通用链接（Universal Link）必须要有域名，下面的配置中将要用到

登录苹果开发者网站，在“Certificates, Identifiers & Profiles”页面选择“Identifiers”中选择对应的App ID，确保开启Associated Domains服务

开启Associated Domains服务后需要重新生成profile文件，提交云端打包时使用

使用HBuilderX可视化界面配置 打开项目的manifest.json文件，切换到“App常用其它设置”项，在“iOS设置”下的“关联域（Associated Domains）”中进行配置：

使用HBuilderX源码视图配置 打开项目的manifest.json文件，切换到“源码视图”项，在uni-app项目在"app-plus" -> "distribute" -> "ios" -> "capabilities" -> "entitlements"节点下添加"com.apple.developer.associated-domains"字段，字段值为字符串数组，每个字符串为要关联的域名：

示例源码如下，请查看 pre > code 标签中的内容

其中demo.dcloud.net.cn是应用通用链接的域名（这里不要包含path），请修改为自己应用要使用的域名

5+ App项目源码视图配置节点为："plus" -> "distribute" -> "apple" -> "capabilities" -> "entitlements"

HBuilderX4.71 及以上版本支持 manifest.json 可视化配置，详情参考：uni-app x 关联域 配置 。

HBuilderX4.71 以下版本未提供 maniest.json 可视化配置，需在项目下创建 "nativeResources" -> "ios" 目录，添加UniApp.entitlements文件配置，详情参考：https://uniapp.dcloud.net.cn/tutorial/app-nativeresource-ios.html#domains 。

在原生XCode工程中配置通用链接域名（使用HBuilderX云端打包跳过）

HBuilderX中自带的默认真机运行基座HBuilderX注册的通用链接为：https://demo.dcloud.net.cn/ulink/

需要在上面域名对应的服务器上放apple-app-site-association文件。 apple-app-site-association文件配置如下：

示例源码如下，请查看 pre > code 标签中的内容

注意：不要直接拷贝使用上面的示例，必须根据自己应用的配置修改 把配置好的apple-app-site-association文件上传到你自己的服务器，确保通过https://demo.dcloud.net.cn/.well-known/apple-app-site-association可访问。

其中demo.dcloud.net.cn为上面配置的域名 应用安装后会通过访问上面的url向系统注册应用的通用链接。

推荐方案：将apple-app-site-association文件部署到，免费的阿里云版unicloud的 前端网页托管

可通过5+ API的plus.runtime.launcher 判断应用启动来源，如果其值为"uniLink"则表示通过通用链接启动应。 这时可通过5+ API的plus.runtime.arguments 获取启动参数，通用链接启动的情况将返回完整的通用链接地址。

在 App.uvue 文件的应用生命周期 onLaunch 和 onShow 回调参数中可通过 appLink 属性获取通用链接地址。

也可以通过 API： uni.getLaunchOptionsSync 和 uni.getEnterOptionsSync 返回值中的 appLink 属性获取通用链接地址。

**Examples:**

Example 1 (json):
```json
"capabilities": {
		"entitlements": {	// 合并到工程entitlements文件的数据（json格式）
		},
		"plists": {			// 合并到工程Info.plist文件的数据（json格式）
		}
	},
```

Example 2 (json):
```json
"capabilities": {
		"entitlements": {	// 合并到工程entitlements文件的数据（json格式）
		},
		"plists": {			// 合并到工程Info.plist文件的数据（json格式）
		}
	},
```

Example 3 (json):
```json
"capabilities": {
		"entitlements": {	// 合并到工程entitlements文件的数据（json格式）
		},
		"plists": {			// 合并到工程Info.plist文件的数据（json格式）
		}
	},
```

Example 4 (json):
```json
"capabilities": {
		"entitlements": {	// 合并到工程entitlements文件的数据（json格式）
		},
		"plists": {			// 合并到工程Info.plist文件的数据（json格式）
		}
	},
```

---

## Geolocation定位 | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/tutorial/app-geolocation#lic.md

**Contents:**
- # Geolocation定位
  - # 系统定位
    - # iOS平台
    - # Android平台
  - # 高德定位
    - # 参数说明
    - # 高德开放平台用户名
  - # 腾讯定位
    - # 参数说明
  - # 商业授权相关说明

定位模块封装了OS自带的系统定位，及市场上主流的三方定位SDK，如高德定位、腾讯定位等。并提供统一的JS API调用定位能力。

三方定位（高德、腾讯、谷歌等）是商业收费服务，需获取授权，注意避免侵权。详见

使用定位功能需在项目manifest.json的“App模块配置”中勾选“Geolocation(定位)”，并根据项目实际需求勾选使用的三方定位SDK：

HBuilderX3.2.16开始独立出“系统定位”模块

使用系统定位需在“App模块配置”项的“Geolocation(定位)”下，勾选“系统定位”：

系统定位调用设备的操作系统提供的定位服务，只支持wgs84坐标系，不同设备对定位功能支持的情况有所差异。

由苹果iOS系统提供定位服务，可以获取经纬度信息，支持解析地址信息，即可以直接返回城市街道信息。

只可以获取经纬度信息，不支持解析地址信息，即无法返回城市街道信息。

标准Android系统的定位服务是Google的GMS服务，需连接Google服务器。中国大陆地区用户无法翻墙，导致无法使用定位，或者很多国产手机阉割掉了GMS，也导致无法使用定位。

国内手机厂商早期均没有内置替代GMS的位置服务，这些设备上只能使用三方定位。但后期大品牌手机和三方定位合作，内置了替代GMS的版本。如下Android手机厂商的新款手机都支持系统定位：

其他小众品牌可能不支持，主流品牌中较老的机型也不支持，暂无机型清单，需自行测试。

需要向高德申请商业授权，参考:商业授权相关说明，使用前需登录 高德开放平台 创建应用申请Key

使用高德定位需在“App模块配置”项的“Geolocation(定位)”下，勾选“高德定位”：

登录 高德开放平台 ，进入“控制台”，在“账号信息”的“基本信息”中可获取“用户名”：

HBuilderX4.31 新增支持 腾讯定位 需要向腾讯申请商业授权，参考:商业授权相关说明，使用前需登录 腾讯位置服务官网 创建应用申请Key

使用腾讯定位需在“安卓/iOS模块配置”项的“Geolocation(定位)”下，勾选“腾讯定位”：

2021年起，高德、腾讯、百度等地图服务商开始商业授权。

例外：如果是公益类应用，可以申请豁免商业授权。只要不是公益应用，不管你有多少用户，都需要获取商业授权。

如需购买地图的商业授权，请点击 获取优惠 。

部分中介采用共享地图授权的模式，吸引开发者向该中介采购地图授权。本质是中介向地图厂商支付授权费，然后把开发者的应用创建到中介在地图厂商的账户下。

这种做法是纯粹的骗局。因为开发者向中介支付了费用，虽然可能低于地图厂商的授权费，但开发者并没有获得商业许可。地图厂商的商业许可是出具给中介的，开发者仍然是侵权的。地图厂商仍然会给您打电话催缴商业许可费用。

所以请开发者务必注意，付款时一定要拿到地图厂商向您出具的授权许可。切勿付了款又没有得到授权，财物两空。

对于已经被中介欺骗的开发者，请尽快向公安报案。

海外用户使用google地图，也需要付费，支持按量付费，具体请参阅google地图官网。

---
