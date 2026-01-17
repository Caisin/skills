---
url: 'https://uviewpro.cn/zh/components/actionSheet.md'
---
# ActionSheet 操作菜单&#x20;

本组件用于从底部弹出一个操作菜单，供用户选择并返回结果。\
本组件功能类似于 uni 的`uni.showActionSheet`API，配置更加灵活，所有平台都表现一致。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`list`设置需要显示的菜单，该值为一个数组，元素为对象，对象至少要提供`text`属性，另外可选的有`fontSize`(字体大小)，`color`(颜色)，`disabled`(是否禁用)，
  `subText`(描述信息)
* 通过`v-model`绑定一个值为布尔值的变量控制组件的弹出与收起，`v-model`的值是双向绑定的

```html
<template>
  <view>
    <u-action-sheet :list="list" v-model="show"></u-action-sheet>
    <u-button @click="show = true">打开ActionSheet</u-button>
  </view>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  // 定义列表数据
  const list = ref<ActionSheetItem[]>([
    {
      text: '点赞',
      color: 'blue',
      fontSize: '28rpx',
      subText: '感谢您的点赞'
    },
    {
      text: '分享'
    },
    {
      text: '评论'
    }
  ])

  // 控制 ActionSheet 显示状态
  const show = ref(false)
</script>
```

## 配置顶部的提示信息和底部取消按钮

* `tips`参数为一个对象类型，属性可以设置`text`，`fontSize`(字体大小)，`color`(颜色)，文本内容将会显示组件的上方，起提示作用。
* `cancel-btn`参数配置是否显示底部的取消按钮，默认显示

```html
<template>
  <u-action-sheet
    :list="list"
    v-model="show"
    :tips="tips"
    :cancel-btn="true"
  ></u-action-sheet>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetTips, ActionSheetItem } from 'uview-pro/types/global'

  // 顶部提示信息
  const tips = ref<ActionSheetTips>({
    text: '在水一方',
    color: '#909399',
    fontSize: '24rpx'
  })

  // 按钮列表
  const list = ref<ActionSheetItem[]>([
    {
      text: '点赞',
      color: 'blue',
      fontSize: '28rpx'
    }
  ])

  // 控制显示状态
  const show = ref(true)
</script>
```

## 如何知道点了第几项

`click`回调事件带有一个`index`值，这个索引值为传递的`list`数组的索引值，根据回调事件，能获得点击了
第几项和该项的内容

```html
<template>
  <u-action-sheet
    :list="list"
    @click="handleClick"
    v-model="show"
  ></u-action-sheet>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  // 按钮列表
  const list = ref<ActionSheetItem[]>([
    {
      text: '点赞',
      color: 'blue',
      fontSize: '28rpx'
    },
    {
      text: '分享'
    },
    {
      text: '评论'
    }
  ])

  // 控制显示状态
  const show = ref(true)

  // 处理点击事件
  const handleClick = (index: number) => {
    console.log(`点击了第${index + 1}项，内容为：${list.value[index].text}`)
  }
</script>
```

## 自定义 item 内容&#x20;

从`v0.3.5`开始，`u-action-sheet`开始支持自定义`item`内容，通过定义 u-action-sheet-item 的`slot="default"`插槽，传入自定义的`item`内容，会覆盖默认的`item`内容。
该功能兼容使用`list`配置数据的方式。

如下示例：

```vue
<template>
  <u-action-sheet
    :list="list"
    v-model="show"
    @click="handleClick"
  ></u-action-sheet>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import type { ActionSheetItem } from 'uview-pro/types/global'

const show = ref(true)

const list = ref<ActionSheetItem[]>([
  {
    text: '最是人间留不住'
  },
  {
    text: '朱颜辞镜花辞树',
    disabled: true
  },
  {
    text: '正是江南好风景',
    subText: '春江水暖鸭先知'
  },
  {
    text: '落花时节又逢君'
  }
])

function handleClick(index: number) {
  console.log('点击了第' + (index + 1) + '项')
}
</script>
```

当你要使用`u-action-sheet-item`时，不需要传入`list`即可，如使用以下代码是同样的效果：

```html
<template>
  <u-action-sheet v-model="show" @click="handleClick">
    <u-action-sheet-item
      v-for="(item, index) in list"
      :key="index"
      :text="item.text"
      :sub-text="item.subText"
      :disabled="item.disabled"
    />
  </u-action-sheet>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  const show = ref(true)

  const list = ref<ActionSheetItem[]>([
    {
      text: '最是人间留不住'
    },
    {
      text: '朱颜辞镜花辞树',
      disabled: true
    },
    {
      text: '正是江南好风景',
      subText: '春江水暖鸭先知'
    },
    {
      text: '落花时节又逢君'
    }
  ])

  function handleClick(index: number) {
    console.log('点击了第' + (index + 1) + '项')
  }
</script>
```

使用`slot`自定义内容，则需要使用`u-action-sheet-item`组件，如下示例：

```html
<template>
  <u-action-sheet v-model="show">
    <u-action-sheet-item>
      <u-text
        type="success"
        text="我是自定义的（微信能力）"
        size="32"
        openType="openSetting"
        @click="handleClick"
      ></u-text>
    </u-action-sheet-item>
  </u-action-sheet>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import type { ActionSheetItem } from 'uview-pro/types/global'

  const show = ref(true)

  function handleClick(index: number) {
    console.log('点击了第' + (index + 1) + '项')
    show.value = false
  }
</script>
```

## API

## ActionSheet Props

注意：props 中没有控制组件弹出与收起的参数，因为这是通过 v-model 绑定变量实现的，见上方说明。
|参数|说明|类型|默认值|可选值|
|-|-|-|-|-|
|list|按钮的文字数组，见上方文档示例|Array\<Object>|\[]|-|
|tips|顶部的提示文字，见上方文档示例|Object|-|-|
|cancel-btn|是否显示底部的取消按钮|Boolean|true|false|
|border-radius|弹出部分顶部左右的圆角值，单位 rpx|Number \ String|0|-|
|mask-close-able|点击遮罩是否可以关闭|Boolean|true|false|
|safe-area-inset-bottom|是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明)|Boolean|false|true|
|z-index|`z-index`值|Number \ String|1075|-|
|cancel-text|取消按钮的提示文字|String|取消|-|
|async-close |是否异步关闭|Boolean|false|true|

## ActionSheet Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| click | 点击ActionSheet列表项时触发 | index: 点击了第几个，从0开始 | - |
| close | 点击取消按钮时触发 | - | - |

## ActionSheet-item Props&#x20;

注意：props 中没有控制组件弹出与收起的参数，因为这是通过 v-model 绑定变量实现的，见上方说明。

|参数|说明|类型|默认值|可选值|
|:-|:-|:-|:-|:-|
|text|标题|String|''|-|
|subText|描述|String|''|-|
|padding|边距|Number \ String|'34rpx 0'|-|
|color|字体颜色|String|mainColor|-|
|fontSize|字体大小|Number \ String|'32rpx'|-|
|disabled|是否禁用|Boolean|false|true|
|asyncClose|是否异步关闭|Boolean|false|true|

## ActionSheet-item Slot&#x20;

|名称|说明|
|:-|:-|
|default|自定义item内容|

## ActionSheet-item Event&#x20;

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| click | 点击ActionSheet列表项时触发 | index: 点击了第几个，从0开始 | - |
| async-close | 是否异步关闭 | Boolean  | false | true |

---

---
url: 'https://uviewpro.cn/zh/components/alertTips.md'
---
# AlertTips 警告提示&#x20;

警告提示，展现需要关注的信息。

## 使用场景

* 当某个页面需要向用户显示警告的信息时。
* 非浮层的静态展现形式，始终展现，不会自动消失，用户可以点击关闭。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`title`和`description`设置组件的标题和描述内容，如果内容和标题同时存在，标题字体会被加粗加大
* 通过`type`设置主题类型，有`primary`,`success`,`error`,`warning`,`info`可选值

```html
<template>
	<u-alert-tips type="warning" :title="title" :description="description"></u-alert-tips>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('登高望远')
const description = ref('欲穷千里目，更上一层楼')
</script>
```

## 图标

通过`show-icon`设置是否显示图标，作用是让信息类型更加醒目。

**注意**：当前版本图标为uView内置图标，根据`type`参数显示不同的图标，无法自定义。

```html
<u-alert-tips type="warning" :show-icon="true"></u-alert-tips>
```

## 可关闭的警告提示

显示关闭按钮，点击可关闭警告提示。

* `close-text`参数配置关闭的文字，默认为一个叉的icon图标。`close-able`为`true`时有效
* `close-able`参数配置是否允许关闭的文字或图标

::: warning 注意
由于`props`传参的限制，您需要监听组件的`close`事件，并在此此事件中设置`show`参数为`false`，才能关闭组件。
:::

```html
<template>
	<u-alert-tips :show="show" type="error" @close="show = false" :title="title" :close-able="true"></u-alert-tips>
	
	<u-alert-tips type="error" :title="title" close-text="close" :description="description" :close-able="true"></u-alert-tips>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('寻隐者不遇')
const description = ref('松下问童子，言师采药去。只在此山中，云深不知处。')
const show = ref(true)
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| title | 显示的文字  | String | - | - |
| description | 辅助性文字，颜色比`title`浅一点，字号也小一点，可选 | String  | - | - |
| close-able | 关闭按钮(默认为叉号icon图标) | Boolean  | false | true |
| type | 使用预设的颜色 | String  | warning | success / primary / error / info |
| close-text | 用文字替代关闭图标，`close-able`为`true`时有效 | String  | - | - |
| show-icon | 是否显示左边的辅助图标 | Boolean  | false | true |
| show | 显示或隐藏组件 | Boolean  | true | false |
| icon | 左侧的图标名称，如设置`type`和`show-icon`值，会有一个默认的图标 | String  | - | - |
| icon-style | 自定义图标的样式，对象形式 | Object  | - | - |
| title-style | 自定义标题的样式，对象形式 | Object  | - | - |
| desc-style | 自定义内容的样式，对象形式 | Object  | - | - |

## Events

|事件名|说明|回调参数|
|:-|:-|:-|
|close|点击关闭按钮时触发，需在此回调设置`show`为`false`|-|
|click|点击组件时触发|-|

---

---
url: 'https://uviewpro.cn/zh/components/avatar.md'
---
# Avatar 头像&#x20;

本组件一般用于展示头像的地方，如个人中心，或者评论列表页的用户头像展示等场所。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`src`指定头像的路径即可简单使用，如果传递了`text`参数，`text`将会优先起作用

**注意：** 请保证传递给`src`的是绝对地址，而不是相对地址，为什么呢？因为传入`avatar`组件的相对地址，是相对于组件的，而不是父组件(页面)，所以相对址可能会出错。

```html
<template>
	<view>
		<u-avatar :src="src"></u-avatar>
		<u-avatar :text="text"></u-avatar>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const src = ref('http://pic2.sc.chinaz.com/Files/pic/pic9/202002/hpic2119_s.jpg')
const text = ref('无头像')
</script>
```

## 头像类型

* `mode`参数指定头像的类型，取值`circle`为圆形，取值`square`为圆角方形

```html
<template>
	<u-avatar :src="src" mode="square"></u-avatar>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const src = ref('http://pic2.sc.chinaz.com/Files/pic/pic9/202002/hpic2119_s.jpg')
</script>
```

## 默认头像

如果头像加载失败，导致加载图片失败，将会显示一个默认的灰色头像

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| bg-color | 背景颜色，一般显示文字时用  | String | #ffffff | - |
| src | 头像路径，如加载失败，将会显示默认头像  | String	 | - | - |
| size | 头像尺寸，可以为指定字符串(large, default, mini)，或者数值，单位rpx | String | Number  | default | - |
| mode | 显示类型，见上方说明 | String  | circle | square |
| text | 用文字替代图片，级别优先于`src` | String  | - | - |
| img-mode | 头像图片的裁剪类型，与uni的`image`组件的`mode`参数一致，如效果达不到需求，可尝试传`widthFix`值 | String  | aspectFill | - |
| show-sex | 是否显示右上角的性别图标 | Boolean  | false | true |
| sex-icon | 右上角性别图标，可传入图片路径，或内置图标名 | String  | man | woman |
| sex-bg-color | 性别图标的背景颜色 | String  | man-primary主题，woman-error主题 | - |
| show-level | 是否显示右下角的等级图标 | Boolean  | false | true |
| level-icon | 右下角等级图标，可传入图片路径，或内置图标名 | String  | level | - |
| level-bg-color | 等级图标的背景颜色 | String  | warning主题 | - |

## Event

|事件名|说明|回调参数|
|:-|:-|:-|
| click | 头像被点击 | index: 用户传递的标识符 |

---

---
url: 'https://uviewpro.cn/zh/components/avatarCropper.md'
---
# AvatarCropper 头像裁剪&#x20;

该组件一般的图片裁剪需求场景，尤其适合于头像裁剪方面。

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

组件使用流程：

1. 打开头像裁剪页面，同时传递配置基本参数(已默认配置好最优参数)
2. 选取图片，调整图片合适位置和大小，确定裁剪并返回此裁剪结果
3. 在原始页面监听`uAvatarCropper`事件，获得裁剪结果

```html
<template>
  <view class="wrap">
    <view class="u-avatar-wrap">
      <image class="u-avatar-demo" :src="avatar" mode="aspectFill"></image>
    </view>
    <u-button @tap="chooseAvatar">进入裁剪页</u-button>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const avatar = ref("https://ik.imagekit.io/anyup/uview-pro/common/logo-new.png")

// 监听从裁剪页发布的事件，获得裁剪结果
const handleAvatarCropper = (path) => {
  avatar.value = path
  // 可以在此上传到服务端
  uni.uploadFile({
    url: "http://www.example.com/upload",
    filePath: path,
    name: "file",
    complete: (res) => {
      console.log(res)
    },
  })
}

onMounted(() => {
  // 监听裁剪事件
  uni.$on("uAvatarCropper", handleAvatarCropper)
})

onUnmounted(() => {
  // 移除事件监听
  uni.$off("uAvatarCropper", handleAvatarCropper)
})

const chooseAvatar = () => {
  // 此为uView的跳转方法，详见"文档-JS"部分，也可以用uni的uni.navigateTo
  uni.$u.route({
    // 关于此路径，请见下方"注意事项"
    url: "/uview-pro/components/u-avatar-cropper/u-avatar-cropper",
    // 内部已设置以下默认参数值，可不传这些参数
    params: {
      // 输出图片宽度，高等于宽，单位px
      destWidth: 300,
      // 裁剪框宽度，高等于宽，单位px
      rectWidth: 200,
      // 输出的图片类型，如果'png'类型发现裁剪的图片太大，改成"jpg"即可
      fileType: "jpg",
    },
  })
}
</script>

<style lang="scss" scoped>
  .wrap {
    padding: 40rpx;
  }

  .u-avatar-wrap {
    margin-top: 80rpx;
    overflow: hidden;
    margin-bottom: 80rpx;
    text-align: center;
  }

  .u-avatar-demo {
    width: 150rpx;
    height: 150rpx;
    border-radius: 100rpx;
  }
</style>
```

## 注意事项

根据`下载`方式和`NPM`方式引入 uView 的不同，需要进行不同的处理，下载方式可以引用`uview-pro`中的某个文件当做页面文件，但是`NPM`方式，不能引入
`node_modules`文件夹中的`uview-pro`包的某个文件当做页面路径，故下方对两个方式分别说明：

### 1. 下载引入 uView 方式

* 裁剪页面内置在 uView 中，由于打开页面，需要先在`pages.json`声明页面，故请把以下内容复制到项目根目录的`pages.json`中的`pages`数组中：

```js
{
	"path": "uview-pro/components/u-avatar-cropper/u-avatar-cropper",
	"style": {
		"navigationBarTitleText": "头像裁剪",
		"navigationBarBackgroundColor": "#000000"
	}
}
```

### 1. NPM 引入 uView 方式

您需要去`node_modules`文件中，按路径`/node_modules/uview-pro/components/u-avatar-cropper/u-avatar-cropper.vue`找到此文件，将其内容复制出来，
放到`/pages`文件夹中的某个文件中，再按上面下载方式引入的一样的操作，去声明和引用页面即可。

* 裁剪后的结果，通过`uni.$on`监听`uAvatarCropper`事件，由于 uni-app 限制，H5 端裁剪的结果为`base64`格式，其他端为`blod`二进制形式，
  如果后端对接收格式有要求，请自行处理

## API

以下参数，需要通过 URL 的 get 参数传参到裁剪页，非 props。uView 很多组件传递值的单位为`rpx`，注意这里的`dest-width`和`rect-width`单位为`px`

## URL 参数

| 参数       | 说明                                                           | 类型             | 默认值 | 可选值 |
| ---------- | -------------------------------------------------------------- | ---------------- | ------ | ------ |
| dest-width | 输出图片宽度，高等于宽，单位**px**                             | String | Number | 200    | -      |
| rect-width | 裁剪框宽度，高等于宽，单位**px**                               | String | Number | 200    | -      |
| file-type  | 输出的图片类型，如果'png'类型发现裁剪的图片太大，改成"jpg"即可 | String           | jpg    | png    |

## Event

| 事件名         | 说明                                | 回调参数             |
| :------------- | :---------------------------------- | :------------------- |
| uAvatarCropper | 裁剪结束后的事件，通过`uni.$on`监听 | path: 裁剪的图片数据 |

---

---
url: 'https://uviewpro.cn/zh/components/backTop.md'
---
# BackTop 返回顶部&#x20;

该组件一个用于长页面，滑动一定距离后，出现返回顶部按钮，方便快速返回顶部的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

由于返回顶部需要实时监听滚动条的位置，从而判断返回的按钮该出现还是隐藏，由于组件无法得知页面的滚动条信息，只能在**页面**的`onPageScroll`生命周期
中获得滚动条的位置，故需要在页面监听`onPageScroll`生命周期，实时获得滚动条的位置，通过Props传递给组件。

```html
<template>
	<view class="wrap">
		<text>滑动页面，返回顶部按钮将出现在右下角</text>
		<u-back-top :scroll-top="scrollTop"></u-back-top>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const scrollTop = ref(0)

// 页面滚动事件处理
onPageScroll: function(e) {
	console.log("滚动距离为：" + e.scrollTop);
	scrollTop.value = e.scrollTop
}
</script>

<style lang="scss" scoped>
	.wrap {
		height: 200vh;
	}
</style>
```

## 改变返回顶部按钮的出现时机

可以通过`top`参数，修改页面滚动多少距离时，出现返回顶部的按钮

```html
<u-back-top :scroll-top="scrollTop" top="600"></u-back-top>
```

## 自定义返回顶部的图标和提示

* 通过`icon`修改返回顶部按钮的图标，可以是uView内置的图标，或者图片路径
* 通过`tips`参数修改返回顶部按钮的文字提示信息，如果需要修改文字的颜色和大小，可以通过`custom-style`参数

```html
<u-back-top :scroll-top="scrollTop" icon="arrow-up" tips="返回"></u-back-top>
```

## 其他自定义样式

* 通过`icon-style`参数自定义图标的样式，比如颜色，大小等
* 通过`custom-style`修改返回按钮的背景颜色，大小等
* 通过`mode`修改按钮的形状，`circle`为圆形，`square`为方形

注意：如果通过`icon`参数传入图片路径的话，需要通过`icon-style`参数设置图片的`width`和`height`属性

```html
<template>
	<view class="wrap">
		<text>滑动页面，返回顶部按钮将出现在右下角</text>
		<u-back-top :scrollTop="scrollTop" :mode="mode" :icon-style="iconStyle"></u-back-top>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const scrollTop = ref(0)
const mode = ref('square')
const iconStyle = reactive({
	fontSize: '32rpx',
	color: '#2979ff'
})

// 页面滚动事件处理
onPageScroll: function(e) => {
	scrollTop.value = e.scrollTop
}
</script>

<style lang="scss" scoped>
	.wrap {
		height: 200vh;
	}
</style>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| mode | 按钮形状 | String | circle | square |
| icon | uView内置图标名称，或图片路径 | String  | arrow-upward | - |
| tips | 返回顶部按钮的提示文字 | String  | - | - |
| duration | 返回顶部过程中的过渡时间，单位ms | String | Number  | 100 | - |
| scroll-top | 页面的滚动距离，通过`onPageScroll`生命周期获取 | String | Number  | 0 | - |
| top | 滚动条滑动多少距离时显示，单位rpx | String | Number  | 400 | - |
| bottom | 返回按钮位置到屏幕底部的距离，单位rpx | String | Number  | 200 | - |
| right | 返回按钮位置到屏幕右边的距离，单位rpx | String | Number  | 40 | - |
| z-index | 返回顶部按钮的层级 | String | Number  | 9 | - |
| icon-style | 图标的样式，对象形式 | Object  | - | - |

## Slot

|名称|说明|
|:-|:-|
| - | 自定义返回按钮的所有内容 |

---

---
url: 'https://uviewpro.cn/zh/components/badge.md'
---
# Badge 徽标数&#x20;

该组件一般用于图标右上角显示未读的消息数量，提示用户点击，有圆点和圆包含文字两种形式。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`count`参数定义徽标内容
* 通过`type`设置主题。重申一次，uView中，所有组件的`type`参数都只有5个固定的可选值，分别是`primary`(蓝色-主色)，`warning`(黄色-警告)，
  `error`(红色-错误)，`success`(绿色-成功)，`info`(灰色-信息)

::: warning 注意
此组件内部默认为`absolute`绝对定位，所以需要给`badge`父组件(元素)设置`position: relative`相对定位，
再通过调整`offset`偏移值(数组，两个元素，第一个元素为`top`值，第二个元素为`right`值，单位rpx，可为负值，如"\[-10, -10]")设置到合适的位置即可。\
如果不需要组件内容默认的自动绝对定位，设置`absolute`参数为`false`即可。
:::

```html
<u-badge type="error" count="7"></u-badge>
```

## 设置徽标的尺寸

`size`参数默认为`default`，如果设置为`mini`，将会得到一个小尺寸的徽标，组件内部通过css的`scale`属性值进行缩放。

```html
<u-badge size="mini" type="success"></u-badge>
```

## 设置徽标的类型为一个圆点

通过`is-dot`参数设置，该形式组件没有内容，只显示一个圆点

```html
<u-badge :is-dot="true" type="success"></u-badge>
```

## 自定义徽标样式

该组件内部通过一个`view`元素实现，是一个根元素，依据`vue-cli`的`vue-loader`特性，在引用的组件上直接写类名或者内联样式，可以作用于组件内部的
根元素上(微信小程序除外)，所以用户可以在组件引用时自定义修改样式

```html
<u-badge type="green" class="badge"></u-badge>

<style scoped>
	.badge {
		background-color: blue;
		color: white;
	}
</style>
```

## 如何让组件中心点与父组件右上角重合

某些特殊的场景下，特别是`badge`内容值是通过后端获取，长度未知时，会导致最终渲染出来的`badge`组件的位置与父组件右上角的位置有出入，
为了解决这个问题，uView提供了一个`is-center`(默认为`false`)，如果设置为`true`，`offset`参数将会失效，同时`badge`组件的中心点
将会和父组件的右上角重合。

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| count | 展示的数字，大于 `overflowCount` 时显示为 `${overflowCount}+`，为`0`且`show-zero`为`false`时隐藏  | String | Number | - | - |
| is-dot | 不展示数字，只有一个小点 | Boolean  | false | true |
| absolute | 组件是否绝对定位，为`true`时，`offset`参数才有效 | Boolean  | true | false |
| overflow-count | 展示封顶的数字值 | String | Number  | 99 | - |
| type | 使用预设的背景颜色 | String  | error | success / primary / warning / info |
| show-zero | 当数值为 0 时，是否展示 Badge | Boolean  | false | true |
| size | Badge的尺寸，设为`mini`会得到小一号的`Badge` | String  | default | mini |
| offset | 设置badge的位置偏移，格式为 \[x, y]，也即设置的为`top`和`right`的值，单位rpx。`absolute`为`true`时有效 | Array | \[20, 20] | - |
| color | 字体颜色 | String  | #ffffff | - |
| bgColor | 背景颜色，优先级比`type`高，如设置，`type`参数会失效 | String  | - | - |
| is-center | 组件中心点是否和父组件右上角重合，优先级比`offset`高，如设置，`offset`参数会失效 | Boolean  | false | true |

---

---
url: 'https://uviewpro.cn/zh/components/button.md'
---
# Button 按钮&#x20;

该组件内部实现以uni-app`button`组件为基础，进行二次封装，主要区别在于：

* 按钮`type`值有更多的主题颜色
* 有可选的按钮点击水波纹效果
* 按钮`size`值有更多的尺寸可选

::: warning 注意

1. 此组件内部使用uni-app`button`组件为基础，除了开头中所说的增加的功能，另外暴露出来的props属性和官方组件的属性完全一致，
   uni-app`button`组件比较特殊，因为它有一些其他小程序平台的特定能力，请参考文档后面的参数列表，更详细说明请参uni-app方文档：\
   [uni-app方button组件](https://uniapp.dcloud.io/component/button)
2. 由于微信小程序的限制，在微信小程序中设置了`form-type`的`u-button`无法触发`form`组件的`submit`事件(H5和APP正常)，详见微信小程序文档[Bug & Tip部分](https://developers.weixin.qq.com/miniprogram/dev/component/button.html)
   :::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

文字内容通过`slot`传入

```html
<u-button>月落</u-button>
```

## 设置按钮的主题

`type`值可选的有`default`(默认)、`primary`、`success`、`info`、`warning`、`error`

```html
<u-button >默认按钮</u-button>
<u-button type="primary">主要按钮</u-button>
<u-button type="success">成功按钮</u-button>
<u-button type="info">信息按钮</u-button>
<u-button type="warning">警告按钮</u-button>
<u-button type="error">危险按钮</u-button>
```

## 设置按钮为半圆形

`shape`默认值为`square`(按钮为圆角矩形)，设置为`circle`，则按钮两边为半圆形

```html
<u-button shape="square">乌啼</u-button>
```

## 设置尺寸

`button`组件的`size`（可选值为`default`(默认)，`mini`(小尺寸)和`medium`(中等尺寸)）

```html
<u-button size="default">江湖</u-button>
<u-button size="medium">夜雨</u-button>
<u-button size="mini">十年灯</u-button>
```

## 设置按钮的镂空状态

镂空状态按钮背景为白色，边框和文字同色，通过`plain`来设置

```html
<u-button plain>披荆</u-button>

<!-- 或者显式设置为true -->
<u-button :plain="true">斩棘</u-button>
```

## 设置点击按钮的水波纹效果

该效果通过给按钮绝对定位形式覆盖一个`view`，点击时改变`view`的`scale`，`opacity`样式属性，形成扩散再消失的水波纹效果。

```html
<u-button :ripple="true">十年</u-button>

<!-- 通过rippleBgColor设置水波纹的背景颜色 -->
<u-button :ripple="true" ripple-bg-color="#909399">之约</u-button>
```

## 如何修改按钮的样式

1. 针对非微信小程序平台，组件的根元素就是uni-app`button`组件，所以修改按钮的样式很容易，直接给组件定义`类名`或者嵌入`内联样式`即可。
2. 如果是微信小程序，编译后页面会有组件同名的元素存在，导致样式传递有问题。
3. 如果是为了修改按钮与其他元素之间的距离或者宽度等，可以给按钮外面套一个`view`元素，控制这个`view`与其他元素的距离或者宽度，即可达到同等效果。

所以：我们提供了一个`custom-style`参数，推荐用户可以用对象形式传递样式给组件内部，注意驼峰命名。

```html
<u-button class="custom-style">雪月夜</u-button>

<style scoped>
	:deep(.custom-style) {
		color: #606266;
		width: 400rpx;
	}
</style>


/* 也可以 */
<u-button :custom-style="customStyle">雪月夜</u-button>

<script setup lang="ts">
import { reactive } from 'vue'

const customStyle = reactive({
	marginTop: '20px', // 注意驼峰命名，并且值必须用引号包括，因为这是对象
	color: 'red'
})
</script>
```

## 各家小程序开放能力的对接

uView Pro已对接uni-app档关于[uni-app方button组件](https://uni-app.dcloud.io/component/button)的所有开放能力(截止2020-04-14)uni-app-app文档说明使用即可，如果有发现遗漏的地方，请加群反馈。

## API

## Props

|属性名|说明|类型|默认值|可选值|平台差异说明|
|:-|:-|:-|:-|:-|:-|
|size|按钮的大小|String|default|medium / mini|-|
|ripple|是否开启点击水波纹效果|Boolean|false|true|-|
|ripple-bg-color|水波纹的背景色，ripple为true时有效|String|rgba(0, 0, 0, 0.15)|-|-|
|type|按钮的样式类型|String|default|primary / success / info/ warning / error|-|
|plain|按钮是否镂空，背景色透明|Boolean|false|true|-|
|disabled|是否禁用|Boolean|false|true|-|
|hair-line|是否显示按钮的细边框|Boolean|true|false|-|
|shape|按钮外观形状，见上方说明|String|square|circle|-|
|loading|按钮名称前是否带 loading 图标|Boolean|false|true|App-nvue 平台，在 ios 上为雪花，Android上为圆圈|
|form-type|用于 `<form>` 组件，点击分别会触发 `<form>` 组件的 submit/reset 事件|String|-|submit / reset|-|
|open-type|开放能力|String|请参考uni-app方文档|-|-|
|hover-class|指定按钮按下去的样式类。当 hover-class="none" 时，没有点击态效果|String|button-hover|-|App-nvue 平台暂不支持|
|hover-start-time|按住后多久出现点击态，单位毫秒|String | Number|20|-|-|
|hover-stay-time|手指松开后点击态保留时间，单位毫秒|String | Number|150|-|-|
|app-parameter|打开 APP 时，向 APP 传递的参数，open-type=launchApp时有效|Boolean|false|true|微信小程序、QQ小程序|
|hover-stop-propagation|指定是否阻止本节点的祖先节点出现点击态|Boolean|false|true|微信小程序|
|lang|指定返回用户信息的语言，zh\_CN 简体中文，zh\_TW 繁体中文，en 英文|String|en|zh\_CN \ zh\_TW  |微信小程序|
|session-from|会话来源，open-type="contact"时有效|String|-|-|微信小程序|
|send-message-title|会话内消息卡片标题，open-type="contact"时有效|String|当前标题|-|微信小程序|
|send-message-path|会话内消息卡片点击跳转小程序路径，open-type="contact"时有效	|String|当前分享路径|-|微信小程序|
|send-message-img|会话内消息卡片图片，open-type="contact"时有效	|String|当前页面截图|-|微信小程序|
|show-message-card|是否显示会话内消息卡片，设置此参数为 true，用户进入客服会话会在右下角显示"可能要发送的小程序"提示，用户点击后可以快速发送小程序消息，open-type="contact"时有效|String|-|-|微信小程序|
|throttle-time| 节流的时间间隔(一定时间内无论点击多少次，只会触发一次`click`事件)，单位ms，详见[节流防抖](/zh/tools/debounce.html) |String | Number |0|-|-|

## Events

**说明**：目前经测试(Hbuilder X 2.6.8)，在H5，APP，可以直接对组件监听`tap`事件，等同组件内部发出的`click`事件效果，某些HX版本上，
微信小程序对组件使用`tap`事件可能无效，故建议对按钮组件的点击事件监听统一使用组件内部发出的`click`事件。

|属性名|说明|类型|默认值|可选值|平台差异说明|
|:-|:-|:-|:-|:-|:-|
|click|按钮点击，请勿使用`@tap`点击事件，微信小程序无效，返回值为点击事件及参数|Handler|-|
|getphonenumber|open-type="getPhoneNumber"时有效|Handler|微信小程序|
|getuserinfo|用户点击该按钮时，会返回获取到的用户信息，从返回参数的detail中获取到的值同uni.getUserInfo|Handler|微信小程序|
|error|当使用开放能力时，发生错误的回调|Handler|微信小程序|
|opensetting|在打开授权设置页并关闭后回调|Handler|微信小程序|
|launchapp|打开 APP 成功的回调|Handler|微信小程序|

---

---
url: 'https://uviewpro.cn/zh/components/calendar.md'
---
# Calendar 日历&#x20;

此组件用于单个选择日期，范围选择日期等，日历被包裹在底部弹起的容器中。

**注意：** 此组件与[Picker 选择器](/zh/components/picker.html)的日期选择模式有一定的重合之处，区别在于本组件为更专业的日期选择场景，能选择日期范围等。
另外`Picker`组件的日期模式可以配置更多的参数，如时、分、秒等，可以根据不同的使用场景进行选择。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`v-model`绑定一个布尔变量用于打开或收起日历弹窗。
* 通过`mode`参数指定选择单个日期，还是选择日期范围。

```html
<template>
	<view>
		<u-calendar v-model="show" :mode="mode"></u-calendar>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { CalendarMode } from 'uview-pro/types/global'

const show = ref(false)
const mode = ref<CalendarMode>('date')

</script>
```

## 日历模式

* `mode`为`date`只能选择单个日期
* `mode`为`range`可以选择日期范围

## 单个日期模式

选择日期后，需要点击底部的`确定`按钮才能触发回调事件，回调参数为一个对象，有如下属性：

```js
{
	day: 4, // 选择了哪一天
	days: 30, // 这个月份有多少天
	isToday: true, // 选择的日期是否今天
	month: 6, // 选择的月份
	result: "2020-06-04", // 选择的日期整体值
	week: "星期四", // 选择日期所属的星期数
	year: 2020 , // 选择的年份
}
```

示例代码：

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change"></u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('date')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>
```

## 日期范围模式

此模式用于选择一个日期范围，比如住酒店的入住到离店的日期范围，有如下可配置的参数：

* `active-bg-color`参数配置起始/结束日期按钮的背景色
* `active-color`参数配置起始/结束日期按钮的字体颜色
* `range-bg-color`参数配置起始/结束日期之间的区域的背景颜色，默认为`rgba(41,121,255,0.13)`，为浅蓝色
* `start-text`参数用于设置起始日期底部的提示文字，如"住店"
* `end-text`参数用于设置结束日期底部的提示文字，如"离店"

此模式的返回参数如下：

```js
{
	endDate: "2020-06-04", // 选择的结束日期
	endDay: 4, // 结束日期是哪一天
	endMonth: 6, // 结束日期的月份
	endWeek: "星期四", // 结束日期的星期数
	endYear: 2020, // 结束日期的年份
	startDate: "2020-06-01", // 选择的起始日期
	startDay: 1, // 起始日期是哪一天
	startMonth: 6, // 起始日期的月份
	startWeek: "星期一", // 起始日期的星期数
	startYear: 2020 // 起始日期的年份
}
```

示例代码：

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change"></u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('range')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>
```

## 显示农历模式&#x20;

支持农历选择和回调，配置的参数：

* `show-lunar`是否显示农历

单个日期模式的返回参数如下：

```js
{
	day: 4, // 选择了哪一天
	days: 30, // 这个月份有多少天
	isToday: true, // 选择的日期是否今天
	month: 6, // 选择的月份
	result: "2020-06-04", // 选择的日期整体值
	week: "星期四", // 选择日期所属的星期数
	year: 2020 , // 选择的年份
	lunar: { 
		dayCn: '十三', // 农历的日
        monthCn: '四月', // 农历的月
		weekCn: "星期四", // 选择日期所属的星期数
        day: '13', // 农历的日
        month: '4', // 农历的月
		week: 4, // 选择日期所属的星期数
        year: 2020 // 农历的年份
	},
}
```

日期范围模式的返回参数如下：

```js
{
	endDate: "2020-06-04", // 选择的结束日期
	endDay: 4, // 结束日期是哪一天
	endMonth: 6, // 结束日期的月份
	endWeek: "星期四", // 结束日期的星期数
	endYear: 2020, // 结束日期的年份
	startDate: "2020-06-01", // 选择的起始日期
	startDay: 1, // 起始日期是哪一天
	startMonth: 6, // 起始日期的月份
	startWeek: "星期一", // 起始日期的星期数
	startYear: 2020, // 起始日期的年份
	startLunar: { 
		dayCn: '初十',
        monthCn: '四月',
		weekCn: "星期一",
        day: '13',
        month: '4',
		week: 1,
        year: 2020
	},
	endLunar: { 
		dayCn: '十三',
        monthCn: '四月',
		weekCn: "星期四",
        day: '13',
        month: '4',
		week: 4,
        year: 2020
	},
}
```

示例代码：

```html
<template>
	<view>
		<u-calendar v-model="show" :mode="mode" :show-lunar="showLunar" @change="change"></u-calendar>
		<view>{{ result }}</view>
		<view>{{ lunarResult }}</view>
	</view>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const result = ref('')
const lunarResult = ref('')
const mode = ref<CalendarMode>('date')
const showLunar = ref(true)


function change(e: CalendarChangeRange | CalendarChangeDate) {
    if (mode.value === 'range') {
        const range = e as CalendarChangeRange;
        result.value = range.startDate + ' - ' + range.endDate;
        if (showLunar.value && range.startLunar && range.endLunar) {
            lunarResult.value = `${range.startLunar.monthCn ?? ''}${range.startLunar.dayCn ?? ''}` + ' - ' + `${range.endLunar.monthCn ?? ''}${range.endLunar.dayCn ?? ''}`;
        } else {
            lunarResult.value = '';
        }
    } else {
        const single = e as CalendarChangeDate;
        result.value = single.result;
        if (showLunar.value && single.lunar) {
            lunarResult.value = `${single.lunar.monthCn ?? ''}${single.lunar.dayCn ?? ''}`;
        } else {
            lunarResult.value = '';
        }
    }
}
</script>
```

## 自定义内容

组件有一个默认插槽，名为`tooltip`，传入的内容将会显示在键盘的顶部位置，如使用，需要为传入的内容自定义样式。

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change">
		<template #tooltip>
			<view class="title">
				请选择住店/离店时间
			</view>
		</template>
	</u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('range')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| mode | 选择日期的模式，date-为单个日期，range-为选择日期范围 | String | date | range |
| v-model | 布尔值变量，用于控制日历的弹出与收起 | Boolean | false | true |
| show-lunar | 是否显示农历 | Boolean | false | true |
| safe-area-inset-bottom | 是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明) | Boolean  | false | true |
| change-year | 是否显示顶部的切换年份方向的按钮  | Boolean | true | false |
| change-month | 是否显示顶部的切换月份方向的按钮  | Boolean | true | false |
| max-year | 可切换的最大年份 | Number | String | 2050 | - |
| min-year | 可切换的最小年份 | Number | String | 1950 | - |
| min-date | 最小可选日期 | Number | String | 1950-01-01 | - |
| max-date | 最大可选日期 | Number | String | 当前日期 | - |
| border-radius | 弹窗顶部左右两边的圆角值，单位rpx  | Number | String | 20 | - |
| mask-close-able | 是否允许通过点击遮罩关闭日历  | Boolean | true | false |
| month-arrow-color | 月份切换按钮箭头颜色 | String | #606266 | - |
| year-arrow-color | 年份切换按钮箭头颜色 | String | #909399 | - |
| color | 日期字体的默认颜色 | String | #303133 | - |
| active-bg-color | 起始/结束日期按钮的背景色 | String | #2979ff | - |
| z-index | 弹出时的`z-index`值 | String | Number | 10075 | - |
| active-color | 起始/结束日期按钮的字体颜色 | String | #ffffff | - |
| range-bg-color | 起始/结束日期之间的区域的背景颜色 | String | rgba(41,121,255,0.13) | - |
| range-color | 选择范围内字体颜色 | String | #2979ff | - |
| start-text | 起始日期底部的提示文字 | String | 开始 | - |
| end-text | 结束日期底部的提示文字 | String | 结束 | - |
| btn-type | 底部确定按钮的主题 | String | primary | default / success / info/ warning / error |
| toolTip | 顶部提示文字，如设置名为`tooltip`的`slot`，此参数将失效 | String | 选择日期 | - |
| closeable | 是否显示右上角的关闭图标 | Boolean | true | false |

## Slot

|名称|说明|
|:-|:-|
| tooltip | 自定义日历顶部的内容 |

## Event

|事件名|说明|回调参数|
|:-|:-|:-|
| change | 点击右上角`确定`按钮时触发 | 选择日期相关的返回参数 |

---

---
url: 'https://uviewpro.cn/zh/components/card.md'
---
# Card 卡片&#x20;

卡片组件一般用于多个列表条目，且风格统一的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

组件的头部信息可以通过参数配置，其他主体和底部的信息，需要通过`slot`传入。

* `title`配置标题
* `sub-title`配置副标题

```html
<template>
	<u-card :title="title" :sub-title="subTitle" :thumb="thumb">
		<template #body>
			<view class="u-body-item u-flex u-border-bottom u-col-between u-p-t-0">
				<view class="u-body-item-title u-line-2">瓶身描绘的牡丹一如你初妆，冉冉檀香透过窗心事我了然，宣纸上走笔至此搁一半</view>
				<image src="https://img11.360buyimg.com/n7/jfs/t1/94448/29/2734/524808/5dd4cc16E990dfb6b/59c256f85a8c3757.jpg" mode="aspectFill"></image>
			</view>
			<view class="u-body-item u-flex u-row-between u-p-b-0">
				<view class="u-body-item-title u-line-2">釉色渲染仕女图韵味被私藏，而你嫣然的一笑如含苞待放</view>
				<image src="https://img12.360buyimg.com/n7/jfs/t1/102191/19/9072/330688/5e0af7cfE17698872/c91c00d713bf729a.jpg" mode="aspectFill"></image>
			</view>
		</template>
		<template #foot>
			<u-icon name="chat-fill" size="34" color="" label="30评论"></u-icon>
		</template>
	</u-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const title = ref('素胚勾勒出青花，笔锋浓转淡')
const subTitle = ref('2020-05-15')
const thumb = ref('http://pic2.sc.chinaz.com/Files/pic/pic9/202002/hpic2119_s.jpg')
</script>

<style scoped lang="scss">
	.u-card-wrap { 
		background-color: $u-bg-color;
		padding: 1px;
	}
	
	.u-body-item {
		font-size: 32rpx;
		color: #333;
		padding: 20rpx 10rpx;
	}
		
	.u-body-item image {
		width: 120rpx;
		flex: 0 0 120rpx;
		height: 120rpx;
		border-radius: 8rpx;
		margin-left: 12rpx;
	}
</style>
```

## 配置卡片间距

可以通过`margin`参数配置卡片与屏幕左右的边距，以及上下卡片之间的距离，如: `20rpx 30rpx`、`20rpx 30rpx 30rpx 20rpx`。\
注意：当设置`full`参数为`true`的时候，也就是卡片占据屏幕总宽度的时候，通过`margin`配置的左右边距会失效。

```html
<u-card margin="30rpx"></u-card>
```

## 配置卡片左上角的缩略图

这个缩略图是可选的，显示在卡片的左上角位置，如果配置了`thumb`参数(图片路径)，就会显示图片。

* `thumb`缩略图路径
* `thumb-width`缩略图宽度，高等于宽
* `thumb-circle`缩略图是否为圆形

```html
<u-card thumb="xxx.jpg" thumb-width="60"></u-card>
```

## 配置卡片边框

这里说的边框，有3个：

* `border`配置是否显示整个卡片的外边框
* `head-border-bottom`配置是否显示卡片内部头部的下边框
* `foot-border-top`配置是否显示卡片内部底部的上边框

```html
<u-card :border="false" :foot-border-top="false"></u-card>
```

## 设置内边距

默认下，卡片内部的头部，主体，底部都有一个内边距，可以通过配置`padding`参数去覆盖：

```html
<u-card padding="30"></u-card>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| full | 卡片与屏幕两侧是否留空隙  | Boolean | fasle | true |
| title | 头部左边的标题  | String	 | - | - |
| title-color | 标题颜色 | String  | #303133 | - |
| title-size | 标题字体大小，单位rpx | String | Number  | 30 | - |
| sub-title | 头部右边的副标题 | String  | - | - |
| sub-title-color | 副标题颜色 | String  | #909399 | - |
| sub-title-size | 副标题字体大小 | String | Number  | 26 | - |
| border | 是否显示边框 | Boolean  | true | false |
| index | 用于标识点击了第几个卡片 | String | Number  | - | - |
| margin | 卡片与屏幕两边和上下元素的间距，需带单位，如"30rpx 20rpx"，见上方说明 | String  | 30rpx | - |
| border-radius | 卡片整体的圆角值，单位rpx | String | Number  | 16 | - |
| head-style | 头部自定义样式，对象形式 | Object  | - | - |
| body-style | 主体自定义样式，对象形式 | Object  | - | - |
| foot-style | 底部自定义样式，对象形式 | Object  | - | - |
| head-border-bottom | 是否显示头部的下边框 | Boolean  | true | false |
| foot-border-top | 是否显示底部的上边框 | Boolean  | true | false |
| thumb | 缩略图路径，如设置将显示在标题的左边，不建议使用相对路径 | String  | - | - |
| thumb-width | 缩略图的宽度，高等于宽，单位rpx | String | Number  | 60 | - |
| thumb-circle | 缩略图是否为圆形 | Boolean  | false | true |
| padding | 给head，body，foot部的内边距，见上方说明，单位rpx | String | Number  | 30 | - |
| show-head | 是否显示头部 | Boolean  | true | false |
| show-foot | 是否显示尾部 | Boolean  | true | false |
| box-shadow | 卡片外围阴影，字符串形式 | String  | none | - |

## Slot

| 名称          | 说明            |
|-------------  |---------------- |
| default  | 同 body 插槽 |
| head | 自定义卡片头部内容  |
| body | 自定义卡片主体部分内容 |
| foot | 自定义卡片底部部分内容 |

## Event

|事件名|说明|回调参数|
|:-|:-|:-|
| click | 整个卡片任意位置被点击时触发 | index: 用户传递的标识符 |
| head-click | 卡片头部被点击时触发 | index: 用户传递的标识符 |
| body-click | 卡片主体部分被点击时触发 | index: 用户传递的标识符 |
| foot-click | 卡片底部部分被点击时触发 | index: 用户传递的标识符 |

---

---
url: 'https://uviewpro.cn/zh/components/cell.md'
---
# Cell 单元格&#x20;

cell单元格一般用于一组列表的情况，比如个人中心页，设置页等。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 该组件需要搭配`cell-group`使用，并由它实现列表组的上下边框，如不需要上下边框，配置`cellGroup`的`border`参数为`false`即可。
* 通过`title`设置左侧标题，`value`设置右侧内容。
* 通过`icon`字段设置图标，值为uView自带的[Icon 图标](/zh/components/icon.html)名。

**注意：** 由于`cell`组件需要由`cellGroup`组件提供参数值，这些父子组件间通过Vue的"provide/inject"特性注入依赖，
所以您必须使用`cellGroup`包裹`cell`组件才能正常使用。

```html
<template>
	<u-cell-group>
		<u-cell-item icon="setting-fill" title="个人设置"></u-cell-item>
		<u-cell-item icon="integral-fill" title="会员等级" value="新版本"></u-cell-item>
	</u-cell-group>
</template>
```

## 自定义内容

* 通过插槽`icon`可以自定义图标，内容会替换左边图标位置
* 通过插槽`title`定义左边标题部分
* 通过插槽`right-icon`定义右边内容部分

```html
<u-cell-group>
	<u-cell-item  title="夕阳无限好" arrow-direction="down">
		<template #icon>
			<u-icon size="32" name="search"></u-icon>
		</template>
		<template #right-icon>
			<u-switch v-model="checked"></u-switch>
		</template>
	</u-cell-item>
	<u-cell-item icon="setting-fill" title="只是近黄昏"></u-cell-item>
</u-cell-group>
```

如上所示，可以给`cell-item`组件通过`<template #right-icon></template>`设定右边uView自带的`badge`或者`switch`组件：

* 如果搭配的是`badge`组件，注意设置`absolute`参数为`false`去掉绝对定位，否则其位于右侧的恰当位置，详见[Badge 徽标数](/zh/components/badge.html)。
* 如果搭配的是`switch`组件，注意要通过`v-model`绑定一个内容为布尔值的变量，否则无法操作`switch`，详见[Switch 开关选择器](/zh/components/switch.html)。

## 展示右箭头

设置`arrow`为`true`，将会显示右侧的箭头，可以通过arrow-direction控制箭头的方向

```html
<u-cell-group>
	<u-cell-item icon="share" title="停车坐爱枫林晚" :arrow="true" arrow-direction="down"></u-cell-item>
	<u-cell-item icon="map" title="霜叶红于二月花" :arrow="false"></u-cell-item>
</u-cell-group>
```

## 分组标题

通过`cell-group`的`title`参数可以指定分组标题

```html
<u-cell-group title="设置喜好">
	<u-cell-item icon="setting-fill" title="个人设置"></u-cell-item>
	<u-cell-item icon="integral-fill" title="会员等级" value="新版本"></u-cell-item>
</u-cell-group>
```

## 是否开启点击反馈

如果将`arrow`参数设置为`true`，意味着这是一个可点击的Cell，默认会给一个点击的反馈效果，如果您想自定义这个反馈效果，可以通过
`hover-class`参数传入一个样式类名，这个类必须写在全局样式中，如`App.vue`、或通过`Apop.vue`引入的全局样式中，一般建议定义反馈的背景颜色，或者是透明度即可。
如果不想要任何效果，将`hover-class`设置为`none`即可。

```html
<u-cell-group title="设置喜好">
	<u-cell-item icon="setting-fill" title="个人设置" hover-class="cell-hover-class"></u-cell-item>
</u-cell-group>
```

```css
/* App.vue */
.cell-hover-class {
	background-color: rgb(235, 237, 238);
}

/* 或者单是设置透明度 */
.cell-hover-class {
	opacity: 0.5;
}
```

## API

## CellGroup Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| title | 分组标题  | String | - | - |
| border | 是否显示外边框 | Boolean  | true | false |
| title-style | 分组标题的的样式，对象形式，如`{'font-size': '24rpx'}` 或 `{'fontSize': '24rpx'}` | object  | - | - |

## CellItem Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| title | 左侧标题  | String | - | - |
| icon | 左侧图标名，只支持uView内置图标，见[Icon 图标](/zh/components/icon.html) | String  | - | - |
| icon-style | icon的样式，对象形式 | Object | - | - |
| value | 右侧内容 | String  | - | - |
| label | 标题下方的描述信息 | String | - | - |
| border-bottom | 是否显示cell的下边框 | Boolean  | true | false |
| border-top | 是否显示cell的上边框 | Boolean  | false | true |
| border-gap | `border-bottom`为`true`时，Cell列表中间的条目的下边框是否与左边有一个间隔   | Boolean  | true | false |
| hover-class | 是否开启点击反馈，`none`为无效果，见上方说明 | String  | - | none |
| arrow | 是否显示右侧箭头，开启的话，将会默认带上点击反馈，可通过`hover-class`配置 | Boolean | true | false |
| arrow-direction | 箭头方向，可选值为 | String  | right | up / down |
| title-style | 标题样式，对象形式 | Object | - | - |
| required | 是否显示左边表示必填的星号 | Boolean | false | true |
| value-style | 右侧内容样式，对象形式 | Object | - | - |
| label-style | 标题下方描述信息的样式，对象形式 | Object | - | - |
| bg-color | 背景颜色，默认透明背景 | String  | transparent | - |
| index | 用于在`click`事件回调中返回，标识当前是第几个Item  | String | Number | - | - |
| title-width | 标题的宽度，单位rpx | Number | String | - | - |
| icon-size | 左边通过`icon`参数传入的图标的大小，单位rpx | Number | String | 34 | - |
| center | 是否使内容垂直居中 | Boolean | false | true |

## CellItem Slot

| 名称          | 说明            |
|-------------  |---------------- |
| title | 自定义左侧标题部分的内容，如需使用，请勿定义`title`参数，或赋值`null`即可  |
| icon | 自定义左侧的图标 |
| right-icon | 自定义右侧图标内容，需设置`arrow`为`false`才起作用 |
| label | 自定义`label`内容，需同时设置`use-label-slot`为`true` |

## CellItem Event

|事件名|说明|回调参数|
|:-|:-|:-|
| click | 点击cell列表时触发 | index: 通过`props`传递的`index`参数 |

---

---
url: 'https://uviewpro.cn/zh/components/checkbox.md'
---
# Checkbox 复选框&#x20;

复选框组件一般用于需要多个选择的场景，该组件功能完整，使用方便

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 该组件无需强制搭配`checkboxGroup`组件使用(视情况而定)，可以单个独立使用`u-checkbox`组件
* 通过`v-model`给`checkbox`绑定一个变量，这个绑定的变量是双向的(初始值只能是`true`或者`false`)，也就是说，您可以无需监听`checkbox`或者`checkboxGroup`组件的`change`事件，也能知道哪个复选框
  被勾选了

```html
<template>
	<view class="">
		<u-checkbox-group @change="checkboxGroupChange">
			<u-checkbox 
				@change="checkboxChange" 
				v-model="item.checked" 
				v-for="(item, index) in list" :key="index" 
				:name="item.name"
			>{{item.name}}</u-checkbox>
		</u-checkbox-group>
		<u-button @click="checkedAll">全选</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface CheckboxItem {
  name: string
  checked: boolean
  disabled: boolean
}

const list = reactive<CheckboxItem[]>([
  {
    name: 'apple',
    checked: false,
    disabled: false
  },
  {
    name: 'banner',
    checked: false,
    disabled: false
  },
  {
    name: 'orange',
    checked: false,
    disabled: false
  }
])

// 选中某个复选框时，由checkbox时触发
const checkboxChange = (e: any) => {
  //console.log(e);
}

// 选中任一checkbox时，由checkbox-group触发
const checkboxGroupChange = (e: any) => {
  // console.log(e);
}

// 全选
const checkedAll = () => {
  list.map(val => {
    val.checked = true;
  })
}
</script>
```

## 禁用checkbox

设置`disabled`为`true`，即可禁用某个组件，让用户无法点击，禁用分为两种状态，一是未勾选前禁用，这时只显示一个灰色的区域。二是已勾选后
再禁用，会有灰色的已勾选的图标，但此时依然是不可操作的。

```html
<u-checkbox-group>
	<u-checkbox v-model="checked" :disabled="false">天涯</u-checkbox>
</u-checkbox-group>
```

## 自定义形状

可以通过设置`shape`为`square`或者`circle`，将复选框设置为方形或者圆形

```html
<u-checkbox-group>
	<u-checkbox v-model="checked" shape="circle">明月</u-checkbox>
</u-checkbox-group>
```

## 自定义颜色

此处所指的颜色，为`checkbox`选中时的背景颜色，参数为`active-color`

```html
<u-checkbox-group>
	<u-checkbox v-model="checked" active-color="red">光影</u-checkbox>
</u-checkbox-group>
```

## 文本是否可点击

设置`label-disabled`为`false`，点击文本时，无法操作`checkbox`

```html
<u-checkbox-group>
	<u-checkbox v-model="checked" :label-disabled="false">剑舞</u-checkbox>
</u-checkbox-group>
```

## API

## Checkbox Props

注意：需要给`checkbox`组件通过`v-model`绑定一个**布尔值**，来初始化`checkbox`的状态，随后该值被双向绑定，
当用户勾选复选框时，该值在`checkbox`内部被修改为`true`，并反映到父组件，否则为`false`，换言之，您无需监听`checkbox`的`change`事件，也能
知道某一个`checkbox`是否被选中的状态

注意：`checkbox`和`checkbox-group`二者同名参数中，`checkbox`的参数优先级更高。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 双向绑定某一个`checkbox`的值，如果将该变量设置为`true`，将会被选中 | String \ Number | - | - |
| size | 组件整体的大小，单位rpx  | String \ Number | - | - |
| label-size | label字体大小，单位rpx  | String \ Number | - | - |
| icon-size | 图标大小，单位rpx  | String \ Number | - | - |
| name | `checkbox`组件的标示符  | String \ Number | - | - |
| shape | 形状，见上方说明 | String  | - | square |
| disabled | 是否禁用 | Boolean  | - | false / true |
| label-disabled | 是否禁止点击文本操作`checkbox` | Boolean  | - | false / true |
| active-color | 选中时的颜色，如设置`CheckboxGroup`的`active-color`将失效 | String  | - | - |

## CheckboxGroup Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| max | 最多能选中多少个`checkbox`  | String \ Number | 999 | - |
| disabled | 是否禁用所有`checkbox`  | Boolean | false | true |
| icon-size | 图标大小，单位rpx  | String \ Number | 20 | - |
| size | 组件整体的大小，单位rpx  | String \ Number | 34 | - |
| shape | 形状，见上方说明 | String  | circle | square |
| active-color | 选中时的颜色，应用到所有子`Checkbox`组件 | String  | #2979ff | - |
| label-disabled | 是否禁止点击文本操作`checkbox` | Boolean  | false | true |
| width | `checkbox`的宽度，需带单位，如`50%`，`150rpx` | String  | auto | - |
| wrap | 是否每个`checkbox`占一行 | Boolean  | false | true |

## Checkbox Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 某个`checkbox`状态发生变化时触发，回调为一个对象 | detail = {value: \[true或者false，true为被选中，否则反之], name: \[通过props传递的`name`参数] } | - |

## CheckboxGroup Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 任一个`checkbox`状态发生变化时触发，回调为一个对象 | detail = array( \[元素为被选中的`checkbox`的`name`] ) | - |

---

---
url: 'https://uviewpro.cn/zh/components/circleProgress.md'
---
# CircleProgress 圆形进度条&#x20;

展示操作或任务的当前进度，比如上传文件，是一个圆形的进度环。

## 内部实现

组件内部通过`canvas`实现，有更好的性能和通用性。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`percent`设置当前的进度值，该值区间为0-100
* 通过`active-color`设置圆环的颜色，也可以直接设置`type`主题颜色，使用预置值
* 通过默认`slot`传入内容，将会显示在圆环的内部

```html
<template>
	<u-circle-progress active-color="#2979ff" :percent="80">
		<view class="u-progress-content">
			<view class="u-progress-dot"></view>
			<text class='u-progress-info'>查找中</text>
		</view>
	</u-circle-progress>
</template>

<style lang="scss" scoped>
	.u-progress-content {
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.u-progress-dot {
		width: 16rpx;
		height: 16rpx;
		border-radius: 50%;
		background-color: #fb9126;
	}
	
	.u-progress-info {
		font-size: 28rpx;
		padding-left: 16rpx;
		letter-spacing: 2rpx
	}
</style>
```

## 设置圆环的动画时间

通过`duration`设置圆环从0递增到100%(也即一圆周)所需的时间，如需动态修改进度值时会用到，比如用户进行某一个操作之后，
需要把进度值从30%改为80%，这里增加了50%(80% - 30% = 50%)，也即半个圆周，所需时间为`duration`的一半，因为`duration`值为一个圆周的时间。

```html
<u-circle-progress type="primary" :percent="30" duration="2000"></u-circle-progress>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| percent | 圆环进度百分比值，为数值类型，0-100  | String | Number | - | - |
| inactive-color | 圆环的底色，默认为灰色(该值无法动态变更) | String  | #ececec | - |
| active-color | 圆环激活部分的颜色(该值无法动态变更) | String  | #19be6b | - |
| width | 整个圆环组件的宽度，高度默认等于宽度值，单位rpx | String | Number  | 200 | - |
| border-width | 圆环的边框宽度，单位rpx | String | Number  | 14 | - |
| duration | 整个圆环执行一圈的时间，单位ms | String | Number  | 1500 | - |
| type | 如设置，`active-color`值将会失效 | String  | - | success / primary / error / info / warning |
| bg-color | 整个组件背景颜色，默认为白色 | String  | #ffffff | - |

---

---
url: 'https://uviewpro.cn/zh/components/collapse.md'
---
# Collapse 折叠面板&#x20;

通过折叠面板收纳内容区域

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

默认为手风琴模式，即打开一个，另外所有的都会关闭。可以将`u-collapse`的`accordion`设置为`false`，这样可以允许打开多个面板

```html
<template>
	<u-collapse>
		<u-collapse-item :title="item.head" v-for="(item, index) in itemList" :key="index">
			{{item.body}}
		</u-collapse-item>
	</u-collapse>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

interface CollapseItem {
  head: string
  body: string
  open?: boolean
  disabled?: boolean
}

const itemList = reactive<CollapseItem[]>([{
  head: "赏识在于角度的转换",
  body: "只要我们正确择取一个合适的参照物乃至稍降一格去看待他人，值得赏识的东西便会扑面而来",
  open: true,
  disabled: true
}, {
  head: "生活中不是缺少美，而是缺少发现美的眼睛",
  body: "学会欣赏，实际是一种积极生活的态度，是生活的调味品，会在欣赏中发现生活的美",
  open: false,
}, {
  head: "周围一些不起眼的人、事、物，或许都隐藏着不同凡响的智慧",
  body: "但是据说雕刻大卫像所用的这块大理石，曾被多位雕刻家批评得一无是处，有些人认为这块大理石采凿得不好，有些人嫌它的纹路不够美",
  open: false,
}])
</script>
```

## 控制面板的初始状态，以及是否可以操作

* 设置`u-collapse-item`的`open`参数为`true`，可以让面板初始化时为打开状态
* 如果设置`u-collapse-item`的`disabled`参数为`true`，那么面板会保持初始状态，无法关闭或打开

```html
<template>
	<u-collapse>
		<u-collapse-item :title="item.head" v-for="(item, index) in itemList" :key="index" :open="item.open" :disabled="item.disabled">
			{{item.body}}
		</u-collapse-item>
	</u-collapse>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

interface CollapseItem {
  head: string
  body: string
  open?: boolean
  disabled?: boolean
}

const itemList = reactive<CollapseItem[]>([{
  head: "赏识在于角度的转换",
  body: "只要我们正确择取一个合适的参照物乃至稍降一格去看待他人，值得赏识的东西便会扑面而来",
  open: true,
  disabled: true
}, {
  head: "生活中不是缺少美，而是缺少发现美的眼睛",
  body: "学会欣赏，实际是一种积极生活的态度，是生活的调味品，会在欣赏中发现生活的美",
  open: false,
}, {
  head: "周围一些不起眼的人、事、物，或许都隐藏着不同凡响的智慧",
  body: "但是据说雕刻大卫像所用的这块大理石，曾被多位雕刻家批评得一无是处，有些人认为这块大理石采凿得不好，有些人嫌它的纹路不够美",
  open: false,
}])
</script>
```

## 自定义样式

在此组件中，可以通过多个方式对每个`Item`进行样式定义，我们可以从如下方面思考和着手：

### 1. 如果修改展开后的内容？

* 因为是通过默认的`slot`传入的(见上方示例)，我们可以加一个`view`元素当做外层，在父组件给它添加样式，如下：

```html
<template>
	<u-collapse :item-style="itemStyle" event-type="close" :arrow="arrow" :accordion="accordion" @change="change">
		<u-collapse-item :index="index" @change="itemChange" :title="item.head" v-for="(item, index) in itemList" :key="index">
			<view class="collapse-item">
				{{item.body}}
			</view>
		</u-collapse-item>
	</u-collapse>
</template>

<style scoped>
	.collapse-item {
		color: red;
		padding-bottom: 10px;
	}
</style>
```

* 通过`Collapse`的`body-style`参数也可以配置主体内容的样式，需要注意上面的自定义`slot`内容如果在父组件定义了样式，会优先起作用。

### 2. 如何自定义标题的样式？

如果想修改头部标题的字体大小，颜色等，可以通过`head-style`参数修改。

### 3. 如何修改整个`Item`的样式？

有时候我们需要修改`Item`的整体样式，比如将各个`Item`之间隔开，这时我们可以通过`item-style`参数进行设置，比如：

```html
<template>
	<u-collapse :item-style="itemStyle">
		......
	</u-collapse>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const itemStyle = reactive({
	marginTop: '20px'
})
</script>
```

## API

## Collapse Props

|参数|说明|类型|默认值|可选值|
|---|---|---|---|---|
|accordion|是否手风琴模式|Boolean|true|false|
|arrow|是否显示标题右侧的箭头|Boolean|true|false|
|arrow-color|标题右侧箭头的颜色|String|#909399|-|
|item-style|整个`Item`的自定义样式，对象形式|Object|-|-|
|head-style|`Item`的标题自定义样式，对象形式|Object|-|-|
|body-style|`Item`的主体自定义样式，对象形式|Object|-|-|
|hover-class|样式类名，按下时有效，样式必须写在根目录的`App.vue`或通过其引入的全局样式中才有效，`none`为无效果，作用于头部标题区域|String|u-hover-class|none/其他|

## Collapse Item Props

|参数|说明|类型|默认值|可选值|
|---|---|---|---|---|
|title|面板标题|String|-|-|
|index|主要用于事件的回调，标识那个Item被点击|String/Number|-|-|
|disabled|面板是否可以打开或收起|Boolean|false|true|
|open|设置某个面板的初始状态是否打开|Boolean|false|true|
|name|唯一标识符，如不设置，默认用当前`collapse-item`的索引值|String/Number|-|-|
|align|标题的对齐方式|String|left|-|
|active-style|不显示箭头时，可以添加当前选择的collapse-item活动样式，对象形式|Object|-|-|

## Collapse Event

注意：请在`<u-collapse></u-collapse>`上监听此事件

|事件名|说明|回调参数|
|---|---|---|
|change|当前激活面板展开时触发(如果是手风琴模式，参数activeNames类型为String，否则为Array)|activeNames: String/Array|

## Collapse Item Event

注意：请在`<u-collapse-item></u-collapse-item>`上监听此事件

|事件名|说明|回调参数|
|---|---|---|
|change|某个item被打开或者收起时触发|对象，{index: index, show: true|false}，index为`collapse-item`的`index`参数，show为`true`表示被打开，`false`表示被收起|

## Collapse Methods

注意：此方法需要通过`ref`调用

|方法|说明|
|---|---|
|init|重新初始化内部高度计算，用于异步获取内容的情形，请结合`nextTick()`使用|

## Slot

|名称|说明|
|---|---|
|-|主体部分的内容|
|title|头部的内容，不含右边的箭头|
|title-all|整个头部的内容，包含右边的箭头|

---

---
url: 'https://uviewpro.cn/zh/components/color.md'
---
# Color 色彩

uView经过大量调试和研究，得出一套专有的调色板，在各个组件内部，使用统一的配色，为您的产品带来统一又鲜明的视觉效果。

::: danger 注意
uView为了更好编写css，使用了scss预处理器，使用uView之前，请确认您的Hbuilder X已经安装了scss预处理器，一般情况下，相信您已经安装了。如果没有安装，
请在 Hbuilder X->工具->插件安装 中找到找到"scss/sass编译"安装即可，安装完毕如果不生效，请重启Hbuilder X。
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 主题色

`primary`，`success`，`error`，`warning`，`info`是uView的主题色，他们给人在视觉感受上分别对应于蓝色，绿色，红色，黄色，灰色。
而他们又有对应的`disabled`、`dark`和`light`状态，分别表示对应的禁止，加深和变浅的对应颜色。举例uView的`button`组件来说：

1. 设置`type`参数为`primary`时，按钮显示蓝色。
2. 按钮被按下时，使用的是`primary`的加深颜色，也即`dark`状态。
3. 按钮设置为镂空状态(`plain`为`true`)时，背景色为`primary`的变浅颜色，也即`light`状态。
4. 按钮处于禁止状态时，使用的是`primary`的稍浅颜色，也即`disabled`状态。

## 主色

蓝色作为uView主色调，表示一种鲜明，积极的态度

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这些变量，如下：

```css
/* 变量的定义，该部分uView已全局引入，无需您编写 */
$u-type-primary: #2979ff;
$u-type-primary-light: #ecf5ff;
$u-type-primary-disabled: #a0cfff;
$u-type-primary-dark: #2b85e4;


/* 在您编写css的地方使用这些变量 */
.title {
	color: $u-type-primary;
	......
}
```

## 辅助色

除了主色外的场景色，需要在不同的场景中使用，如绿色代表成功，红色代表错误，黄色代表警示。

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这些变量，如下：

```css
/* 变量的定义，该部分uView已全局引入，无需您编写 */

$u-type-warning: #ff9900;
$u-type-warning-disabled: #fcbd71;
$u-type-warning-dark: #f29100;
$u-type-warning-light: #fdf6ec;

$u-type-success: #19be6b;
$u-type-success-disabled: #71d5a1;
$u-type-success-dark: #18b566;
$u-type-success-light: #dbf1e1;

$u-type-error: #fa3534;
$u-type-error-disabled: #fab6b6;
$u-type-error-dark: #dd6161;
$u-type-error-light: #fef0f0;

$u-type-info: #909399;
$u-type-info-disabled: #c8c9cc;
$u-type-info-dark: #82848a;
$u-type-info-light: #f4f4f5;

/* 在您编写css的地方使用这些变量 */
.title {
	color: $u-type-info;
	......
}
```

## 文字颜色

uView中，分别提炼了4种用于文字颜色，分别是：主要文字、常规文字、次要文字、占位文字颜色。

* 主要文字颜色一般用于内容的标题等，如新闻列表的标题
* 常规文字颜色一般用于内容的主体，如新闻列表的概要
* 次要文字颜色一般用于内容的提示部分，如新闻列表底部的时间，评论数量的提示文字
* 占位文字颜色属于更浅的灰色，看场景选择使用

```css
/* 变量的定义，该部分uView已全局引入，无需您编写 */
$u-main-color: #303133;
$u-content-color: #606266;
$u-tips-color: #909399;
$u-light-color: #c0c4cc;

/* 在您编写css的地方使用这些变量 */
.title {
	color: $u-main-color;
}
```

## 背景颜色

uView中，定义了一个背景颜色，如下：

我们在全局样式中，通过`scss`提供了对应的颜色变量名，方便您在任何可写css的地方，调用这个变量，如下：

```css
/* 变量的定义，该部分uView已全局引入，无需您编写 */
$u-bg-color: #f3f4f6;

/* 在您编写css的地方使用这些变量 */
.title {
	color: $u-bg-color;
}
```

## 边框颜色

uView自定义了一个边框的颜色，值为`#e4e7ed`，如果想使用，如下：

```css
/* 变量的定义，该部分uView已全局引入，无需您编写 */
$u-border-color: #e4e7ed;

/* 在您编写css的地方使用这个变量 */
.item {
	border: 1px solid $u-border-color;
}
```

---

---
url: 'https://uviewpro.cn/zh/tools/color.md'
---
# color 颜色值

此功能为uView内部通过js提供的一些颜色值，可以用于通过js修改元素字体，背景颜色等一些场景，常用于uView的各个组件中。\
这些颜色值，挂载在`$u`对象下的`color`数组中，关于这些颜色值的具体描述，详见[Color 色彩](/zh/components/color.html)\
使用方法：如使用`primary`颜色值，方法为：`$u.color['primary']`

**说明**：这些通过JS调用的颜色值，也是能通过CSS调用的，二者等价。详见[Color 色彩](/zh/components/color.html)

## 主题颜色

该主题颜色值，一共有5个，分别是`primary`、`error`、`success`、`info`、`warning`

```js
import { ref, onMounted } from 'vue';

const errorColor = ref('');

onMounted(() => {
  errorColor.value = uni.$u.color['error'];
});
```

## 文字颜色

uView一共提供了四个颜色值，具体请见组件部分[Color色彩](/zh/components/color.html)\
分别有：`mainColor`、`contentColor`、`tipsColor`、`lightColor`、`borderColor`(边框颜色值)

```js
console.log(uni.$u.color['contentColor']);
```

## 背景颜色

uView提供了一个浅灰的背景颜色值，该值为`#f3f4f6`

```js
console.log(uni.$u.color['bgColor']);
```

---

---
url: 'https://uviewpro.cn/zh/tools/colorSwitch.md'
---
# colorSwitch 颜色转换

## RGB转十六进制Hex

### rgbToHex(rgb)

该函数可以将一个RGB颜色值转换成一个Hex的十六进制颜色值

* `rgb` \<String> RGB颜色值，如`rgb(230, 231, 233)`

```js
import { ref, onMounted } from 'vue';
import { $u } from 'uview-pro';

const rgb = ref('rgb(13, 145, 20)');

onMounted(() => {
  console.log($u.rgbToHex(rgb.value));
});
```

## 十六进制Hex转RGB

### hexToRgb(hex)

该函数可以将一个Hex的十六进制颜色值转换成一个RGB颜色值

* `hex` \<String> HEx颜色值，如`#0afdce`

```js
import { ref, onMounted } from 'vue';
import { $u } from 'uview-pro';

const hex = ref('#0afdce');

onMounted(() => {
  console.log($u.hexToRgb(hex.value));
});
```

## 颜色渐变

### colorGradient(startColor, endColor, step)

该函数实现两个颜色值之间等分取值，返回一个数组，元素为十六进制形式的颜色值，数组长度为`step`值。
例如：colorGradient('rgb(250, 250, 250)', 'rgb(252, 252, 252)', 3)，得到的结果为\["#fafafa", "#fafafa", "#fbfbfb"]

* `startColor` \<String> 开始颜色值，可以是HEX或者RGB颜色值，如`#0afdce`或者`rgb(120, 130, 150)`
* `endColor` \<String> 结束颜色值，可以是HEX或者RGB颜色值，如`#0afdce`或者`rgb(120, 130, 150)`
* `step` \<Number> 均分值，把开始值和结束值平均分成多少份

```js
console.log(uni.$u.colorGradient('rgb(250,250,250)', 'rgb(252,252,252)', 3));
// 结果为：["#fafafa", "#fafafa", "#fbfbfb"]
```

## 颜色透明度

### colorToRgba(color, opacity = 0.3)

该函数可以接受一个`十六进制`或者`rgb`格式的颜色值(不能接受命名式颜色格式，比如`white`)，返回此颜色的`rgba`格式值，如下：

* `color` \<String> 颜色值，只能`hex`或者`rgba`格式
* `opacity` \<Number> 不透明度值，取值为0-1之间

```js
uni.$u.colorToRgba('#000000', 0.35);
// 结果为 rgba(0, 0, 0, 0.35)

uni.$u.colorToRgba('rgb(255, 180, 0)', 0.4);
// 结果为 rgba(255, 180, 0, 0.4)
```

---

---
url: 'https://uviewpro.cn/zh/components/configProvider.md'
---
# ConfigProvider 全局配置 &#x20;

`u-config-provider` 是 uView Pro 主题系统的唯一入口组件，负责把 `useTheme` 维护的 CSS 变量注入到页面，同时向外抛出主题与暗黑模式变更事件。本文档面向业务开发者，介绍其用法、属性与常见场景。

## 监听主题切换

> 需要配合虚拟根组件(`uni-ku-root`) 来做全局共享

### 安装

::: code-group

```bash [npm]
npm i -D @uni-ku/root
```

```bash [yarn]
yarn add -D @uni-ku/root
```

```bash [pnpm]
pnpm add -D @uni-ku/root
```

:::

### 引入

* CLI项目: 直接编辑 根目录下的 vite.config.(js|ts)
* HBuilderX项目: 需要在根目录下 创建 vite.config.(js|ts)

```ts
// vite.config.(js|ts)

import { defineConfig } from 'vite'
import UniKuRoot from '@uni-ku/root'
import Uni from '@dcloudio/vite-plugin-uni'

export default defineConfig({
  plugins: [
    // ...plugins
    UniKuRoot(),
    Uni()
  ]
})
```

:::tip
若存在改变 pages.json 的插件，需要将 UniKuRoot 放置其后
:::

### 使用

1. 创建根组件并处理全局配置组件

* CLI项目: 在 **src** 目录下创建下 App.ku.vue
* HBuilderX项目: 在 **根** 目录下创建 App.ku.vue

:::tip
在 App.ku.vue 中标签 `<KuRootView />` 代表指定视图存放位置
:::

## 基本用法

```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
import { computed } from 'vue';

const { darkMode, themes, currentTheme } = useTheme();

const themeName = computed(() => currentTheme.value?.name);
</script>

<template>
  <u-config-provider :dark-mode="darkMode" :current-theme="themeName" :themes="themes">
    <KuRootView />
  </u-config-provider>
</template>
```

* 建议在应用的最外层（如 `App.ku.vue`）直接包裹整个视图，保证所有子组件都能拿到最新的 CSS 变量。
* `darkMode` 默认是 `Ref<'light' | 'dark' | 'auto'>`，直接透传即可；组件内部会依赖 `useTheme` 自动切换类名 `u-theme-light / u-theme-dark`。

## API

## Props

| Prop | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `themes` | `Theme[]` | `[]` | 可选。用于在运行时（如远程拉取主题）重新初始化主题列表，通常不需要手动传入。 |
| `currentTheme` | `string` | `''` | 可选。强制切换到指定主题名；当你希望父级受控时使用。 |
| `darkMode` | `'light' \| 'dark' \| 'auto'` | `'auto'` | 推荐配合 `useTheme().darkMode`，也可以手动传值。 |
| `customStyle` | `Record<string, any> \| string` | `{}` | 可选。追加到根节点上的样式，会与系统注入的 CSS 变量合并。 |
| `customClass` | `string` | `''` | 可选。自定义外层样式类名。 |

> 当 `themes` 已通过插件初始化后，`u-config-provider` 会跳过重复初始化，仅根据 props 调整当前主题/模式，因此可以安心地多次挂载（例如微前端场景）。

## Events

| 事件 | 回调参数 | 触发时机 |
| --- | --- | --- |
| `theme-change` | `(themeName: string)` | 全局主题被切换时（包括 `setTheme`、外部传入 `currentTheme`）。 |
| `mode-change` | `(mode: 'light' \| 'dark')` | 暗黑渲染状态变化时触发，`auto` 也会根据系统变化回调。 |

示例：

```vue
<u-config-provider
  @theme-change="name => console.log('主题切换到', name)"
  @mode-change="mode => console.log('渲染模式', mode)"
>
  <slot />
</u-config-provider>
```

## 常见场景

* **受控主题面板**：当你的设置页需要根据表单实时切换主题，可在父层直接修改 `currentTheme`，并监听 `theme-change` 做持久化。
* **多应用容器**：如果你的应用存在多个入口，可在每个入口都包裹一个 `u-config-provider`，无需担心初始化冲突。
* **局部覆写样式**：通过 `customStyle` / `customClass` 提供局部布局、背景覆写，同时依旧继承全局 CSS 变量。

## 最佳实践

* 始终通过 `useTheme` 获取 `darkMode` ref，保持单一数据源。
* 不要在业务组件里直接调用 `configProvider` 单例，`u-config-provider` + `useTheme` 已暴露全部能力。
* 若需要在页面层面自定义背景色、遮罩等，请使用 `$u-bg-color`、`rgba(var(--u-mask-color-rgb), .5)` 等变量，避免硬编码。

通过以上方式即可让 `u-config-provider` 在项目中稳定运行，确保主题/暗黑模式与应用保持同步。

---

---
url: 'https://uviewpro.cn/zh/components/countDown.md'
---
# CountDown 倒计时&#x20;

该组件一般使用于某个活动的截止时间上，通过数字的变化，给用户明确的时间感受，提示用户进行某一个行为操作。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`timestamp`参数设置倒计时间，单位为`秒`

```html
<template>
	<u-count-down :timestamp="timestamp"></u-count-down>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const timestamp = ref(86400)
</script>
```

## 设置是否显示天，时，分，秒

说明：参数的配置原则应该是"自右向左"的，设置了"时"，它右边的"分"和"秒"也应该设置为`true`

* `show-days`，`show-hours`，`show-minutes`，`show-seconds`等参数默认为`true`，分别对应是否显示倒计时的"天"，"时"，"分"，"秒"。

该示例表示只显示倒计时的分和秒

```html
<u-count-down :timestamp="86400" :show-days="false" :show-hours="false"></u-count-down>
```

## 倒计时分隔符

通过配置`separator`参数为`colon`或者`zh`来区分分隔符。`separator-size`配置分隔符的大小，单位rpx。`separator-color`配置分隔符的颜色
`separator`可选值如下：

* `colon`(默认)时显示为冒号，如：23:14:51
* `zh`时显示为中文，如：23时14分51秒

```html
<u-count-down :timestamp="86400" separator="colon" separator-size="28" separator-color="#606266"></u-count-down>
```

## 倒计时样式

* 通过`color`设置倒计数字的颜色
* `font-size`设置倒计数字的大小，重申一次：uView中，所有`font-size`，`width`，`height`，`padding`，`margin`等props参数
  的单位默认都是`rpx`，特别说明除外(极少数场景会要求px单位)。关于`rpx`单位的说明，请参考uni官方文档：[尺寸单位](https://uniapp.dcloud.io/frame?id=%e5%b0%ba%e5%af%b8%e5%8d%95%e4%bd%8d)
* `show-border`参数设置倒计数字是否添加边框，`border-color`参数设置边框的颜色

```html
<u-count-down :timestamp="86400" :show-border="true" font-size="28" color="#606266" border-color="#909399"></u-count-down>
```

## 倒计时执行的时机

通过`autoplay`配置倒计时是否在组件的`mounted`生命周期进行初始化(在`timestamp`有值前提下)，如果设置`autoplay`为`false`，就需要手动通过
`refs`的形式通知倒计时开始执行，调用的是组件内部的`start()`方法

```html
<template>
	<u-count-down ref="uCountDownRef" :timestamp="86400" :autoplay="false"></u-count-down>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

const uCountDownRef = ref()

onMounted(() => {
  setTimeout(() => {
    uCountDownRef.value.start()
  }, 2000)
})
</script>
```

## 如何获取当前倒计的秒数

有时候我们可会需要记录当前剩余的秒数，并在某个时机重新触发，可以通过如下两个方式实现：

* 监听`change`事件，在回调中获得当前剩余的秒数
* 通过ref调用，获取内部的`seconds`参数即为当前剩余的秒数

```html
<template>
	<u-count-down ref="uCountDownRef" :timestamp="timestamp" @change="change"></u-count-down>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const timestamp = ref(86400)
const uCountDownRef = ref()

// 事件触发，每秒一次
const change = (timestamp: number) => {
  console.log(timestamp)
}

// ref形式获取内部的值
const getSeconds = () => {
  console.log(uCountDownRef.value.seconds)
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| timestamp | 倒计时，单位为秒 | String | Number | 0 | - |
| autoplay | 是否自动开始倒计时，如果为`false`，需手动调用开始方法。见上方说明  | Boolean | true | false |
| separator | 分隔符，`colon`为英文冒号，`zh`为中文 | String  | colon | zh |
| separator-size | 分隔符的字体大小，单位rpx | String | Number  | 30 | - |
| separator-color | 分隔符的颜色 | String  | #303133 | - |
| font-size | 倒计时字体大小，单位rpx | String | Number  | 30 | - |
| show-border | 是否显示倒计时数字的边框 | Boolean | false | true |
| border-color | 数字边框的颜色 | String  | #303133 | - |
| bg-color | 倒计时数字的背景颜色 | String  | #ffffff | - |
| color | 倒计时数字的颜色 | String  | #303133 | - |
| height | 数字高度值(宽度等同此值)，设置边框时看情况是否需要设置此值，单位rpx | String  | auto | - |
| show-days | 是否显示倒计时的"天"部分 | Boolean  | true | false |
| show-hours | 是否显示倒计时的"时"部分 | Boolean  | true | false |
| show-minutes | 是否显示倒计时的"分"部分 | Boolean  | true | false |
| show-seconds | 是否显示倒计时的"秒"部分 | Boolean  | true | false |
| hide-zero-day | 当"天"的部分为0时，隐藏该字段 | Boolean  | true | false |

## Events

|事件名|说明|回调参数|
|:-|:-|:-|
|end|倒计时结束|-|
|change|倒计过程中，每秒触发一次|timestamp: 当前剩余的倒计秒数|

## Methods

需要通过ref获取倒计时组件才能调用，见上方"倒计时执行的时机"说明

| 名称          | 说明            |
|-------------  |---------------- |
| start | 开始倒计时  |
| end | 停止倒计时  |

---

---
url: 'https://uviewpro.cn/zh/components/countTo.md'
---
# CountTo 数字滚动&#x20;

该组件一般用于需要滚动数字到某一个值的场景，目标要求是一个递增的值。

::: warning 注意
如果给组件的父元素设置`text-align: center`想让数字水平居中，可能是由于元素内容快速变化而导致渲染的问题，在APP上组件可能会有轻微的左右抖动现象，
解决办法是给父元素设置`padding-left`或者`margin-left`即可。
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`start-val`设置开始值，`end-val`设置结束值

```html
<u-count-to :start-val="30" :end-val="500"></u-count-to>
```

## 设置滚动相关参数

* 通过`duration`设置从开始值到结束值整个滚动过程所需的时间，单位`ms`
* 通过`use-easing`设置滚动快结尾的时候，是否放慢滚动的速度，给用户更好的视觉效果

```html
<u-count-to :start-val="30" :end-val="500" :duration="2000" :use-easing="false"></u-count-to>
```

## 是否显示小数位

通过`decimals`设置显示的小数位，如果设置了，在滚动过程中，小数位会一起变化。如果`start-val`和`end-val`是带小数的，应该设置`decimals`为
`start-val`和`end-val`一样的小数位数值，如`end-val`为1200.55，那么`decimals`应该设置为2。

```html
<u-count-to :start-val="30" :end-val="500.55" :decimals="2"></u-count-to>
```

## 千分位分隔符

通过`separator`配置千分位分隔符，默认为空字符串，可以设置英文逗号","，此参数表现为`end-val`值超过1000时，比如为"1257"，那么滚动后会变成"1,245"，在金额数值时，
该参数可能会用上。

```html
<u-count-to :end-val="1542" separator=","></u-count-to>
```

## 滚动执行的时机

可以通过`autoplay`设置是否需要初始化时就开始滚动，默认为`true`，如果设置为`false`，可以通过组件的`ref`去控制组件内部的`start()`和`paused()`
方法来开始或暂停。

```html
<template>
	<u-count-to ref="uCountToRef" :end-val="endVal" :autoplay="autoplay"></u-count-to>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const endVal = ref(5000.55)
const autoplay = ref(false)
const uCountToRef = ref()

const start = () => {
  uCountToRef.value.start()
}

const paused = () => {
  uCountToRef.value.paused()
}

const reStart = () => {
  uCountToRef.value.reStart()
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| start-val | 开始值  | String | Number | 0 | - |
| end-val | 结束值 | String | Number  | 0 | - |
| duration | 滚动过程所需的时间，单位ms | String | Number  | 2000 | - |
| autoplay | 是否自动开始滚动 | Boolean  | true | false |
| decimals | 要显示的小数位数，见上方说明 | String | Number  | 0 | - |
| use-easing | 滚动结束时，是否缓动结尾，见上方说明 | Boolean  | true | false |
| separator | 千位分隔符，见上方说明 | String  | - | - |
| color | 字体颜色 | String  | #303133 | - |
| font-size | 字体大小，单位rpx | String | Number  | 50 | - |
| bold | 字体是否加粗 | Boolean | false | true |

## Methods

此方法如要通过ref手动调用

| 名称          | 说明            |
|-------------  |---------------- |
| start |  	`autoplay`为`false`时，通过此方法启动滚动 |
| reStart |   暂停后重新开始滚动(从暂停前的值开始滚动) |
| paused |   暂停滚动 |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| end | 数值滚动到目标值时触发 | - | - |

---

---
url: 'https://uviewpro.cn/zh/guide/customIcon.md'
---
# CustomIcon 扩展自定义图标库

uView Pro 已通过大量的实践中，收集了用户最有可能需要用到的图标，见 [Icon 图标](/zh/components/icon.html)，但我们也相信，它肯定无法覆盖所有的场景和需求。

用户也可以使用标签的方式，自行引入字体图标，为何要通过扩展的方式集成呢？\
这是因为 uView 有统一的字体图标组件，使用方便，配置灵活，且风格统一。

:::tip 说明
以下说明和演示，均针对[阿里字体图标库](https://www.iconfont.cn)，其他字体库源同理
:::

总的来说，我们要实现的效果如下：

```css
@font-face {
  /* 声明"custom-icon"字体 */
  font-family: "custom-icon";
  src: url("data:application/x-font-woff2;charset=utf-8;base64,xxxxxxxx") format("woff2");
}

.custom-icon {
  /* 引用上面声明的"custom-icon"字体 */
  font-family: "custom-icon" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 字体图标的前缀为"custom-icon-" */
.custom-icon-copy:before {
  content: "\e641";
}
```

通过如下方式引用：

通过`custom-prefix`指定类名为`custom-icon`

```html
<u-icon name="copy" custom-prefix="custom-icon"></u-icon>
```

## 基础说明

我们假定您一个项目中，需要扩展多个图标，所以您应该把各个图标收集进一个阿里图标库的项目中，即使您后面不断的扩展图标，也能让它们在同一个库中。

一般情况下，我们建议您在收藏的项目中，使用"下载至本地"的功能，而后解压，复制文件夹中的"iconfont.css"至 uni-app 目中(其余的文件可忽略)

下面的操作默认您已进入阿里图标库的"图标管理"栏目中

1. 我们建议，您应该修改这个图标的前缀，这样以后有新图标加入的时候，不用每次频繁修改前缀，在右上角的"更多操作"中，进入"编辑项目"：

2) 修改"FontClass/Symbol 前缀"项为"custom-icon-"，修改"Font Family"为"custom-icon"，如下图：

3. 下载项目至本地

4) 复制"iconfont.css"至项目，一般放在根目录的`static`文件夹下

5. 复制"iconfont.css"文件到 uni-app 目根目录的`static`目录后(也可以为其他目录)，打开"iconfont.css"，内部如下：

删掉下图圈出的部分，记得把"src: url('data:application/x-font-woff2......"最后的逗号`,`改成分号`;`。

6. 最终如下图：

7) 在项目根目录的"App.vue"中，引入上述的"iconfont.css"，注意自己存放的路径，且通过"@import"引入的外部样式，为了兼容性建议使用相对路径，
   且引入的样式，需要写在`style`标签有效内容中的最前面，如下：

```css
/* App.vue */
<style>
/* 此处为style标签内容的最前面 */
@import "./static/iconfont.css";

.view {
	......
}

/* 下面为错误示例，因为这里不是style标签内容的最前面，前面还有个".view"的样式 */
/* @import "./static/iconfont.css"; */
</style>
```

8. 在页面通过 uView 的[Icon](/zh/components/icon.html)组件使用图标，图标名称为您在阿里图标库中点击"编辑图标"时的"Font Class / Symbol"(该值可修改，每次修改都需重新下载"iconfont.css"放到 uni-app 目中，
   覆盖原来的"iconfont.css")

如上图，我们得到"backspace"值，使用如下：

```html
<u-icon
  name="backspace"
  custom-prefix="custom-icon"
  size="30"
  color="#888888"
></u-icon>
```

从上可以看出，相比 uView 内置的图标使用，多了一句固定的`custom-prefix="custom-icon"`，其余使用方法完全相同


**注意**：执行完上面的操作后，您就可以随心所欲的扩展自己的图标了，最重要的是第二步，修改了它，就免了以后每次都要修改"iconfont.css"的多处细节。
当然，每次新增图标，当您把"iconfont.css"复制至项目中覆盖原来的"iconfont.css"后，都需要执行一遍第 5 步删掉多余的内容，别忘了修改最后的`,`为`;`。

最后提一下，为了多平台兼容性，您应该仅把单色图标添加到阿里图标库的项目中，即使添加了多色的图标，在使用中，也会被转成单色。

祝您使用愉快！

---

---
url: 'https://uviewpro.cn/zh/tools/deepClone.md'
---
# deepClone 对象深度克隆

:::tip 注意
由于JS对象包括的范围非常广，加上ES6又有众多的新特性，很难、也没必要做到囊括所有的类型和情况，这里说的"对象"，指的是普通的对象，不包括修改对象原型链，
或者为"Function"，"Promise"等的情况，请留意。
:::

场景：

* 我们平时可能会遇到需要通过`console.log`打印一个对象，至执行打印的时刻，此对象为空，后面的逻辑中对此对象进行了修改赋值，但是我们在控制台直接看到的打印结果
  却是修改后的值，这让人匪夷所思，虽然我们可以通过`console.log(JSON.parse(JSON.stringify(object)))`的形式处理，但是需要写这长长的一串，难免让人心生抵触。

* 当我们将一个对象(变量A)赋值给另一个变量(变量B)时，修改变量B，因为对象引用的特性，导致A也同时被修改，所以有时候我们需要将A克隆给B，这样修改B的时候，就不会
  导致A也被修改。

### deepClone(object = {})

* `object` \<Object> 需要被克隆的对象

```js
let a = {
	name: 'mary'
};

// 直接赋值，为对象引用，即修改b等于修改a，因为a和b为同一个值
let b = a;

b.name = 'juli';
console.log(b); // 结果为 {name: 'juli'}
console.log(a); // 结果为 {name: 'juli'}


// 深度克隆
let b = uni.$u.deepClone(a);

b.name = 'juli';
console.log(b); // 结果为 {name: 'juli'}
console.log(a); // 结果为 {name: 'mary'}
```

---

---
url: 'https://uviewpro.cn/zh/tools/deepMerge.md'
---
# deepMerge 对象深度合并

:::tip 注意
由于JS对象包括的范围非常广，加上ES6又有众多的新特性，很难、也没必要做到囊括所有的类型和情况，这里说的"对象"，指的是普通的对象，不包括修改对象原型链，
或者为"Function"，"Promise"等的情况，请留意。
:::

在ES6中，我们可以很方便的使用`Object.assign`进行对象合并，但这只是浅层的合并，如果对象的属性为数组或者对象的时候，会导致属性内部的值丢失。

**注意：** 此处合并不同于`Object.assign`，因为`Object.assign(a, b)`会修改`a`的值为最终的结果(这往往不是我们所期望的)，但是`deepMerge(a, b)`并不会修改`a`的值。

### deepMerge(target = {}, source = {})

* `target` \<Object> 目标对象
* `source` \<Object> 源对象

`Object.assign`浅合并示例：

```js
let a = {
	info: {
		name: 'mary'
	}
}

let b = {
	info: {
		age: '22'
	}
}

// 使用Object.assign进行合并，注意此时a被修改了
let c = Object.assign(a, b);

// 我们期望的结果为：
c = {
	info: {
		name: 'mary',
		age: '22'
	}
}

// 事实上，我们得到的结果却为：
c = {
	info: {
		age: '22'
	}
}
```

深度合并示例：

```js
let a = {
	info: {
		name: 'mary'
	}
}

let b = {
	info: {
		age: '22'
	}
}

let c = uni.$u.deepMerge(a, b);

// c为我们期望的结果
c = {
	info: {
		age: '22',
		name: 'mary'
	}
}
```

---

---
url: 'https://uviewpro.cn/zh/components/divider.md'
---
# Divider 分割线&#x20;

区隔内容的分割线，一般用于页面底部"没有更多"的提示。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

文字内容通过`slot`传入

```html
<u-divider>大漠孤烟直</u-divider>
```

## 设置文字颜色

可以通过`color`指定文字的颜色

```html
<u-divider color="#fa3534">长河落日圆</u-divider>
```

## 设置单边边线条宽度和颜色

* `half-width`指定文字某一边的线条宽度(注意这里设置的是一边，而不是文字两边线条的总长度)，`half-width`可以是数值(rpx)或者百分比
* `type`可以快捷的设置线条为某一个主题色(默认`primary`)，`border-color`参数同样也能设置线条颜色，优先级高于`type`，也即是说二者同时
  设置了值，将会是`border-color`起作用。反之，如果要让`type`值起作用，就要将`border-color`置为空字符串或者`null`。

```html
<u-divider color="#fa3534" half-width="200" border-color="#6d6d6d">姑苏城外寒山寺</u-divider>
```

## API

## Props

| 参数          | 说明            | 类型            |        默认值        | 可选值   |
|-------------  |---------------- |---------------- |---------------------- |-------- |
| half-width | 文字左或右边线条宽度，数值或百分比，数值时单位为rpx  | String | Number | - | 150 |
| border-color | 线条颜色，优先级高于`type` | String  | #dcdfe6 | - |
| color | 文字颜色 | String  | #909399 | - |
| fontSize | 字体大小，单位rpx | String | Number  | 26 | - |
| bg-color | 整个divider的背景颜色 | String  | #ffffff | - |
| height | 整个divider的高度，单位rpx | string | Number  | 40 | - |
| type | 将线条设置主题色 | string  | primary | info \ success \ warning \ error |
| margin-top | 与前一个元素的距离，单位rpx | String | Number  | 0 | - |
| margin-bottom | 与后一个元素的距离，单位rpx | String | Number  | 0 | - |
| use-slot | 是否使用slot传入内容，如果不传入，中间不会有空隙 | Boolean  | true | false |

## Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| click | divider组件被点击时触发 | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/dropdown.md'
---
# Dropdown 下拉菜单 &#x20;

该组件一般用于向下展开菜单，同时可切换多个选项卡的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

使用前说明：

* 该组件必须结合`u-dorpdown`和`u-dropdown-item`一起使用，展开的内容由`u-dropdown-item`通过传递参数或者`slot`提供
* 组件的菜单栏标题由`u-dropdown-item`通过`title`参数提供
* `u-dropdown-item`带有默认的单选展示功能，通过`options`(见下方说明)配置，传入`slot`则会覆盖默认功能，通过`v-model`双向绑定`options`选中项的`value`值

```html
<template>
	<view class="">
		<u-dropdown>
			<u-dropdown-item v-model="value1" title="距离" :options="options1"></u-dropdown-item>
			<u-dropdown-item v-model="value2" title="温度" :options="options2"></u-dropdown-item>
		</u-dropdown>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value1 = ref<number>(1)
const value2 = ref<number>(2)

// 定义选项数据
const options1 = ref<Array<{ label: string; value: number }>>([
  {
    label: '默认排序',
    value: 1,
  },
  {
    label: '距离优先',
    value: 2,
  },
  {
    label: '价格优先',
    value: 3,
  }
])

const options2 = ref<Array<{ label: string; value: number }>>([
  {
    label: '去冰',
    value: 1,
  },
  {
    label: '加冰',
    value: 2,
  },
])
</script>
```

## 配置选项卡默认功能

如上所示，`u-dropdown-item`具有默认的单选功能，这里主要讲解其`options`和`v-model`参数：

`options`参数为一个数组，元素为对象，其中`label`为需要展示的提示文字，`value`为点击时双向绑定给`v-model`的值，`v-model`初始化时如果设置
某个`options`中的`value`，则该条目将会被默认选中：

```js
let options = [
	{
		label: '蜀道难',
		value: 1
	},
	{
		label: '难以上青天',
		value: 2
	}
]
```

## 配置选项卡自定义功能

在选项卡默认的单选功能无法满足的时候，我们可以给`u-dropw-item`传递`slot`来自定义需要展示的内容。

问：如果自定义内容，如何实现点击其中的按钮关闭下拉菜单？

答：在`u-dropdown`中，有一个`close()`方法，可以通过`ref`获取实例，并调用方法进行关闭即可。

```html
<template>
	<view class="">
		<u-dropdown ref="uDropdownRef">
			<u-dropdown-item title="属性">
				<view class="slot-content">
					<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">其他自定义内容</view>
					<u-button type="primary" @click="closeDropdown">确定</u-button>
				</view>
			</u-dropdown-item>
		</u-dropdown>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// 假设 u-dropdown 组件实例类型，实际使用时需要根据具体组件定义
const uDropdownRef = ref<any>(null)

const closeDropdown = () => {
	uDropdownRef.value.close()
}
</script>
```

## 配置选项卡内容可滚动

如果我们想给自定义内容的选项中局部内容可滚动，可以通过嵌入`scroll-view`元素实现，需要注意的是`scroll-view`必须声明高度才有效，大概如下：

```html
<template>
	<view class="">
		<u-dropdown ref="uDropdownRef">
			<u-dropdown-item title="属性">
				<view class="slot-content" style="background-color: #FFFFFF;">
					<scroll-view scroll-y="true" style="height: 200rpx;">
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">无言独上西楼</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">月如钩</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">寂寞梧桐深院锁清秋</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">剪不断</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">理还乱</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">是离愁</view>
						<view class="u-text-center u-content-color u-m-t-20 u-m-b-20">别是一般滋味在心头</view>
					</scroll-view>
					<u-button type="primary" @click="closeDropdown">确定</u-button>
				</view>
			</u-dropdown-item>
		</u-dropdown>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// 假设 u-dropdown 组件实例类型，实际使用时需要根据具体组件定义
const uDropdownRef = ref<any>(null)

const closeDropdown = () => {
	uDropdownRef.value.close()
}
</script>
```

## 如何保持菜单高亮

有时候，我们可能会希望下拉菜单收起之后，标题部分可以保持高亮，组件内部可以做到这样的要求，但是如果通过自定义`slot`传入了内容，那么组件就不知道
收起的时候，是否该保持菜单的高亮了，因为组件不知道您在自定义的内容中是否进行了"操作"，所以我们提供了一个手动通过`ref`设置的`highlight(index)`方法，
让您自主决定是否让某个菜单高亮，可以自行结合`change`(dropdown-item)、`open`(dropdown)、`close`(dropdown)事件进行组合操作。

```html
<template>
	<view class="">
		<u-dropdown ref="uDropdownRef" @open="open" @close="close">
			<u-dropdown-item v-model="value1" title="距离" :options="options1" @change="change"></u-dropdown-item>
			<u-dropdown-item v-model="value2" title="温度" :options="options2"></u-dropdown-item>
		</u-dropdown>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value1 = ref<number>(1)
const value2 = ref<number>(2)

// 定义选项数据
const options1 = ref<Array<{ label: string; value: number }>>([
	{
		label: '默认排序',
		value: 1,
	},
	{
		label: '距离优先',
		value: 2,
	}
])

const options2 = ref<Array<{ label: string; value: number }>>([
	{
		label: '去冰',
		value: 1,
	},
	{
		label: '加冰',
		value: 2,
	},
])

// 定义组件引用
const uDropdownRef = ref<any>(null)

// 定义事件处理函数
const open = (index: number) => {
	// 展开某个下来菜单时，先关闭原来的其他菜单的高亮
	// 同时内部会自动给当前展开项进行高亮
	uDropdownRef.value?.highlight()
}

const close = (index: number) => {
	// 关闭的时候，给当前项加上高亮
	// 当然，您也可以通过监听dropdown-item的@change事件进行处理
	uDropdownRef.value?.highlight(index)
}

const change = (value: any) => {
	// 更多的细节，如有需要请自行根据业务逻辑进行处理
	// uDropdownRef.value?.highlight(xxx)
}
</script>
```

## 兼容性

* 由于`头条小程序`的兼容性原因，如果`u-dropdown`父元素设置了`display: flex`，您可能需要给组件添加`u-dropdown`类，如下：

```html
<u-dropdown class="u-dropdown"></u-dropdown>
```

## API

## Dropdown Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| active-color | 标题和选项卡选中的颜色  | String  | #2979ff | - |
| inactive-color | 标题和选项卡未选中的颜色  | String  | #606266 | - |
| close-on-click-mask | 点击遮罩是否关闭菜单  | Boolean | true | false |
| close-on-click-self | 点击当前激活项标题是否关闭菜单  | Boolean | true | false |
| duration | 选项卡展开和收起的过渡时间，单位ms  | String | Number | 300 | - |
| height | 标题菜单的高度，单位任意，数值默认为rpx单位 | String | Number | 80 | - |
| border-bottom | 标题菜单是否显示下边框  | Boolean | false | true |
| title-size | 标题的字体大小，单位任意，数值默认为rpx单位 | String | Number | 28 | - |
| border-radius | 菜单展开内容下方的圆角值，单位任意 | String | Number | 0 | - |
| menu-icon | 标题菜单右侧的图标 | String | arrow-down | arrow-down-fill |
| menu-icon-size | 标题菜单右侧的图标的大小，单位任意，数值默认为rpx单位 | String | Number | 26 | - |

## Dropdown Events

|事件名|说明|回调参数|
|:-|:-|:-|
| open | 下拉菜单被打开时触发 | (index) - 当前被打开菜单的索引 |
| close | 下拉菜单被关闭时触发 | (index) - 当前被关闭菜单的索引 |

## Dropdown-item Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 双向绑定选项卡选择值  | String | Number | - | - |
| title | 菜单项标题  | String  | - | - |
| options | 选项数据，如果传入了默认slot，此参数无效，数据结构见上方说明  | Array\[Object]  | - | - |
| disabled | 是否禁用此选项卡  | Boolean | false | true |
| height | 弹窗下拉内容的高度(内容超出将会滚动)，`slot`自定义内容时无效(自行使用`scroll-view`处理)，单位任意，默认rpx | String | Number | auto | - |
| show  | 是否显示此选项卡 | Boolean | false | true |

## Dropdown-item Slot

| 名称          | 说明            |
|-------------  |---------------- |
| - | 自定义选项卡内容  |

## Dropdown-item Events

|事件名|说明|回调参数|
|:-|:-|:-|
| change | 每个`u-dropdown`均有此回调，点击某个`options`选项时触发 | (value) - 点击项绑定的`value`属性值 |

## Dropdown-item Methods

这些为组件内部的方法，需要通过`ref`调用

| 参数          | 说明            |
|-------------  |---------------- |
| highlight(index) | index为需要设置高亮的菜单项的索引(从0开始)，不写表示清空内部的高亮 |

---

---
url: 'https://uviewpro.cn/zh/components/empty.md'
---
# Empty 内容为空&#x20;

该组件用于需要加载内容，但是加载的第一页数据就为空，提示一个"没有内容"的场景，
我们精心挑选了十几个场景的图标，方便您使用。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

:::tip 提示
新版本移除了此组件内置的图片，因为这些图片太大，影响了组件库的大小。改用字体图标的形式提供，缺点是字体图标只能是单色的，形状与原来的图片也有些许出入。
基于以上，我们的专业设计师精心为您准备了一套精美缺省图，带有图片和`Sketch`文件，您可以下载或修改后再使用：[资源下载](/zh/components/resource.html)
:::

* 通过`text`参数配置提示的文字内容
* 通过`mode`(默认为`data`)参数配置要显示的图标

```html
<u-empty text="所谓伊人，在水一方" mode="list"></u-empty>
```

## 内置图标

这些图标已内置，直接通过`mode`参数引用即可

| 名称         | 说明            |
|-------------  |---------------- |
| car | 购物车为空 |
| page | 页面不存在 |
| search | 没有搜索结果 |
| address | 没有收货地址 |
| wifi | 没有WiFi |
| order | 订单为空 |
| coupon | 没有优惠券 |
| favor | 无收藏 |
| permission | 无权限 |
| history | 无历史记录 |
| news | 无新闻列表 |
| message | 消息列表为空 |
| list | 列表为空(通用) |
| data | 数据为空(默认，通用) |

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| color | 文字颜色 | String | #c0c4cc | - |
| text | 文字提示 | String  | 无内容 | - |
| icon-color | icon的颜色，字体图标时有效 | String  | #c0c4cc | - |
| icon-size | icon的大小，单位rpx，如果`src`为图片路径，此参数可以设置图片的尺寸 | String | Number  | 120 | - |
| src | 图标名称或者图片路径(绝对路径)，如定义，`mode`参数会失效 | String  | - | - |
| font-size | 提示文字的大小，单位rpx | String | Number  | 28 | - |
| mode | 内置的图标，见上方说明 | String  | data | - |
| img-width  | 图标的宽度，单位rpx | String | Number  | 240 | - |
| img-height  | 图标的高度，单位rpx | String  | auto | - |
| show | 是否显示组件 | Boolean  | true | false |
| margin-top | 组件到上一个元素的间距,单位rpx | String | Number  | 0 | - |

## Slot

| 名称          | 说明            |
|-------------  |---------------- |
| bottom |  给组件底部传入`slot`内容  |

---

---
url: 'https://uviewpro.cn/zh/components/fab.md'
---
# Fab 悬浮按钮 &#x20;

悬浮按钮（Floating Action Button）用于在页面右下角或指定位置提供常用快捷操作入口，支持拖拽、展开子操作项、以及多种布局策略。本文件按组件文档规范提供示例与 API 说明，包含平台差异与常见问题说明。

:::warning 注意
由于演示示例是通过`iframe`嵌入到网页的，所以可能会造成某些在网页上(浏览器 F12 手机调试模式无问题)无法使用，造成组件有 BUG 的错觉。
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本用法（默认右下角）

```html
<template>
  <u-fab @trigger="onTrigger" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

function onTrigger() {
  uni.showToast({ title: '触发', icon: 'none' })
}
</script>
```

示例：

```html
<!-- 有子项 -->
<u-fab>
  <u-button custom-style="margin:16rpx">收藏</u-button>
  <u-button custom-style="margin:16rpx">点赞</u-button>
</u-fab>

<!-- 自定义触发器 -->
<u-fab>
  <template #trigger>
    <u-button type="primary">触发器</u-button>
  </template>
</u-fab>
```

## 启用拖拽并关闭自动吸边

```html
<u-fab :draggable="true" :autoStick="false">
  <u-button custom-style="margin:12rpx">收藏</u-button>
  <u-button custom-style="margin:12rpx">分享</u-button>
</u-fab>
```

## 传入四边 gap 并设置右上角（position）

```html
<u-fab :position="'right-top'" :gap="{ top: 20, right: 20, bottom: 20, left: 20 }" :draggable="true">
  <u-icon name="star" size="60rpx"></u-icon>
  <u-icon name="heart" size="60rpx"></u-icon>
</u-fab>
```

## 自定义触发器并通过 ref 控制展开

```html
<template>
  <u-fab ref="fabRef" :draggable="true" :position="'left-bottom'">
    <template #trigger>
      <u-button type="primary" @click="onBtnClick">Menu</u-button>
    </template>
    <u-icon name="star" size="36rpx"></u-icon>
    <u-icon name="share" size="36rpx"></u-icon>
  </u-fab>
  <u-button @click="toggleFab">切换 FAB</u-button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const fabRef = ref<any>(null)
function toggleFab() {
  fabRef.value?.toggle?.()
}
function onBtnClick() {
  // 自定义触发器点击逻辑
}
</script>
```

## API

## Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|:- |:- |:- |:-: |:-: |
| type | 主题颜色 | String | `primary` | `primary` / `info` / `error` / `warning` / `success` |
| disabled | 是否禁用 | Boolean | `false` | - |
| draggable | 是否允许拖拽 | Boolean | `false` | - |
| autoStick | 拖拽释放后是否自动吸边（仅当 draggable=true 时生效） | Boolean | `true` | - |
| gap | 与屏幕边缘的间距，支持单值或对象分别配置四边间距，单位px |  Object | `{ left: 16, right: 16, top: 16, bottom: 16 }` | - |
| position | 预设停靠位置 | String | `right-bottom` | `left-top` / `right-top` / `left-bottom` / `right-bottom` / `left-center` / `right-center` / `top-center` / `bottom-center` |
| direction | 子操作项展开方向 | String | `top` | `top` / `bottom` / `left` / `right` |
| zIndex | 层级 | Number | `99` | - |

> 说明：`gap` 支持对象形式 `{ top, right, bottom, left }`，单位：px。

## Events

| 事件名 | 说明 | 回调参数 |
|:-|:-|:-|
| trigger | 当没有子项时，点击触发此事件 | event |

## 暴露方法

| 方法名 | 说明 |
|:-|:-|
| toggle | 切换展开/收缩状态（通过组件 ref 调用） |

## Slots

| 名称 | 说明 |
|:-|:-|
| default | 子操作项插槽（存在 slot 时组件作为展开菜单展示） |
| trigger | 自定义触发器（覆盖默认圆形按钮） |

---

---
url: 'https://uviewpro.cn/zh/components/field.md'
---
# Field 输入框&#x20;

借助此组件，可以实现表单的输入， 有"text"和"textarea"类型的，此外，借助uView的`picker`和`actionSheet`组件可以快速实现上拉菜单，时间，地区选择等，
为表单解决方案的利器。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`v-model`，可以双向绑定输入框的值
* 通过`label`设置输入框左边的提示文字
* 通过`placeholder`指定个性化的提示语

```html
<template>
	<view>
		<u-field
			v-model="mobile"
			label="手机号"
			placeholder="请填写手机号"
		>
		</u-field>
		<u-field
			v-model="code"
			label="验证码"
			placeholder="请填写验证码"
		>
		</u-field>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const mobile = ref<string>('')
const code = ref<string>('')
</script>
```

### 自定义输入框类型

我们可以通过`type`参数来自定义输入框的类型，如果为`text`(默认)内部为`input`输入框，如果为`textarea`值，内部为`textarea`输入框，相比`input`输入框，
它的默认高度约为两个`input`的高度，且可以换行，同时组件高度也会自动增高，适用于需要多行输入的场景。

```html
<template>
	<view class="">
		<u-field
			v-model="mobile"
			label="手机号"
			placeholder="请填写手机号"
		>
		</u-field>
		
		<u-field
			v-model="mobile"
			label="手机号"
			placeholder="请填写手机号"
			type="textarea"
		>
		</u-field>
	</view>
</template>
```

### 必填和错误提示

* 通过设置`required`，可以给输入框左边添加一个红色的"\*"号，它只起提示作用，uView内部不会判断用户是否输入了值，您需要提交的时候，通过`v-model`绑定的值自行判断
* 通过设置`error-message`，会在输入框下方给用红色给出错误提示

```html
<template>
	<view class="">
		<u-field
			v-model="mobile"
			label="手机号"
			required
			:error-message="errorMessage"
		>
		</u-field>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const mobile = ref<string>('')
const errorMessage = ref<string>('剑未配妥，出门已是江湖')
</script>
```

### 在输入框尾部插入按钮

此为在表单填写时，可能需要用户发送验证码的场景，可以通过`slot`插入一个uView的[button](/zh/components/button.html)组件，通过结合uView的[VerificationCode](/zh/components/verificationCode.html)，
可以简单，迅速的将功能集成

```html
<template>
	<view class="">
		<u-field
			v-model="code"
			label="验证码"
			placeholder="请填写验证码"
		>
			<template #right>
				<u-button size="mini" type="success" @click="getCode">{{codeText}}</u-button>
			</template>
		</u-field>
		<u-verification-code ref="uCodeRef" @change="codeChange"></u-verification-code>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const mobile = ref<string>('')
const code = ref<string>('')
const codeText = ref<string>('')

// 定义组件引用
const uCodeRef = ref<any>(null)

// 定义事件处理函数
const codeChange = (text: string) => {
	codeText.value = text
}

const getCode = () => {
	if (uCodeRef.value?.canGetCode) {
		// 模拟向后端请求验证码
		uni.showLoading({
			title: '正在获取验证码'
		})
		setTimeout(() => {
			uni.hideLoading()
			// 通知验证码组件内部开始倒计时
			uCodeRef.value?.start()
		}, 1000)
	} else {
		uni.$u.toast('倒计时结束后再发送')
	}
}
</script>
```

### 如何与Picker或者actionSheet等组件结合

某些场景，比如需要用用户选择性别，或者时间，地区选择等，我们可以结合uView的[ActionSheet](/zh/components/actionSheet.html)和[Picker](/zh/components/picker.html)组件解决，
这种情况，一般都是要求`field`组件是不可输入内容的，我们需要设置`disabled`参数为`true`，既然是需要弹出选择框，`field`组件右边应该要有一个实心向下的
三角形图标，配置为`right-icon`为`arrow-down-fill`，同时监听`click`即可。这一切，uView都帮您想到，并且做好了。

```html
<template>
	<view class="">
		<u-field @click="showAction" v-model="sex" 
		:disabled="true" label="性别" placeholder="请选择性别"
		right-icon="arrow-down-fill"
		>
		</u-field>
		<u-action-sheet @click="clickItem" :list="sexList" v-model="show"></u-action-sheet>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const sex = ref<string>('')
const show = ref<boolean>(false)

// 定义性别选项列表
const sexList = ref<Array<{ text: string }>>([
	{
		text: '男',
	},
	{
		text: '女'
	},
	{
		text: '保密'
	}
])

// 定义事件处理函数
const showAction = () => {
	show.value = true
}

const clickItem = (index: number) => {
	sex.value = sexList.value[index].text
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| type | 输入框的类型 | String  | text | textarea |
| icon | `label`左边的图标，限uView的图标名称 | String | - | - |
| border-bottom | 是否显示field的下边框 | Boolean  | true | false |
| border-top | 是否显示field的上边框 | Boolean  | false | true |
| icon-style | icon的样式，对象形式 | Object | - | - |
| right-icon | 输入框右边的图标名称，限uView的图标名称 | String  | - | - |
| required | 是否必填，左边显示红色"\*"号 | Boolean  | false | true |
| label | 输入框左边的文字提示 | String  | - | - |
| password | 是否密码输入方式(用点替换文字)，`type`为`text`时有效 | Boolean  | false | true |
| clearable | 是否显示右侧清空内容的图标控件(输入框有内容，且获得焦点时才显示)，点击可清空输入框内容 | Boolean  | true | false |
| label-width | `label`的宽度，单位rpx | Number | String | 130 | - |
| label-align | `label`的文字对齐方式 | String  | left | center / right |
| input-align | 输入框内容对齐方式 | String | left | center / right |
| icon-color | 左边通过`icon`配置的图标的颜色 | String  | #606266 | - |
| clear-size | 清除图标的大小，单位rpx | Number | String | 30 | - |
| field-style | 输入框的样式，对象形式 | Object  | - | - |
| auto-height | 是否自动增高输入区域，`type`为`textarea`时有效 | Boolean | true | false |
| error-message | 显示的错误提示内容，如果为空字符串或者`false`，则不显示错误信息 | String \ Boolean  | - | - |
| placeholder | 输入框的提示文字 | String | - | - |
| placeholder-style | `placeholder`的样式(内联样式，字符串)，如"color: #ddd" | String | - | - |
| focus | 是否自动获得焦点 | Boolean | false | true |
| fixed | 如果`type`为`textarea`，且在一个"position:fixed"的区域，需要指明为`true` | Boolean | false | true |
| disabled | 是否不可输入 | Boolean | false | true |
| maxlength | 最大输入长度，设置为 -1 的时候不限制最大长度 | Number | String | 140 | - |
| confirm-type | 设置键盘右下角按钮的文字，仅在type="text"时生效 | String | done | - |
| trim | 是否自动去除两端的空格 | Boolean | true | false |

## Slot

| 名称          | 说明            |
|-------------  |---------------- |
| icon | 自定义左侧的图标 |
| right | 自定义右侧内容 |

## Events

|事件名|说明|回调参数|
|:-|:-|:-|
| input | 输入框内容发生变化时触发 | value：输入框的内容，建议通过`v-model`双向绑定输入值，而不是监听此事件的形式 |
| focus | 输入框获得焦点时触发 | - |
| blur | 输入框失去焦点时触发 | - |
| confirm | 点击完成按钮时触发 | value：输入框的内容，建议通过`v-model`双向绑定输入值，而不是监听此事件的形式 |
| right-icon-click | 通过`right-icon`生成的图标被点击时触发 |
| click | 输入框被点击或者通过`right-icon`生成的图标被点击时触发，这样设计是考虑到传递右边的图标，一般都为需要弹出"picker"等操作时的场景，点击倒三角图标，理应发出此事件，见上方说明| - |

---

---
url: 'https://uviewpro.cn/zh/components/form.md'
---
# Form 表单&#x20;

此组件一般用于表单场景，可以配置Input输入框，Select弹出框，进行表单验证等。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

此组件一般是用于表单验证使用，每一个表单域由一个`u-form-item`组成，表单域中可以放置`u-input`、`u-checkbox`、`u-radio`、`u-switch`等。

* 在表单组中，通过`model`参数绑定一个对象，这个对象的属性为各个`u-form-item`内组件的对应变量。
* 由于表单验证和绑定表单规则时，需要通过`ref`操作，故这里需要给`form`组件声明`ref="uFormRef"`属性。
* 关于`u-from-item`内其他可能包含的诸如`input`、`radio`等组件，请见各自组件的相关文档说明。

下方为一个经典表单的示例，包含`input`、`textarea`、`radio`、`checkbox`、`switch`的组合使用：

```vue
<template>
	<u-form :model="form" ref="uFormRef">
		<u-form-item label="姓名"><u-input v-model="form.name" /></u-form-item>
		<u-form-item label="简介"><u-input v-model="form.intro" /></u-form-item>
		<u-form-item label="性别"><u-input v-model="form.sex" type="select" /></u-form-item>
		<u-form-item label="水果">
			<u-checkbox-group>
				<u-checkbox
					v-for="(item, index) in checkboxList"
					:key="index"
					v-model="item.checked"
					:name="item.name"
				>
					{{ item.name }}
				</u-checkbox>
			</u-checkbox-group>
		</u-form-item>
		<u-form-item label="味道">
			<u-radio-group v-model="radio">
				<u-radio
					v-for="(item, index) in radioList"
					:key="index"
					:name="item.name"
					:disabled="item.disabled"
				>
					{{ item.name }}
				</u-radio>
			</u-radio-group>
		</u-form-item>
		<u-form-item label="开关">
			<template #right>
				<u-switch v-model="switchVal"></u-switch>
			</template>
		</u-form-item>
	</u-form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

const uFormRef = ref();
const form = reactive({
	name: '',
	intro: '',
	sex: ''
});
const checkboxList = reactive([
	{ name: '苹果', checked: false, disabled: false },
	{ name: '雪梨', checked: false, disabled: false },
	{ name: '柠檬', checked: false, disabled: false }
]);
const radioList = reactive([
	{ name: '鲜甜', disabled: false },
	{ name: '麻辣', disabled: false }
]);
const radio = ref('');
const switchVal = ref(false);
</script>
```

## Form-item组件说明

此组件一般需要搭配`Form`组件使用，也可以单独搭配`Input`等组件使用，由于此组件参数较多，这里只对其中参数最简要介绍，其余请见底部的API说明：

* `prop`为传入`Form`组件的`model`中的属性字段，如果需要表单验证，此属性是必填的。
* `label-position`可以配置左侧"label"的对齐方式，可选为`left`和`top`。
* `border-bottom`是否显示表单域的下划线，如果给`Input`组件配置了边框，可以将此属性设置为`false`，从而隐藏默认的下划线。
* 如果想在表单域配置左右的图标(或小图片，[Icon 图标](/zh/components/icon.html)可以配置图片)，可以通过`left-icon`和`right-icon`参数实现。

## 表单验证

uView Pro的表单组件具备完整的验证功能，在开始之前，需要了解如下几个注意事项，方面您快速上手：

### `Form`组件绑定`model`参数

* `model`参数为一个对象，对象属性为需要验证的变量名。
* 通过`ref`，在`onMounted`生命周期调用组件的`setRules`方法绑定验证规则，无法通过`props`传递变量，是因为微信小程序会过滤掉对象中的方法，导致自定义验证规则无效。

```vue
<template>
	<view>
		<u-form :model="form" ref="uFormRef">
			<u-form-item label="姓名" prop="name">
				<u-input v-model="form.name" />
			</u-form-item>
			<u-form-item label="简介" prop="intro">
				<u-input v-model="form.intro" />
			</u-form-item>
		</u-form>
		<u-button @click="submit">提交</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';

const uFormRef = ref();
const form = reactive({
	name: '',
	intro: ''
});
const rules = {
	name: [
		{
			required: true,
			message: '请输入姓名',
			// 可以单个或者同时写两个触发验证方式 
			trigger: ['change', 'blur']
		}
	],
	intro: [
		{
			min: 5,
			message: '简介不能少于5个字',
			trigger: 'change'
		}
	]
};

function submit() {
	uFormRef.value?.validate((valid: boolean) => {
		if (valid) {
			console.log('验证通过');
		} else {
			console.log('验证失败');
		}
	});
}

onMounted(() => {
	uFormRef.value?.setRules(rules);
});
</script>
```

### 嵌套验证

自`v0.3.15`起，uView Pro的表单组件支持嵌套验证，即`u-form-item`的 `prop` 可以书写成`a.b.c`，如：

```html
<template>
	<view> 
		<u-form :model="model" :rules="rules" ref="uFormRef">  
			<u-form-item label="特长" prop="extra.strong">
				<u-textarea
					:border="border"
					v-model="model.extra.strong"
					placeholder="请输入特长，这是一个嵌套校验，a.b.c"
					count
				></u-textarea>
			</u-form-item>
		</u-form>
		<u-button type="primary" @click="handleSubmit" :throttle-time="0">提交</u-button>
        <u-gap></u-gap>
        <u-button @click="handleReset" :throttle-time="0">重置</u-button>
	</view>
</template>

<script setup lang="ts"> 
import { ref, reactive } from 'vue';
import { $u } from 'uview-pro';
import type { FormRules } from 'uview-pro/types/global';

const uFormRef = ref();

interface Model {
    extra: { strong: string };
}
const model = reactive<Model>({
    extra: {
        strong: ''
    }
});

// 校验规则
const rules: FormRules = {
    'extra.strong': [
        {
            required: true,
            message: '请输入特长',
            trigger: ['change', 'blur']
        },
        {
            min: 5,
            message: '特长不能少于5个字',
            trigger: ['change', 'blur']
        },
        // 正则校验示例，此处用正则校验是否中文，此处仅为示例，因为uView有this.$u.test.chinese可以判断是否中文
        {
            pattern: /^[\u4e00-\u9fa5]+$/gi,
            message: '特长只能为中文',
            trigger: ['change', 'blur']
        }
    ]
};

// 提交表单
function handleSubmit() {
    uFormRef.value?.validate((valid: boolean, errors: any[]) => {
        if (valid) {
            if (!model.agreement) return $u.toast('请勾选协议');
            console.log('验证通过', errors);
        } else {
            console.log('表单信息', model);
            console.log('验证失败', errors);
        }
    });
}

// 重置表单
function handleReset() {
    uFormRef.value?.resetFields();
}
</script>
```

### 深层验证、动态验证

自`v0.4.5`起，uView Pro 的表单组件支持深层验证、动态验证：

详情参考[form校验](https://github.com/anyup/uView-Pro/blob/master/src/pages/componentsA/form/index.vue)

### u-form-item绑定`label`和`prop`

此组件最大的作用是与`u-form`和`u-input`等组件进行交互，在表单验证时，需要绑定`prop`参数，此参数为`u-form`组件的`model`对象中的属性名，
目的是在验证时，通过这个`prop`属性名将父组件`u-form`的`model`和`rules`规则关联起来。

注意点：

* 通过`prop`绑定对应的属性名，这里是字符串，而不是一个变量。
* 通过`label`参数设置左边显示的提示文字，另外通过`label-position`可以配置`label`在左边还是上方。

```vue
<template>
	<u-form :model="form" ref="uFormRef">
		<u-form-item label="姓名" prop="name">
			<u-input v-model="form.name" />
		</u-form-item>
		<u-form-item label="简介" prop="intro">
			<u-input v-model="form.intro" />
		</u-form-item>
	</u-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';

const uFormRef = ref();
const form = reactive({
	name: '',
	intro: ''
});
const rules = {
	name: [
		{
			required: true,
			message: '请输入姓名',
			// 可以单个或者同时写两个触发验证方式
			trigger: ['blur', 'change']
		}
	],
	intro: [
		{
			min: 5,
			message: '简介不能少于5个字',
			trigger: 'change'
		}
	]
};

onMounted(() => {
	uFormRef.value?.setRules(rules);
});
</script>
```

从上面的示例我们可以看到，`rules`中的属性名和`form`的属性名是一致的，同时传递给`u-form-item`的`prop`参数绑定的也是相同的属性名，注意这里`prop`参数绑定的是
字符串(属性名)，而不是一个变量。

### 验证规则

组件验证部分采用了[async-validator](https://github.com/yiminghe/async-validator)，一个字段可以设置多个内置规则，以及自定义规则，触发方式等，
每个字段的验证规则为一个数组，数组的每一个元素对象为其中一条规则(一个字段的验证可以配置多个规则)，如下：

```ts
const rules = {
	name: [
		// 对name字段进行长度验证
		{
			min: 5,
			message: '简介不能少于5个字',
			trigger: 'change'
		},
		// 对name字段进行必填验证
		{
			required: true,
			message: '请填写姓名',
			trigger: ['change', 'blur']
		}
	]
};
```

### 验证规则属性

每一个验证规则中，可以配置多个属性，下面对常用的属性进行讲解，更具体的可以查看[async-validator](https://github.com/yiminghe/async-validator)的文档说明：

* `trigger`{`String | Array`}：触发校验的方式有2种：
  * change：字段值发生变化时校验
  * blur：输入框失去焦点时触发
  * 如果同时监听两种方式，需要写成数组形式：`['change', 'blur']`

* `type`{String}\
  内置校验规则，如这些规则无法满足需求，可以使用正则匹配、或者使用`validator`自定义方法并结合uView自带[验证规则](/zh/tools/test.html)。
  * string：必须是 `string` 类型，默认类型
  * number：必须是 `number` 类型
  * boolean：必须是 `boolean` 类型
  * method：必须是 `function` 类型
  * regexp：必须是 `regexp` 类型，这里的正则，指的是判断字段的内容是否一个正则表达式，而不是用这个正则去匹配字段值
  * integer：必须是`整数`类型
  * float：必须是`浮点数`类型
  * array：必须是 `array` 类型
  * object：必须是 `object` 类型
  * enum：必须出现在 `enmu` 指定的值中
  * date：必须是 `date` 类型
  * url：必须是 `url` 类型
  * hex：必须是 `16` 进制类型
  * email：必须是 `email` 类型
  * any：任意类型

* `required`\
  布尔值，是否必填，配置此参数不会显示输入框左边的必填星号，如需要，请配置`u-form-item`的`required`为`true`

* `pattern`\
  要求此参数值为一个正则表达式，如： /\d+/，**不能**带引号，如："/\d+/"，组件会对字段进行正则判断，返回结果。

* `min`\
  最小值，如果字段类型为字符串和数组，会取字符串长度与数组长度(length)与`min`比较，如果字段是数值，则直接与`min`比较。

* `max`\
  最大值，规则同`min`参数

* `len`\
  指定长度，规则同`min`，优先级高于`min`和`max`

* `enum`{Array}
  指定的值，配合 type: 'enum' 使用

* `whitespace`{Boolean}\
  如果字段值内容都为空格，默认无法通过`required: true`校验，如果要允许通过，需要将此参数设置为`true`

* `transform`{Function}，校验前对值进行转换，函数的参数为当前值，返回值为改变后的值，参数如如下：
  * `value`：当前校验字段的值

* `message`\
  校验不通过时的提示信息

* `validator`{Function}：自定义**同步**校验函数，参数如下：
  * `rule`：当前校验字段在 rules 中所对应的校验规则
  * `value`：当前校验字段的值
  * `callback`：校验完成时的回调，一般无需执行callback，返回`true`(校验通过)或者`false`(校验失败)即可

* `asyncValidator`{Function}：自定义**异步**校验函数，参数如下：
  * `rule`：当前校验字段在 rules 中所对应的校验规则
  * `value`：当前校验字段的值
  * `callback`：校验完成时的回调，执行完异步操作(比如向后端请求数据验证)，如果不通过，需要callback(new Error('提示错误信息'))，如果校验通过，执行callback()即可

### uView Pro自带验证规则

uView在JS板块的[Test 规则校验](/zh/tools/test.html)中有大量内置的验证规则，这些规则对表单验证来说，属于**自定义规则**，故需要用到上方规则属性的
`validator`自定义验证函数，这里做一个详细说明。

我们知道uView有自带的判断手机号的验证方法`uni.$u.test.mobile(value)`，但是[async-validator](https://github.com/yiminghe/async-validator)没有
内置判断手机号的规则，所以将二者结合使用：

```ts
const rules = {
	// 字段名称
	mobile: [
		{
			required: true,
			message: '请输入手机号',
			trigger: ['change', 'blur']
		},
		{
			// 自定义验证函数，见上说明
			validator: (rule: any, value: string, callback: Function) => {
				// uni.$u.test.mobile()就是返回true或者false的
				return uni.$u.test.mobile(value);
			},
			message: '手机号码不正确',
			trigger: ['change', 'blur']
		}
	]
};
```

### 综合实战

上面讲述了[async-validator](https://github.com/yiminghe/async-validator)的规则和配置，以及uView内置规则的结合使用，下面我们进行一个综合
实战示例，要入对某一个字段进行如下验证(验证实现有多种方法，下方仅为引导示例，非唯一，或最优做法)：

1. 必填，同时可接受`change`和`blur`触发校验：配置`required`参数为`true`，同时配置`trigger`为`[change, bulr]`
2. 必须为字母或字符串，校验前先将字段值转为字符串类型：通过`pattern`参数配置正则：/^\[0-9a-zA-Z]\*$/g，通过`transform`参数在校验前对字段值转换为字符串
3. 长度6-8个字符之间：通过 配置`min`为6，`max`为8
4. 需要包含字母"A"：使用uView的`uni.$u.test.contains()`方法，并结合`validator`自定义函数实现
5. 异步校验，输入完账号，输入框失去焦点时，向后端请求该账号是否已存在：通过上方的`asyncValidator`异步函数进行验证。

综上，我们可以得出如下的一个配置规则(仅为综合演示，非最优做法)：

```ts
const rules = {
	name: [
		// 必填规则
		{
			required: true,
			message: '此为必填字段',
			// blur和change事件触发检验
			trigger: ['blur', 'change']
		},
		// 正则判断为字母或数字
		{
			pattern: /^[0-9a-zA-Z]*$/g,
			// 正则检验前先将值转为字符串
			transform(value: any) {
				return String(value);
			},
			message: '只能包含字母或数字'
		},
		// 6-8个字符之间的判断
		{
			min: 6,
			max: 8,
			message: '长度在6-8个字符之间'
		},
		// 自定义规则判断是否包含字母"A"
		{
			validator: (rule: any, value: string, callback: Function) => {
				return uni.$u.test.contains(value, "A");
			},
			message: '必须包含字母"A"'
		},
		// 校验用户是否已存在
		{
			asyncValidator: (rule: any, value: string, callback: Function) => {
				uni.$u.post('/xxx/xxx', { name: value }).then((res: any) => {
					// 如果验证不通过，需要在callback()抛出new Error('错误提示信息')
					if (res.error) {
						callback(new Error('姓名重复'));
					} else {
						// 如果校验通过，也要执行callback()回调
						callback();
					}
				});
			}
			// 如果是异步校验，无需写message属性，错误的信息通过Error抛出即可
			// message: 'xxx'
		}
	]
};
```

### 校验错误提示方式

uView提供了多种校验的错误提示方式，这些值需要包含在数组(可以填写多个值，同时进行多种提示)中，传递给`Form`组件的`error-type`参数：

* `message`：默认为输入框下方用文字进行提示
* `none`：只要包含此值，将不会进行任何提示
* `border-bottom`：配置作用域底部的下划线显示为红色
* `border`：配置输入框的边框为红色进行提示 -- 如果有配置显示`Input`组件显示边框的话
* `toast`：以"toast"提示的方式弹出错误信息，每次只弹出最前面的那个表单域的错误信息

```vue
<template>
	<u-form :error-type="errorType">
		<!-- ... -->
	</u-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const errorType = ref(['message']);
// 不提示
// const errorType = ref(['none']);
// 文字和下划线提示
// const errorType = ref(['message', 'border-bottom']);
</script>
```

### 校验

进行了上方的配置和讲解后，进入到最后一步，执行验证：\
需要通过`ref`调用`Form`组件的`validate`方法，该方法回调函数的参数为一个布尔值，`true`为校验通过，否则反之。

```vue
<template>
	<view>
		<u-form :model="form" ref="uFormRef">
			<u-form-item label="姓名" prop="name">
				<u-input v-model="form.name" />
			</u-form-item>
		</u-form>
		<u-button @click="submit">提交</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';

const uFormRef = ref();
const form = reactive({
	name: ''
});
const rules = {
	name: [
		{
			required: true,
			message: '请输入姓名',
			trigger: ['blur', 'change']
		}
	]
};

function submit() {
	uFormRef.value?.validate((valid: boolean) => {
		if (valid) {
			console.log('验证通过');
		} else {
			console.log('验证失败');
		}
	});
}

onMounted(() => {
	uFormRef.value?.setRules(rules);
});
</script>
```

## API

## Form Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| model | 表单数据对象  | Object	 | - | - |
| rules | 通过`ref`设置，见上方说明 | Object | - | - |
| error-type | 错误的提示方式，数组形式，见上方说明 | Array | \['message', 'toast'] | - |
| border-bottom | 是否显示表单域的下划线边框 | Boolean | true | - |
| label-position | 表单域提示文字的位置，`left`-左侧，`top`-上方 | String | left | top |
| label-width | 提示文字的宽度，单位rpx | String | Number | 90 | 数值 / auto |
| label-style | `lable`的样式，对象形式 | Object | - | - |
| label-align | `lable`的对齐方式 | String | left |  center / right |

## Form Methods

此方法如要通过ref手动调用

| 名称          | 说明            |    参数   |
|-------------  |---------------- |  ---------------- |\
| setRules | 调用此方法，设置校验规则  | Function(rules) |
| resetFields | 对整个表单进行重置，将所有字段值重置为初始值并移除校验结果  | - |
| validate | 对整个表单进行校验的方法，第一个参数为boolean，表示校验结果，第二个参数为数组，包含所有错误信息支持第二个参数 | Function(callback: Function(boolean, array)) |

## Form-item Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| label | 左侧提示文字  | String	 | - | - |
| prop | 表单域`model`对象的属性名，在使用 validate、resetFields 方法的情况下，该属性是必填的 | String | - | - |
| border-bottom | 是否显示下边框，如不需要下边框，需同时将`u-form`的同名参数设置为`false` | Boolean | true | true / false |
| label-position | 表单域提示文字的位置，`left`-左侧，`top`-上方，如设置，将覆盖`u-form`的同名参数 | String | - | left / top |
| label-width | 提示文字的宽度，单位rpx，如设置，将覆盖`u-form`的同名参数| String | Number | - | - |
| label-style | `lable`的样式，对象形式，如设置，将覆盖`u-form`的同名参数 | Object | - | - |
| label-align | `lable`的对齐方式，如设置，将覆盖`u-form`的同名参数 | String | - |  - |
| right-icon | 右侧自定义字体图标(限uView内置图标)或图片地址 | String |  - |
| left-icon | 左侧自定义字体图标(限uView内置图标)或图片地址 | String |  - |
| left-icon-style | 左侧图标的样式，对象形式 | Object | - | - |
| right-icon-style | 右侧图标的样式，对象形式 | Object | - | - |
| required | 是否显示左边的"\*"号，这里仅起展示作用，如需校验必填，请通过`rules`配置必填规则 | Boolean | false | true |

## Form-item Slot

|名称|说明|版本|
|:-|:-|:-|
| default | Form Item 的内容 | - |
| right | 右侧自定义内容，可以在此传入一个按钮，用于获取验证码等场景 | - |
| label | 左侧标题自定义内容 |  |

---

---
url: 'https://uviewpro.cn/zh/components/fullScreen.md'
---
# fullScreen 压窗屏

所谓压窗屏，是指遮罩能盖住原生导航栏和底部tabbar栏的弹窗，一般用于在APP端弹出升级应用弹框，或者其他需要增强型弹窗的场景。

:::danger 警告
由于uni-app的Bug，在最新版的HX2.8.6(包括之前的多个版本)，此功能(组件)无效，等到uni-app修复此Bug时，我们会撤销此通告。
:::

:::tip 提示
这里的做法是在本页面打开一个新页面，同时在`pages.json`中配置本页面的背景为百分百透明，这样即可达到压窗效果。\
由于只有APP支持设置页面背景透明度，故只有APP支持本组件做法，非APP端不支持。
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|x|x|x|x|x|x|

## 基本使用

本组件只是提供参考思路和注意事项，因为每个人在弹窗需要实现的逻辑和样式都是不一样的，请参考本文档思路，自行实行相关功能。

首先，我们需要`pages.json`中声明一个页面用于弹窗：

```js
// pages.json

"pages": [
	{
		"path": "uview-pro/components/u-full-screen/u-full-screen",
		"style": {
			"navigationStyle": "custom",  // 取消本页面的导航栏
			"app-plus": {
				"animationType": "fade-in", // 设置fade-in淡入动画，为最合理的动画类型
				"background": "transparent", // 背景透明
				"backgroundColor": "rgba(0,0,0,0)", // 背景透明
				"popGesture": "none" // 关闭IOS屏幕左边滑动关闭当前页面的功能
			}
		}
	}
]
```

通过上面的配置，我们得到了一个页面：

* 这个页面去掉了导航栏
* 页面进入的时候，是采用淡入动画的形式
* 并且此页面的背景是百分比透明度，这样可以看到底层页面的内容
* 移除在iOS上左滑手势，避免本页被左滑关闭

## 触发压窗屏

我们在父页面(当前页面)通过路由方法，打开一个新页面(上面配置的压窗屏页面)，由于它是一个普通的页面，故可以通过常规方法传递参数。

```js
<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'

// 页面加载时触发
onLoad(() => {
  // 也可以在onShow生命周期打开，此为uView封装的请求方法
  uni.$u.route("/uview-pro/components/u-full-screen/u-full-screen?id=1")
})
</script>
```

## 定义压窗屏内容

当我们触发(打开)了压窗屏页面之后，将会有一个新的，背景透明的页面覆盖在本页面上，由于我们的终极目标就是要做一个弹窗，让其遮罩盖住"父页面"的导航栏和
Tabbar栏，所以这里我们可以使用uView的[Popup 弹出层](/zh/components/popup.html)组件，并且将`popup`组件的`mode`参数设置`center`，即中部弹出的形式。

下方示例为打开一个[Modal 模态框](/zh/components/modal.html)组件的示例，此组件内部用的也是`popup`组件。

```html
<template>
	<u-modal v-model="show" :show-cancel-button="true" confirm-text="升级"
		title="发现新版本" @cancel="cancel" @confirm="confirm"
	>
		<view class="u-update-content">
			<rich-text :nodes="content"></rich-text>
		</view>
	</u-modal>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 定义响应式数据
const show = ref<boolean>(true)

// 传递给uni-app"rich-text"组件的内容，可以使用"<br>"进行换行
const content = ref<string>(`
	1. 修复badge组件的size参数无效问题<br>
	2. 新增Modal模态框组件<br>
	3. 新增压窗屏组件，可以在APP上以弹窗的形式遮盖导航栏和底部tabbar<br>
	4. 修复键盘组件在微信小程序上遮罩无效的问题
`)

// 页面准备完成时触发
onMounted(() => {
	show.value = true
})

// 定义事件处理函数
const cancel = () => {
	closeModal()
}

const confirm = () => {
	closeModal()
}

const closeModal = () => {
	uni.navigateBack()
}
</script>

<style scoped lang="scss">
.u-full-content {
	background-color: #00C777;
}

.u-update-content {
	font-size: 26rpx;
	color: $u-content-color;
	line-height: 1.7;
	padding: 30rpx;
}
</style>
```

上面有一个需要注意的点，我们打开"压窗"弹窗后，可能需要通过一些按钮来关闭弹窗，这里关闭弹窗的本质意义是关闭弹出的页面(压窗屏弹框)，所以用的是uni-app带的
关闭页面的接口`uni.navigateBack()`，见上方示例。

## 注意事项

由于压窗屏其实也是一个普通的页面的，当我们关闭弹窗(顶层页面)，"父页面"(上一个页面)就会显示出来，意味着会进入`onShow`生命周期，如有相关特定逻辑需要
处理，可关注此处。

由于弹窗打开的实际是一个页面，而不是一个组件，所以我们无法通过`props`的形式传递参数，有如下方式可以行进两个页面之间的通信：

* 父页面通过URL参数的形式将参数传递给弹窗
* 当弹窗内进行某些操作之后，可以通过`uni.$emit`的方式发送事件，父页面中通过`uni.$on`的形式接收事件和参数，达到通信的效果
* 通过Vuex的形式共享变量

---

---
url: 'https://uviewpro.cn/zh/components/gap.md'
---
# Gap 间隔槽&#x20;

该组件一般用于内容块之间的用一个灰色块隔开的场景，方便用户风格统一，减少工作量

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

直接引入即可使用

* 通过`height`配置高度，单位rpx
* 通过`bg-color`配置背景颜色

```html
<u-gap height="80" bg-color="#bbb"></u-gap>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| bg-color |  背景颜色 | String	 | transparent(背景透明) | - |
| height | 间隔槽高度，单位rpx  | String | Number | 30 | - |
| margin-top | 与前一个元素的距离，单位rpx | String | Number  | 0 | - |
| margin-bottom | 与后一个元素的距离，单位rpx | String | Number  | 0 | - |

---

---
url: 'https://uviewpro.cn/zh/tools/getRect.md'
---
# getRect 节点布局信息

此方法封装自uni的[nodesRef.boundingClientRect](https://uniapp.dcloud.io/api/ui/nodes-info?id=nodesrefboundingclientrect)，它极大简化了
使用复杂度，内部使用`Promise`，可以让用户同步获取节点信息。

### getRect(selector, instance, all)

* `selector` \<String> 此参数为元素节点，可以是`id`或者`class`，比如"#user-name"，".box"
* `instance` \<ComponentInternalInstance> 此参数为组件实例，通过 `getCurrentInstance()` 获得
* `all` \<Boolean> 是否返回全部节点信息，当页面有多个相同`selector`的元素时，`all`为`true`，会以数组形式返回所有节点的信息(结果为数组，数组元素为对象)，否则只返回第一个节点的信息(结果为一个对象)

注意：该方法返回的结果，共有如下有用信息：

```js
res = {
	left: 0,
	right: 414,
	top: 323,
	height: 2597,
	bottom: 2920,
	width: 414
}
```

受限于`nodesRef.boundingClientRect`，其上结果中的`left`，`top`，`right`，`bottom`，是会随着页面滚动而变化的，因为这个查询的相对于屏幕窗口，而不是
相对于页面根元素的，但`width`，`height`，是恒定不变的，所以一般情况我们推荐您想要获取节点宽高的时候采用这个方法。

:::warning 注意
由于`onLoad`生命周期元素尚未创建完成，请勿在此生命周期使用此方法，如果是页面，应该在`onReady`生命周期，组件内应该在`mounted`生命周期调用。
如果要查询的目标，是通过服务端获取数据后才渲染的，那么应该在获取数据后，通过`this.$nextTick`调用此方法。
:::

### 异步使用方法

通过`then`调用即可

```js
const instance = getCurrentInstance()

getElInfo() {
	uni.$u.getRect('.user-avatar', instance).then(res => {
		console.log(res);
	})
}

```

### 同步使用方法

该方法的使用场景为您下一步的操作需要获取元素的节点后才能进行的情况，可以通过`async/await`方式调用，注意，无论是生命周期还是`methods`中的方法，都可以在
其前面添加`async`修饰符

```js
const instance = getCurrentInstance()

async getElInfo() {
	let rectInfo = await uni.$u.getRect('.user-avatar', instance);
	console.log(rectInfo);
}
```

### 请求数据后再获取节点信息

此场景为元素内容为后端获取数据填充的，节点填充数据前后，元素的大小尺寸是不一样的，所以需要在获取后再执行此方法，这里通过`this.$nextTick`调用，
是因为它会等待数据赋值，元素创建完成后再执行，此时才是准确的尺寸，以下演示，为uView Pro自带的[http 请求](/zh/tools/http.html)方法调用

```html
<template>
	<view>
		<view class="user-name">
			{{ userName }}
		</view>
	</view>
</template>

<script setup >
import { ref, onMounted, getCurrentInstance } from 'vue';

const userName = ref('');
const instance = getCurrentInstance();

onMounted(() => {
	getElInfo();
});

async function getElInfo() {
	try {
		const res = await uni.$u.post('http://www.example.com/user/info');
		userName.value = res.name;
		await nextTick();
		const rect = await uni.$u.getRect('.user-avatar', instance);
		console.log(rect);
	} catch (error) {
		console.error(error);
	}
}
</script>
```

### 获取全部节点信息

设置第二个参数为`true`，此场景为页面有多个相同类名的元素，需要获取所有同类名节点信息时候使用，返回结果为一个数组

```html
<template>
	<view>
		<view class="item">
			uView Pro
		</view>
		<view class="item">
			<view>红豆生南国，春来发几枝</view>
			<view>愿君多采撷，此物最相思</view>
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';

const instance = getCurrentInstance();

onMounted(() => {
	getElInfo();
});

async function getElInfo() {
	try {
		const rect = await uni.$u.getRect('.item', instance, true);
		console.log(rect); // rect为一个数组(内有2个元素)，因为页面有2个.item节点
	} catch (error) {
		console.error(error);
	}
}
</script>
```

### 如何让让某个元素滚动到页面顶部

这里说的顶部，指的是导航栏的下方，比如我们点击某个操作，页面自动滚动，指定元素位于导航栏下方时停止。\
我们需要结合`onPageScroll`生命周期，获得实时的页面滚动条位置。

```html
<template>
	<view class="wrap">
		<view class="item">
			uView Pro
		</view>
		<view class="item">
			uView Pro
		</view>
		<view class="item">
			uView Pro
		</view>
		<view class="item">
			uView Pro
		</view>
		<view class="item object-item" @tap="scrollEl">
			点我，我就会滚动到导航栏下方
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';
import { onPageScroll } from '@dcloudio/uni-app';

const instance = getCurrentInstance();

const scrollTop = ref(0);

onPageScroll((e: { scrollTop: number }) => {
    scrollTop.value = e.scrollTop;
});

const scrollEl = () => {
  uni.$u.getRect('.object-item', instance).then(res => {
    uni.pageScrollTo({
      scrollTop: scrollTop.value + res.top,
      duration: 0
    });
  });
}
</script>

<style lang="scss" scoped>
	.wrap {
		height: 200vh;
	}
</style>
```

---

---
url: 'https://uviewpro.cn/zh/components/grid.md'
---
# Grid 宫格布局&#x20;

宫格组件一般用于同时展示多个同类项目的场景，可以给宫格的项目设置徽标组件([badge](/zh/components/badge.html))，或者图标等，也可以扩展为左右滑动的轮播形式。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 该组件外层为`u-grid`组件包裹，通过`col`设置内部宫格的列数
* 内部通过`ugrid-item`组件的`slot`设置宫格的内容
* 如果不需要宫格的边框，可以设置`border`为`false`

```html
<template>
	<u-grid :col="3">
		<u-grid-item>
			<u-icon name="photo" :size="46"></u-icon>
			<view class="grid-text">图片</view>
		</u-grid-item>
		<u-grid-item>
			<u-icon name="lock" :size="46"></u-icon>
			<view class="grid-text">锁头</view>
		</u-grid-item>
		<u-grid-item>
			<u-icon name="hourglass" :size="46"></u-icon>
			<view class="grid-text">沙漏</view>
		</u-grid-item>
	</u-grid>
</template>

<style scoped lang="scss">
	.grid-text {
		font-size: 28rpx;
		margin-top: 4rpx;
		color: $u-type-info;
	}
</style>
```

## 给宫格设置右上角的角标和图标

可以通过uView的`badge`(注意Badge在此需要设置相关定位属性，详见[Badge](/zh/components/badge.html))或者`image`设置宫格有右上角的内容

```html
<template>
	<u-grid :col="3">
		<u-grid-item>
			<u-badge count="9" :offset="[20, 20]"></u-badge>
			<u-icon name="photo" :size="46"></u-icon>
			<view class="grid-text">图片</view>
		</u-grid-item>
		<u-grid-item>
			<image src="/static/image/icon/hot5.png" class="badge-icon"></image>
			<u-icon name="lock" :size="46"></u-icon>
			<view class="grid-text">锁头</view>
		</u-grid-item>
		<u-grid-item>
			<u-icon name="hourglass" :size="46"></u-icon>
			<view class="grid-text">沙漏</view>
		</u-grid-item>
	</u-grid>
</template>

<style scoped lang="scss">
	.badge-icon {
		position: absolute;
		top: 14rpx;
		right: 40rpx;
		width: 30rpx;
		height: 30rpx;
	}
	
	.grid-text {
		font-size: 28rpx;
		margin-top: 4rpx;
		color: $u-type-info;
	}
</style>
```

## 实现宫格的左右滑动

结合uni的swiper组件可以实现宫格的左右滑动，因为`swiper`特性的关系，请指定`swiper`的高度 ，否则`swiper`的高度不会被内容撑开，可以自定义`swiper`的指示器，达到更高的灵活度

```html
<template>
	<swiper class="swiper" @change="change">
		<swiper-item>
			<u-grid :col="3" @click="click" hover-class="hover-class">
				<u-grid-item v-for="(item, index) in list" :index="index" :key="index">
					<u-icon :name="item" :size="46"></u-icon>
					<text class="grid-text">{{ '宫格' + (index + 1) }}</text>
				</u-grid-item>
			</u-grid>
		</swiper-item>
		<swiper-item>
			<u-grid :col="3" @click="click">
				<u-grid-item v-for="(item, index) in list" :index="index + 9" :key="index">
					<u-icon :name="item" :size="46"></u-icon>
					<text class="grid-text">{{ '宫格' + (index + 1) }}</text>
				</u-grid-item>
			</u-grid>
		</swiper-item>
		<swiper-item>
			<u-grid :col="3" @click="click">
				<u-grid-item v-for="(item, index) in list" :index="index + 18" :key="index">
					<u-icon :name="item" :size="46"></u-icon>
					<text class="grid-text">{{ '宫格' + (index + 1) }}</text>
				</u-grid-item>
			</u-grid>
		</swiper-item>
	</swiper>
	<view class="indicator-dots" v-if="isSwiper">
		<view class="indicator-dots-item" :class="[current == 0 ? 'indicator-dots-active' : '']">
		</view>
		<view class="indicator-dots-item" :class="[current == 1 ? 'indicator-dots-active' : '']">
		</view>
		<view class="indicator-dots-item" :class="[current == 2 ? 'indicator-dots-active' : '']">
		</view>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const current = ref<number>(0)
const list = ref<Array<string>>([
	'integral', 'kefu-ermai', 'coupon', 'gift', 'scan', 
	'pause-circle', 'wifi', 'email', 'list'
])

// 定义事件处理函数
const change = (e: any) => {
	current.value = e.detail.current
}

// 注意：isSwiper 变量在原代码中未定义，但模板中使用了，这里需要根据实际需求处理
const isSwiper = ref<boolean>(true)

// 注意：click 方法在模板中使用了但未在原代码中定义，这里需要根据实际需求实现
const click = (index: number) => {
	// 根据实际需求实现点击逻辑
	console.log('点击了宫格:', index)
}
</script>

<style scoped lang="scss">
/* 下方这些scss变量为uView内置变量，详见开发  组件-指南-内置样式 */

.grid-text {
	font-size: 28rpx;
	margin-top: 4rpx;
	color: $u-type-info;
}

.swiper {
	height: 480rpx;
}

.indicator-dots {
	margin-top: 40rpx;
	display: flex;
	justify-content: center;
	align-items: center;
}

.indicator-dots-item {
	background-color: $u-tips-color;
	height: 6px;
	width: 6px;
	border-radius: 10px;
	margin: 0 3px;
}

.indicator-dots-active {
	background-color: $u-type-primary;
}
</style>
```

## API

## Grid Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| col | 宫格的列数  | String | Number | 3 | - |
| border | 是否显示宫格的边框  | Boolean	 | true | false |
| align | 宫格的对齐方式，用于控制只有一两个宫格时的对齐场景  | String | left | center / right |
| hover-class | 样式类名，按下时有效，样式必须写在根目录的`App.vue`或通过其引入的全局样式中才有效，`none`为无效果，作用于头部标题区域  | String | u-hover-class | none / 其他 |

## Grid-item Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| bg-color | 宫格的背景颜色  | String | #ffffff | - |
| index | 点击宫格时，返回的值  | String | Number	 | - | - |

## Grid Event

注意：请在`<u-grid></u-grid>`上监听此事件

|事件名|说明|回调参数|
|:-|:-|:-|
|click|点击宫格触发|index: `u-grid-item`通过`props`传递的`index`值|

## Grid-item Event

注意：请在`<u-grid-item></u-grid-item>`上监听此事件

|事件名|说明|回调参数|
|:-|:-|:-|
|click|点击宫格触发|index: `u-grid-item`通过`props`传递的`index`值|

---

---
url: 'https://uviewpro.cn/zh/tools/guid.md'
---
# guid 全局唯一标识符

## 唯一标识符

### guid(length = 32, firstU = true, radix = 62)

该函数可以生产一个全局唯一、随机的guid，默认首字母为`u`，可以用于当做元素的id或者class名等需要唯一，随机字符串的地方，因为id或者class不能以数字开头。

* `length` \<Number | null> guid的长度，默认为`32`，如果取值`null`，则按`rfc4122标准`生成对应格式的随机数
* `firstU` \<Boolean> 首字母是否为"u"，如果首字母为数字情况下，不能用作元素的`id`或者`class`，默认为`true`
* `radix` \<Number> 生成的基数，默认为`62`，用于生成随机数字符串为"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"，
  如果取2，那么返回的结果就是前两位0和1(可以理解为二进制)的随机结果，如果为7，返回的字符串就是0-7(理解为八进制)之间，
  10为十进制，以此类推。

**说明**：这个方法三个参数都有默认的值，所以您调用的时候，可以无需传递任何参数也是可以的，并且**建议您这样做**。

```html
<template>
	<view :id="$u.guid()" :class="elClass">
		
	</view>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { $u } from 'uview-pro';

const elClass = ref('');

onMounted(() => {
  elClass.value = $u.guid(20);
});
</script>
```

---

---
url: 'https://uviewpro.cn/zh/components/icon.md'
---
# Icon 图标&#x20;

基于字体的图标集，包含了大多数常见场景的图标。

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

:::tip 提示
如果您觉得内置的图标数量不够，或者不合符您的需求，别担心，我们还精心为您准备了一份简单易用的扩展自定义图标库教程：[扩展自定义图标库](https://uviewpro.cn/zh/guide/customIcon.html)
:::

通过`<u-icon>`形式来调用，设置`name`参数为图标名即可

```html
<u-icon name="photo"></u-icon>
```

## 修改图标的样式

* 通过`color`参数修改图标的颜色
* 通过`size`参数修改图标的大小，单位为 rpx

```html
<u-icon name="photo" color="#2979ff" size="28"></u-icon>
```

## 图片图标

这里说的图片图标，指的是小图标，起作用定位为"icon"图标作用，而非大尺寸的图片展示场景，理论上，这个小图标应该为`png`格式的正方形图标。

上面说到，给组件的`name`参数传入一个图片的名称即可显示字体图标，这些名称中不能带有`/`斜杠符号，否则会被认为是传入了图片图标，同时，`size`参数
也被设置为这个图片图标的宽度，由于是图片，诸如颜色`color`等参数都会失效。

```html
<u-icon
  label="uView"
  size="40"
  name="https://ik.imagekit.io/anyup/uview-pro/logo/default.png"
></u-icon>
```

## API

## Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|---|---|---|---|---|
| name | 图标名称，见示例图标集，如名称带有`/`，会被认为是图片图标 | String | - | - |
| color | 图标颜色 | String | inherit | - |
| size | 图标字体大小，单位 rpx | String|Number | inherit | - |
| index | 一个用于区分多个图标的值，点击图标时通过`click`事件传出 | String | - | - |
| hover-class | 图标按下去的样式类，用法同 uni 的`view`组件的`hover-class`参数，详见：[hover-class](https://uniapp.dcloud.io/component/view) | String | - | - |
| label | 图标右侧/下方的 label 文字 | String | - | - |
| label-size | `label`字体大小，单位 rpx | String|Number | 28 | - |
| label-color | `label`字体颜色 | String | #606266 | - |
| custom-prefix | 自定义字体图标库时，需要写上此值，详见：[扩展自定义图标库](https://uviewpro.cn/zh/guide/customIcon.html) | String | uicon | - |
| space  | `label`在四周时与图标的距离，权重高于 margin，单位 rpx | String|Number | - | - |
| margin-left | `label`在右方时与图标的距离，单位 rpx | String|Number | 6 | - |
| margin-top | `label`在下方时与图标的距离，单位 rpx | String|Number | 6 | - |
| margin-bottom | `label`在上方时与图标的距离，单位 rpx | String|Number | 6 | - |
| margin-right | `label`在左侧时与图标的距离，单位 rpx | String|Number | 6 | - |
| label-pos | `label`相对于图标的位置 | String | right | bottom/top/left |
| width | `name`为图片路径时图片的宽度，单位任意，数值默认为 rpx 单位 | String|Number | - | - |
| height | `name`为图片路径时图片的高度，单位任意，数值默认为 rpx 单位 | String|Number | - | - |
| top | 如果某些场景，如果图标没有垂直居中，可以调整此参数，单位任意，数值默认为 rpx 单位 | String|Number | 0 | - |
| show-decimal-icon | 是否为 DecimalIcon | Boolean | false | true |
| inactive-color | 背景颜色，可接受主题色，仅 Decimal 时有效 | String | #ececec | - |
| percent | 显示的百分比，仅 Decimal 时有效 | String|Number | 50 | - |

## Events

| 事件名 | 说明           | 回调参数                          | 版本 |
| :----- | :------------- | :-------------------------------- | :--- |
| click  | 点击图标时触发 | index: 通过`props`传递的`index`值 | -    |

## 图标集

---

---
url: 'https://uviewpro.cn/zh/components/image.md'
---
# Image 图片&#x20;

此组件为 uni-app 的`image`组件的加强版，在继承了原有功能外，还支持淡入动画、加载中、加载失败提示、圆角值和形状等。\
**我们推荐您在任何使用图片场景的地方，都优先考虑使用这个小巧，精致而实用的组件。**

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

配置图片的`width`宽和`height`高，以及`src`路径即可使用。

```html
<template>
  <u-image width="100%" height="300rpx" :src="src"></u-image>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const src = ref<string>("https://ik.imagekit.io/anyup/uview-pro/logo/default.png");
</script>
```

## 填充模式

通过`mode`参数配置填充模式，此模式用法与 uni-app 的`image`组件的`mode`参数完全一致，详见：[Image](https://uniapp.dcloud.io/component/image)

```html
<u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png" mode="widthFix"></u-image>
```

## 图片形状

* 通过`shape`参数设置图片的形状，`circle`为圆形，`square`为方形
* 如果为方形时，还可以通过`border-radius`参数设置圆角值

```html
<u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png" shape="circle"></u-image>
```

## 懒加载

注意：此功能只对微信小程序、App、百度小程序、字节跳动小程序有效，默认开启。

```html
<u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png" :lazy-load="true"></u-image>
```

## 加载中提示

图片加载过程中，为加载中状态(默认显示一个小图标)，可以通过`loading`自定义插槽，结合 uView 的`u-loading`组件，实现加载的动画效果。

```html
<u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png">
  <template #loading>
    <u-loading></u-loading>
  </template>
</u-image>
```

## 加载错误提示

图片加载失败时，默认显示一个错误提示图标，可以通过`error`自定义插槽，实现个性化的提示方式。

```html
<u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png">
  <template #error>
    <view style="font-size: 24rpx;">加载失败</view>
  </template>
</u-image>
```

## 淡入动画

组件自带了加载完成时的淡入动画效果：

* 通过`fade`参数配置是否开启动画效果
* 通过`duration`参数配置动画的过渡时间，单位 ms

```html
<u-image
  src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png"
  :fade="true"
  duration="450"
></u-image>
```

## 事件冒泡

默认情况下，组件是允许内部向外事件冒泡的，因为很多情况下，我们都希望点击图片，同时图片所在的父元素的点击事件也能触发。\
如果您想避免事件冒泡，那么您可以在组件外面嵌套一个`view`，同时给它加上`@tap.stop`即可。

```html
<!-- 点击图片将不会触发clickHandler -->
<view @tap="clickHandler">
  <view @tap.stop>
    <u-image src="https://ik.imagekit.io/anyup/uview-pro/logo/default.png"></u-image>
  </view>
</view>
```

## API

## Props

| 参数                            | 说明                                                          | 类型             | 默认值       | 可选值 |
| ------------------------------- | ------------------------------------------------------------- | ---------------- | ------------ | ------ |
| src                             | 图片地址，**强烈建议**使用绝对或者网络路径                    | String           | -            | -      |
| mode                            | 裁剪模式，见上方说明                                          | String           | aspectFill   | -      |
| width                           | 宽度，单位任意，如果为数值，则为 rpx 单位                     | String | Number | 100%         | -      |
| height                          | 高度，单位任意，如果为数值，则为 rpx 单位                     | String | Number | auto         | -      |
| shape                           | 图片形状，circle-圆形，square-方形                            | String           | square       | circle |
| border-radius                   | 圆角值，单位任意，如果为数值，则为 rpx 单位                   | String | Number | 0            | -      |
| lazy-load                       | 是否懒加载，仅微信小程序、App、百度小程序、字节跳动小程序有效 | Boolean          | true         | -      |
| show-menu-by-longpress          | 是否开启长按图片显示识别小程序码菜单，仅微信小程序有效        | Boolean          | true         | -      |
| loading-icon                    | 加载中的图标，或者小图片                                      | String           | photo        | -      |
| error-icon                      | 加载失败的图标，或者小图片                                    | String           | error-circle | -      |
| show-loading                    | 是否显示加载中的图标或者自定义的 slot                         | Boolean          | true         | false  |
| show-error                      | 是否显示加载错误的图标或者自定义的 slot                       | Boolean          | true         | false  |
| fade                            | 是否需要淡入效果                                              | Boolean          | true         | false  |
| webp                            | 只支持网络资源，只对微信小程序有效                            | Boolean          | false        | true   |
| duration                        | 搭配`fade`参数的过渡时间，单位 ms                             | String | Number | 500          | -      |
| bg-color | 背景颜色                                                      | String           | #f3f4f6      | -      |

## Slot

| 名称    | 说明                   |
| :------ | :--------------------- |
| loading | 自定义加载中的提示内容 |
| error   | 自定义失败的提示内容   |

## CellItem Events

| 事件名 | 说明               | 回调参数      |
| :----- | :----------------- | :------------ |
| click  | 点击图片时触发     | -             |
| error  | 图片加载失败时触发 | err: 错误信息 |
| load   | 图片加载成功时触发 | -             |

---

---
url: 'https://uviewpro.cn/zh/components/indexList.md'
---
# IndexList 索引列表&#x20;

通过折叠面板收纳内容区域

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

外层包裹一个`index-list`组件，内部锚点通过`index-anchor`组件传入，其余内容可以自定义

* 可以通过`index-list`参数自定义索引字符列表
* 需要监听页面的onPageScroll事件，将当前滚动条高度传入`index-list`组件

```html
<template>
	<u-index-list :scrollTop="scrollTop">
		<view v-for="(item, index) in indexList" :key="index">
			<u-index-anchor :index="item" />
			<view class="list-cell">
				列表1
			</view>
			<view class="list-cell">
				列表2
			</view>
			<view class="list-cell">
				列表3
			</view>
		</view>
	</u-index-list>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onPageScroll } from '@dcloudio/uni-app'

// 定义响应式数据
const scrollTop = ref<number>(0)
const indexList = ref<Array<string>>([
	"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
	"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
])

// 页面滚动事件处理
onPageScroll((e) => {
	scrollTop.value = e.scrollTop
})
</script>

<style lang="scss" scoped>
.list-cell {
	display: flex;
	box-sizing: border-box;
	width: 100%;
	padding: 10px 24rpx;
	overflow: hidden;
	color: #323233;
	font-size: 14px;
	line-height: 24px;
	background-color: #fff;
}
</style>
```

## 自定义锚点样式

`index-anchor`锚点组件默认显示`index`参数的值，可以通过设置`use-slot`为`true`，传入自定义内容，同时设定
自己的样式

```html
<template>
	<u-index-list :scrollTop="scrollTop">
		<view v-for="(item, index) in indexList" :key="index">
			<u-index-anchor :use-slot="true">
				<text class="anchor-text">{{item}}</text>
			</u-index-anchor>
			<view class="list-cell">
				列表1
			</view>
			<view class="list-cell">
				列表2
			</view>
			<view class="list-cell">
				列表3
			</view>
		</view>
	</u-index-list>
</template>

<style lang="scss" scoped>
	.list-cell {
		display: flex;
		box-sizing: border-box;
		width: 100%;
		padding: 10px 24rpx;
		overflow: hidden;
		color: #323233;
		font-size: 14px;
		line-height: 24px;
		background-color: #fff;
	}
	
	.anchor-text {
		color: red;
	}
</style>
```

## 自定义导航栏

默认情况下，组件的锚点是吸附在导航栏下方的，如果您修改了导航栏，比如取消导航栏、或者自定义了导航栏，就需要指定吸顶的高度，也就是`offset-top`
的值，注意这个值的单位为`rpx`：

* 如果取消导航栏，需要将`offset-top`为`0`
* 如果自定义了导航栏，需要`offset-top`设置为导航栏的高度

## API

## IndexBar Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| scroll-top | 当前滚动高度，自定义组件无法获得滚动条事件，所以依赖接入方传入 | Number | String | - | - |
| index-list | 索引字符列表，数组  | Array\[string | number] | A-Z | - |
| z-index | 锚点吸顶时的层级  | Number | String | 965 | - |
| sticky | 是否开启锚点自动吸顶  | Boolean | true | false |
| offset-top | 锚点自动吸顶时与顶部的距离，单位rpx，见上方"自定义导航栏"说明  | Number | String | 0 | - |
| active-color | 锚点和右边索引字符高亮颜色  | String | #2979ff | - |

## IndexAnchor Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| use-slot | 是否使用自定义内容的插槽  | Boolean | false | true |
| index | 索引字符，如果定义了`use-slot`，此参数自动失效   | String | Number | - | - |

## IndexBar Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| select | 选中右边索引字符时触发 | index: 索引字符 | - |

## IndexAnchor Slots

| 名称 | 说明 |
|:-|:-|
| default | 锚点位置显示内容，默认为索引字符 |

---

---
url: 'https://uviewpro.cn/zh/components/input.md'
---
# Input 输入框&#x20;

此组件为一个输入框，默认没有边框和样式，是专门为配合表单组件[u-form](/zh/components/form.html)而设计的，利用它可以快速实现表单验证，输入内容，下拉选择等功能。

::: tip 提示
v0.3.7 已新增 Textarea 文本域组件，用于长文本输入，详见：[Textarea 文本域](/zh/components/textarea.html)。
:::

**注意：** 当您仅是需要一个输入框的话，可以考虑使用[u-field](/zh/components/field.html)组件，而如果是一个表单组，比如有多个输入框一起，且需要验证功能的时候，
应该在`u-form`中嵌套`u-form-item`，再嵌套`u-input`去实现。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`v-model`绑定输入框的值
* 通过`type`设置输入框的类型
* 通过`border`配置是否显示输入框的边框

```html
<template>
	<u-input v-model="value" :type="type" :border="border" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<string>('')
const type = ref<string>('text')
const border = ref<boolean>(true)
</script>
```

## 输入框的类型

综述：此组件通过配置`type`参数有两种形态：

1. 一是长文本内容输入的`textarea`类型。
2. 二是类似普通输入框的`text`类型，在普通输入框时，由于HTML5或者小程序等一些特殊场景，此	`type`参数又可以设置为`text`、`number`、`idcard`、`digit`等值，
   这些参数跟各个平台的兼容性有关，详见uni-app文档：[Input 组件](https://uniapp.dcloud.io/component/input)。

### Textarea模式

此模式需要将`type`参数设置为`textarea`，有如下两个需要注意的参数：

* `auto-height`参数可以配置为`textarea`输入框的高度是否随着行数增加，而自动增加输入框的高度。
* `height`参数可以配置输入框的初始高度。

```html
<template>
	<u-input v-model="value" :type="type" :border="border" :height="height" :auto-height="autoHeight" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<string>('')
const type = ref<string>('textarea')
const border = ref<boolean>(true)
const height = ref<number>(100)
const autoHeight = ref<boolean>(true)
</script>
```

### Text模式

将`type`设置为`text`，此种情况为一个单纯的输入框，但是还可以将其设置为`number`、`idcard`、`digit`等值，需要考虑兼容性，见上方说明。

```html
<template>
	<u-input v-model="value" :type="type" :border="border" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<string>('')
const type = ref<string>('text')
const border = ref<boolean>(true)
</script>
```

### Password模式

`type`参数可以设置为`password`，此时输入内容将会用点替代：

* 如果设置`password-icon`设置为`true`，右侧将会出现一个可以切换密码与普通字符的图标。

```html
<template>
	<u-input v-model="value" :type="type" :border="border" :password-icon="passwordIcon" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<string>('')
const type = ref<string>('password')
const passwordIcon = ref<boolean>(true)
const border = ref<boolean>(true)
</script>
```

### Select下拉选择模式

如果将`type`设置为`select`，此时组件将会在外观上呈现出Select选择器的形态，主要体现在右侧多了一个下三角图标，但是此时组件并没有内置下拉的功能，
主要是考虑到移动端的特殊性和uView内置组件的关联性，因为想实现下拉选择，不同场景可能会使用不同的组件，比如uView的[Picker 选择器](/zh/components/picker.html)、
[ActionSheet 操作菜单](/zh/components/actionSheet.html)、[Select 列选择器](/zh/components/select.html)等，您可以根据情况自由选择合适的组件做搭配。

* 以上说的可以配合的组件，它们都有一个共同的通过`v-model`绑定弹出与收起的参数，可以同时将此参数赋值给`Input`组件的`select-open`参数，
  当此参数为`true`(也即`Select`选择器打开时)，右侧的下三角图标会翻转，为`false`时，恢复原位。
* 监听组件的`@click`事件，在此将绑定选择器的参数修改为`true`即可。

```html
<template>
	<view class="">
		<u-input v-model="value" :type="type" :border="border" @click="show = true" />
		<u-action-sheet :list="actionSheetList" v-model="show" @click="actionSheetCallback"></u-action-sheet>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<string>('')
const type = ref<string>('select')
const show = ref<boolean>(false)
const border = ref<boolean>(true)

const actionSheetList = ref<Array<{ text: string }>>([
	{
		text: '男'
	},
	{
		text: '女'
	},
	{
		text: '保密'
	}
])

// 定义事件处理函数
const actionSheetCallback = (index: number) => {
	value.value = actionSheetList.value[index].text
}
</script>
```

## API

## Props

| 参数                                     | 说明            | 类型            | 默认值             |  可选值   |
|----------------------------------------|---------------- |---------------|------------------ |-------- |
| type                                   | 模式选择，见上方说明  | String	 | text | select / password / textarea / number |
| clearable                              | 是否显示右侧的清除图标，type = select时无效 | Boolean | true | false |
| v-model                                | 用于双向绑定输入框的值 | - | - | - |
| input-align                            | 输入框文字的对齐方式  | String | left | center / right |
| placeholder                            | placeholder显示值  | String | 请输入内容 | - |
| disabled                               | 是否禁用输入框 | Boolean | false | true |
| maxlength                              | 输入框的最大可输入长度 | Number | String | 140 | - |
| placeholder-style                      | placeholder的样式，字符串形式，如"color: red;" | String | "color: #c0c4cc;" | - |
| confirm-type                           | 设置键盘右下角按钮的文字，仅在`type`为`text`时生效  | String | done | - |
| focus                                  | 是否自动获得焦点 | Boolean | false | true |
| fixed                                  | 如果`type`为`textarea`，且在一个"position:fixed"的区域，需要指明为`true` | Boolean | false | true |
| password-icon                          | `type`为`password`时，是否显示右侧的密码查看图标 | Boolean | true | false |
| border                                 | 是否显示边框 | Boolean | false | true |
| border-color                           | 输入框的边框颜色 | String | #dcdfe6 | - |
| auto-height                            | 是否自动增高输入区域，`type`为`textarea`时有效 | Boolean | true | false |
| height                                 | 高度，单位rpx | Number | String | text类型时为70，textarea时为100 | - |
| count| type为textarea模式下显示计数| Boolean | false | true |
| cursor-spacing  | 指定光标与键盘的距离，单位**px** | Number | String | 0 | - |
| selection-start | 光标起始位置，自动聚焦时有效，需与selection-end搭配使用 | Number | String | -1 | - |
| selection-end   | 光标结束位置，自动聚焦时有效，需与selection-start搭配使用 | Number | String | -1 | - |
| trim            | 是否自动去除两端的空格 | Boolean | true | false |
| show-confirmbar | 是否显示键盘上方带有”完成“按钮那一栏 | Boolean | true | false |
| adjust-position | 弹出键盘时是否自动调节高度 | Boolean | true | false |

---

---
url: 'https://uviewpro.cn/zh/components/keyboard.md'
---
# Keyboard 键盘&#x20;

此为uView自定义的键盘面板，内含了数字键盘，车牌号键，身份证号键盘3种模式，都有可以打乱按键顺序的选项。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`mode`参数定义键盘的类型，v-model绑定一个值为布尔值的变量控制键盘的弹出与收起：

* mode = number (默认值)为数字键盘，此时顶部工具条中间的提示文字为"数字键盘"
* mode = car 为汽车键盘，此时顶部工具条中间的提示文字为"车牌号键盘"
* mode = card 为身份证键盘，此时顶部工具条中间的提示文字为"身份证键盘"

```html
<template>
	<view>
		<u-keyboard ref="uKeyboardRef" mode="car" v-model="show"></u-keyboard>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)

// 定义组件引用
const uKeyboardRef = ref<any>(null)
</script>
```

## 控制键盘顶部的工具条

* 通过`tooltip`参数配置是否显示显示顶部的工具条，默认为`true`
* 通过`tips`参数修改工具条中间的提示文字
* 通过`show-tips`可以控制是否显示工具条中间的文字
* 通过`cancelBtn`参数配置是否显示工具条左边的"取消"按钮
* 通过`confirmBtn`参数配置是否显示工具条右边的"完成"按钮

```html
<u-keyboard mode="car" tips="请输入车牌号" :cancelBtn="false"></u-keyboard>
```

## 是否显示键盘的点(".")按键

该按键通过`dot-enabled`(默认为`true`)参数配置，只在"mode = number"时生效，因为车牌号和身份证键盘，用不到"."这个按键

```html
<u-keyboard ref="uKeyboard" mode="number" :dot-enabled="false" v-model="show"></u-keyboard>
```

## 是否打乱按键的顺序

如果配置`random`参数为`true`的话，**每次**打开键盘，按键的顺序都是随机的，该功能默认是关闭的

```html
<u-keyboard ref="uKeyboard" mode="number" :random="true" v-model="show"></u-keyboard>
```

## 如何控制键盘的打开和关闭？

通过v-model绑定一个值为布尔值的变量控制组件的弹出与收起，v-model的值是双向绑定的。

```html
<template>
	<u-keyboard mode="number" v-model="show"></u-keyboard>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)

// 页面准备完成时触发（相当于 onReady 生命周期）
onMounted(() => {
	// 如果想一进入页面就打开键盘，请在此生命周期调用
	show.value = true
})

// 注意：onLoad 生命周期在 Vue 3 中通常使用 onBeforeMount 或 onMounted 替代
// 如果需要在更早的阶段设置，可以使用 onBeforeMount
</script>
```

## 如何监听键盘按键被点击？

* 输入值是通过组件的`change`事件实现的，组件内部每个按键被点击的时候，组件就会发出一个`change`事件，回调参数为点击的按键的值。
* 通过`backspace`事件监听键盘退格键的点击，通过修改父组件的值实现退格的效果，见下方示例

注意：点击退格键(也即删除键)不会触发`change`事件

```html
<template>
	<u-keyboard mode="number" @change="valChange" @backspace="backspace" v-model="show"></u-keyboard>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
const value = ref<string>('')

// 按键被点击(点击退格键不会触发此事件)
const valChange = (val: string) => {
	// 将每次按键的值拼接到value变量中，注意+=写法
	value.value += val
	console.log(value.value)
}

// 退格键被点击
const backspace = () => {
	// 删除value的最后一个字符
	if (value.value.length) value.value = value.value.substr(0, value.value.length - 1)
	console.log(value.value)
}
</script>
```

## 是否显示遮罩

当您使用键盘时，可能会不想显示遮罩，这时可以配置`mask`参数为`false`即可

```html
<u-keyboard mode="number" v-model="show" :mask="false"></u-keyboard>
```

## API

## Props

注意：props中没有控制键盘弹出与收起的参数，因为这是通过v-model绑定变量实现的，见上方说明。

| 参数      | 说明        | 类型     |  默认值  |  可选值   |
|-----------|-----------|----------|----------|---------|
| mode | 键盘类型，见上方`基本使用`的说明  | String | number | car / card |
| dot-enabled | 是否显示"."按键，只在mode=number时有效 | Boolean  | true | false |
| tooltip | 是否显示键盘顶部工具条 | Boolean  | true | false |
| tips | 工具条中间的提示文字，见上方`基本使用`的说明 | String  | - | - |
| show-tips | 是否显示工具条中间的文字 | Boolean  | true | false |
| cancel-btn | 是否显示工具条左边的"取消"按钮 | Boolean  | true | false |
| confirm-btn | 是否显示工具条右边的"完成"按钮 | Boolean  | true | false |
| mask | 是否显示遮罩 | Boolean  | true | false |
| z-index | 弹出键盘的`z-index`值 | Number | String  | 1075 | - |
| random | 是否打乱键盘按键的顺序 | Boolean  | false | true |
| safe-area-inset-bottom | 是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明) | Boolean  | false | true |
| mask-close-able | 是否允许点击遮罩收起键盘 | Boolean  | true | false |
| confirm-text  | 确认按钮的文字 | String | 取消 | - |
| cancel-text  | 取消按钮的文字 | String | 确认 | - |

## Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 按键被点击(不包含退格键被点击) | 按键的值，见上方说明和示例 | - |
| cancel | 键盘顶部工具条左边的"取消"按钮被点击 | - | - |
| confirm | 键盘顶部工具条右边的"完成"按钮被点击 | - | - |
| backspace | 键盘退格键被点击 | - | - |

## Slot

|名称|说明|版本|
|:-|:-|:-|
| default | 内容将会显示键盘的工具条上面，可以结合[MessageInput 验证码输入](/zh/components/messageInput.html)组件实现类似支付宝输入密码时，上方显示输入内容的功能 |  - |

---

---
url: 'https://uviewpro.cn/zh/components/layout.md'
---
# Layout 布局&#x20;

通过基础的 12 分栏，迅速简便地创建布局

::: warning 注意
如需实现类似宫格的布局，请使用uView的[Grid宫格组件](/zh/components/grid.html)，可以设置角标，功能更完善和灵活
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`col`组件的`span`设置需要分栏的比例

```html
<template>
	<view class="wrap">
		<u-row gutter="16">
			<u-col span="3">
				<view class="demo-layout bg-purple"></view>
			</u-col>
			<u-col span="4">
				<view class="demo-layout bg-purple-light"></view>
			</u-col>
			<u-col span="5">
				<view class="demo-layout bg-purple-dark"></view>
			</u-col>
		</u-row>
		<u-row gutter="16" justify="space-between">
			<u-col span="3">
				<view class="demo-layout bg-purple"></view>
			</u-col>
			<u-col span="9">
				<view class="demo-layout bg-purple-light"></view>
			</u-col>
		</u-row>
	</view>
</template>

<style scoped lang="scss">
	.wrap {
		padding: 24rpx;
	}

	.u-row {
		margin: 40rpx 0;
	}

	.demo-layout {
		height: 80rpx;
		border-radius: 8rpx;
	}

	.bg-purple {
		background: #d3dce6;
	}

	.bg-purple-light {
		background: #e5e9f2;
	}

	.bg-purple-dark {
		background: #99a9bf;
	}
</style>
```

## 分栏间隔

通过设置`row`组件的`gutter`参数，来指定每一栏之间的间隔(最终表现为左边内边距各为gutter/2)，默认间隔为0

```html
<u-row gutter="16">
	<u-col span="3">
		<view class="demo-layout bg-purple">
		</view>
	</u-col>
	<u-col span="9">
		<view class="demo-layout bg-purple-light">
		</view>
	</u-col>
</u-row>
```

## 分栏偏移

通过指定`col`组件的`offset`属性可以指定分栏偏移的栏数。

```html
<u-row gutter="16">
	<u-col span="3">
		<view class="demo-layout bg-purple"></view>
	</u-col>
	<u-col span="3" offset="6">
		<view class="demo-layout bg-purple-light"></view>
	</u-col>
</u-row>
```

## 对齐方式

通过`row`组件的`justify`来对分栏进行灵活的对齐，
可选值为`start`(或`flex-start`)、`end`(或`flex-end`)、`center`、`around`(或`space-around`)、`between`(或`space-between`)，
其最终的表现类似于css的`justify-content`属性。

**注意**：由于持微信小程序编译后的特殊结构，此方式不支持微信小程序。

```html
<u-row gutter="16" justify="center">
	<u-col span="3">
		<view class="demo-layout bg-purple"></view>
	</u-col>
	<u-col span="3">
		<view class="demo-layout bg-purple-light"></view>
	</u-col>
</u-row>
```

## API

## Row Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| gutter | 栅格间隔，左右各为此值的一半，单位rpx  | String | Number | 0 | - |
| justify | 水平排列方式(微信小程序暂不支持)  | String | start(或flex-start) | end(或flex-end) / center / around(或space-around) / between(或space-between) |
| align | 垂直排列方式 | String | center | top / bottom |

## Col Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| span | 栅格占据的列数，总12等分  | String | Number | 0 | 1-12 |
| offset | 分栏左边偏移，计算方式与`span`相同  | String | Number | 0 | - |
| text-align | 文字水平对齐方式  | String | left | center / right |

## Row Events

|事件名|说明|回调参数|
|:-|:-|:-|
| click | `row`被点击 | - |

## Col Events

|事件名|说明|回调参数|
|:-|:-|:-|
| click | `col`被点击，会阻止事件冒泡到`row` | - |

---

---
url: 'https://uviewpro.cn/zh/components/lazyLoad.md'
---
# LazyLoad 懒加载&#x20;

懒加载使用的场景为：页面有很多图片时，APP会同时加载所有的图片，导致页面卡顿，各个位置的图片出现前后不一致等\
本组件高度封装和集成，创新性地使用`uni.createIntersectionObserver`
接口，保证高性能的同时，还有其他友好的可配置参数，比如预加载占位图，加载错误占位图，加载位置参数(threshold)，各种事件等。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`image`参数传入图片的`src`路径即可

:::warning 注意
由于uni-app默认给了image组件的`height`为225px，同时也只有在uni-appimage组件的`mode`参数为`widthFix`时，image才会自动计算出一个高度值
覆盖默认的`height`(225px)。其他`mode`参数下，如果设置`height`为`auto`，或者`100%`的话，图片将会无法显示。

所以：当您使用uView的`lazyload`组件时，如果设置`height`参数为`auto`，或者`100%`，而`img-mode`参数又不为`widthFix`的话，图片将会不显示，这不是uView的BUG。

结论：如果`img-mode`参数不为`widthFix`的话，必须设置`height`参数为一个固定的高度(单位rpx)，否则无效。
:::

```html
<template>
	<view>
		<u-lazy-load v-for="(item, index) in list" :key="index" :image="item.src"></u-lazy-load>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const list = ref<Array<{ src: string }>>([
	{
		src: "https://gtd.alicdn.com/sns_logo/i1/TB124_3NXXXXXasXVXXSutbFXXX.jpg_240x240xz.jpg",
	},
	{
		src: "https://gtd.alicdn.com/sns_logo/i7/TB1IWtgQFXXXXcmXFXXSutbFXXX.jpg_240x240xz.jpg",
	},
	{
		src: "https://gtd.alicdn.com/sns_logo/i1/TB1_f_PLXXXXXbVXpXXSutbFXXX.jpg_240x240xz.jpg",
	},
	{
		// 这里图片不存在，会加载失败，显示错误的占位图
		src: "xxx",
	},
])
</script>
```

## 配置占位图

占位图有两种情况：

* 一种是正常预加载时显示的，通过`loading-img`配置类似"正在加载"的占位图。
* 另一种是图片加载失败(如图片不存在，路径不完整等)，通过`error-img`参数配置类似"图片加载错误"的占位图

```html
<template>
	<view>
		<u-lazy-load :image="image" :loading-img="loadingImg" :error-img="errorImg"></u-lazy-load>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const image = ref<string>("https://gtd.alicdn.com/sns_logo/i1/TB124_3NXXXXXasXVXXSutbFXXX.jpg_240x240xz.jpg")
const loadingImg = ref<string>('/static/uView/loading.png')
const errorImg = ref<string>('/static/uView/load_error.png')
</script>
```

## 图片加载位置

可以通过`threshold`参数设置图片距离屏幕底部多少距离时触发图片加载，单位rpx，说明：

* 如果取负值(如-300)，为尚未到达屏幕底部，距离300rpx时触发
* 如果取正数(如300)，为图片超出屏幕底部300rpx时触发

```html
<u-lazy-load :image="image" threshold="300"></u-lazy-load>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| index | 用户自定义值，在事件触发时回调，用以区分是哪个图片 | String | Number | - | - |
| image | 图片路径 | String | - | - |
| loading-img | 预加载时的占位图 | String | - | - |
| error-img | 图片加载出错时的占位图 | String | - | - |
| threshold | 触发加载时的位置，见上方说明，单位 rpx | String | 100 | - |
| duration | 图片加载成功时，淡入淡出时间，单位ms | String | Number | 500 | - |
| effect | 图片加载成功时，淡入淡出的css动画效果 | String | ease-in-out | linear /  ease / ease-in / ease-out |
| is-effect | 图片加载成功时，是否启用淡入淡出效果 | Boolean | true | false |
| border-radius | 图片圆角值，单位rpx | String | Number | 0 | - |
| height | 图片高度，注意：实际高度可能受`img-mode`参数影响 | String | Number | 450 | - |
| img-mode | 图片的裁剪模式，详见[image组件裁剪模式](https://uniapp.dcloud.io/component/image) | String | Number | widthFix | - |

## Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
|click|点击图片时触发|index：用户通过props传递的`index`值|-|
|load|图片加载成功时触发|index：用户通过props传递的`index`值|-|
|error|图片加载失败时触发|index：用户通过props传递的`index`值|-|

---

---
url: 'https://uviewpro.cn/zh/components/line.md'
---
# Line 线条&#x20;

此组件一般用于显示一根线条，用于分隔内容块，有横向和竖向两种模式，且能设置0.5px线条，使用也很简单。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

组件内部有预置的参数，直接使用即可，有如下几个参数需要了解：

* `color`为线条的颜色
* `direction`为线条的方向，默认为横向
* `hair-line`为是否设置细线条(0.5px)，默认为`true`
* `length`参数需要特别留意，它需要带上单位，比如设置为"50%"，"500rpx"等，在线条为横向时，表现为线条的长度；在线条为竖向时，表现为线条的高度。

```html
<template>
	<u-line color="red" />
	
	/* 等同于 */
	<u-line color="red"></u-line>
</template>
```

## 线条类型

我们可以通过`border-style`参数设置线条的类型，有如下三种可选项：

* `solid`表示实线
* `dashed`表示方形虚线
* `dotted`表示圆点虚线

## 兼容性

由于`头条小程序`的兼容性，如果组件无效的情况下，您可能需要给组件加上`u-line`类，如下：

```html
<u-line class="u-line"></u-line>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| color | 线条的颜色 | String | #e4e7ed | - |
| length | 长度，竖向时表现为高度，横向时表现为长度，可以为百分比，带rpx单位的值等 | String | 100% | - |
| direction | 线条的方向，`row`-横向，`column`-竖向 | String | row | column |
| hair-line | 是否显示细线条 | Boolean  | true | false |
| margin | 线条与上下左右元素的间距，字符串形式，如"30rpx"、"20rpx 30rpx" | String  | - | - |
| border-style | 线条类型，见上方说明 | String  | solid | dashed / dotted |

---

---
url: 'https://uviewpro.cn/zh/components/lineProgress.md'
---
# LineProgress 线形进度条&#x20;

展示操作或任务的当前进度，比如上传文件，是一个线形的进度条。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`percent`设置当前的进度值，该值区间为0-100.
* 通过`active-color`设置进度条的颜色，也可以直接设置`type`主题颜色(优先起作用)，使用预置值

```html
<u-line-progress active-color="#2979ff" :percent="70"></u-line-progress>
```

## 设置进度条动画效果

该效果会在已完成的百分比部分显示移动的条纹(具体见示例效果)

* `striped`参数配置是否显示条纹
* `striped-active`参数配置条纹是否具有动态效果

```html
<u-line-progress :striped="true" :percent="70" :striped-active="true"></u-line-progress>
```

## 设置进度条内部显示百分比值

参数为`show-percent`

* 说明：进度条可以通过`height`设置高度，如果高度太小的话，是无法在内部显示当前的百分比值的

```html
<u-line-progress :percent="70" :show-percent="true"></u-line-progress>
```

## 修改进度条的样式

* `active-color`参数修改激活部分的颜色
* `round`参数设置进度条两端是否为半圆

```html
<u-line-progress :percent="70" :round="false" active-color="#ff9900"></u-line-progress>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| percent | 进度条百分比值，为数值类型，0-100  | String | Number | - | - |
| round | 进度条两端是否为半圆  | Boolean | true | false |
| type | 如设置，`active-color`值将会失效 | String  | - | success / primary / error / info / warning |
| active-color | 进度条激活部分的颜色 | String  | #19be6b | - |
| inactive-color | 进度条的底色，默认为灰色 | String  | #ececec | - |
| show-percent | 是否在进度条内部显示当前的百分比值数值 | Boolean  | true | false |
| height | 进度条的高度，单位rpx | String | Number  | 28 | - |
| striped | 是否显示进度条激活部分的条纹 | Boolean  | false | true |
| striped-active | 条纹是否具有动态效果 | Boolean  | false | true |

## Slots

| 名称 | 说明 |
|:-|:-|
| default | 传入自定义的显示内容，将会覆盖默认显示的百分比值 |

---

---
url: 'https://uviewpro.cn/zh/components/link.md'
---
# Link 超链接&#x20;

该组件为超链接组件，在不同平台有不同表现形式：

* 在APP平台会通过`plus`环境打开内置浏览器
* 在小程序中把链接复制到粘贴板，同时提示信息
* 在H5中通过`window.open`打开链接

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`href`设置打开的链接，`slot`传入显示的内容

```html
<u-link href="https://uviewpro.cn">蜀道难，难于上青天</u-link>
```

## 下划线

通过`under-line`设置是否显示链接的下划线

```html
<u-link href="https://uviewpro.cn" :under-line="true">蒹葭苍苍，白露为霜</u-link>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| color | 文字颜色 | String | #606266 | - |
| font-size | 字体大小，单位rpx | String | Number  | 28 | - |
| under-line | 是否显示下划线 | Boolean  | false | true |
| href | 跳转的链接，要带上http(s) | String  | - | - |
| line-color | 下划线颜色，默认同`color`参数颜色 | String  | - | - |
| mp-tips | 各个小程序平台把链接复制到粘贴板后的提示语 | String  | 链接已复制，请在浏览器打开 | - |
| default-click  | 是否有默认点击事件，不同平台有不同表现形式，如上介绍 | Boolean  | true | false |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| click | `defaultClick`为`false`时，点击组件会发出此事件 | href |  |

---

---
url: 'https://uviewpro.cn/zh/components/loading.md'
---
# Loading 加载动画&#x20;

此组件为一个小动画，目前用在uView的[loadmore加载更多](/zh/components/loadMore.html)和[switch开关](/zh/components/switch.html)等组件的正在加载状态场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`mode`设定动画的类型，`circle`为圆圈的形状，`flower`为经典类似花朵的形状

```html
<template>
	<view>
		<u-loading mode="circle"></u-loading>
		<u-loading mode="flower"></u-loading>
	</view>
</template>
```

## 动画颜色

`color`可以指定动画活动区域的颜色

```html
<u-loading color="red"></u-loading>
```

## 动画尺寸

通过`size`设定尺寸，单位rpx，组件内把`size`值体现为组件的宽和高

```html
<u-loading size="36"></u-loading>
```

## 显示或隐藏动画

通过`show`设置为`true`或`false`，来显示或隐藏动画

```html
<u-loading :show="true"></u-loading>

/* 等价于 */
<u-loading show></u-loading>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| mode | 模式选择，见上方说明  | String | circle | flower |
| color | 动画活动区域的颜色，只对 mode = circle 模式有效  | String	 | #c7c7c7 | - |
| size |加载图标的大小，单位rpx | String | Number  | 34 | - |
| show | 是否显示动画 | Boolean  | true | false |

---

---
url: 'https://uviewpro.cn/zh/components/loadingPopup.md'
---
# LoadingPopup 加载弹窗 &#x20;

`u-loading-popup` 是 uView Pro 提供的弹窗式加载动画组件，常用于页面或局部异步加载、数据请求等待等场景。相比普通的 `u-loading`，它支持遮罩、内容插槽、自动关闭等高级功能。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过 `v-model` 实现弹窗的双向绑定显示，`mode` 设定动画类型（`circle` 圆圈、`flower` 花朵），可自定义内容。

```html
<template>
  <u-loading-popup v-model="show" mode="circle" text="加载中..." />
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  const show = ref(true)
</script>
```

## 方向

可通过 `direction` 属性设置内容方向，可选值有 `vertical`（垂直）和 `horizontal`（水平）。

```html
<template>
  <u-loading-popup
    v-model="show"
    text="正在加载，请稍候..."
    :direction="direction"
  />
</template>
<script setup lang="ts">
  import { ref } from 'vue'
  const show = ref(true)

  const direction = ref<'vertical' | 'horizontal'>('vertical')
</script>
```

## 动画颜色与尺寸

* `color` 设置动画颜色（仅 mode=circle 有效）。
* `size` 设置动画尺寸，单位 rpx。

```html
<u-loading-popup v-model="show" color="#2979ff" size="40" />
```

## 自动关闭与遮罩交互

* `duration` 设置自动关闭时间（ms），默认（设置为 0）表示不自动关闭。
* `cancelTime` 允许点击遮罩关闭的最短时间（ms），默认 10000。
  * 遮罩层点击在 cancelTime 毫秒后可关闭弹窗，触发 cancel 事件。

```html
<u-loading-popup v-model="show" :duration="2000" :cancelTime="5000" />
```

## 事件

* `@cancel` 点击遮罩关闭时触发。

```html
<template>
  <u-loading-popup v-model="show" @cancel="handleCancel" />
</template>
<script setup lang="ts">
  import { ref } from 'vue'
  const show = ref(true)

  function handleCancel() {
    console.log('cancel')
  }
</script>
```

## API

### Props

| 参数       | 说明                       | 类型          | 默认值   | 可选值              |
| ---------- | -------------------------- | ------------- | -------- | ------------------- |
| v-model    | 弹窗显示的双向绑定         | Boolean       | false    | true/false          |
| mode       | 加载动画类型               | String        | circle   | circle/flower       |
| text       | 加载提示文字               | String        | -        | -                   |
| direction  | 内容方向                   | String        | vertical | vertical/horizontal |
| duration   | 自动关闭时间（ms）         | Number        | 0        | -                   |
| cancelTime | 允许点击遮罩关闭的最短时间 | Number        | 10000    | -                   |
| color      | 动画颜色                   | String        | #c7c7c7  | -                   |
| size       | 加载动画尺寸（rpx）        | String/Number | 48       | -                   |

### Events

| 事件名 | 说明             | 回调参数 |
| ------ | ---------------- | -------- |
| cancel | 点击遮罩关闭时触发 | -        |

***

更多用法请参考组件源码和实际业务场景。

---

---
url: 'https://uviewpro.cn/zh/components/loadMore.md'
---
# loadmore 加载更多&#x20;

此组件一般用于标识页面底部加载数据时的状态，共有三种状态：

* 加载前，显示"加载更多"，加入点击可选，是因为数据不够一页时，无法触发页面的`onReachBottom`生命周期
* 加载中，显示"正在加载..."，2种动画可选
* 加载后，如果还有数据，回到"加载前"状态，否则加载结束，显示"没有更多了"

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`status`设置组件的状态，加载前值为`loadmore`，加载中为`loading`，没有数据为`nomore`

注意：以下示例仅为模拟效果，实际中请根据自己的逻辑，修改代码的实现

```html
<template>
	<view class="wrap">
		<view class="item u-border-bottom" v-for="(item, index) in list" :key="index">
			{{'第' + item + '条数据'}}
		</view>
		<u-loadmore :status="status" />
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onReachBottom } from '@dcloudio/uni-app'

// 定义响应式数据
const status = ref<string>('loadmore')
const list = ref<number>(15)
const page = ref<number>(0)

// 页面上拉触底事件处理
onReachBottom(() => {
	if (page.value >= 3) return
	status.value = 'loading'
	page.value = ++page.value
	setTimeout(() => {
		list.value += 10
		if (page.value >= 3) status.value = 'nomore'
		else status.value = 'loading'
	}, 2000)
})
</script>

<style lang="scss" scoped>
.wrap {
	padding: 24rpx;
}

.item {
	padding: 24rpx 0;
	color: $u-content-color;
	font-size: 28rpx;
}
</style>
```

## 控制组件的提示以及动画效果

* 可以通过`icon-type`设置加载中的图标为`flower`或者`circle`，如果不需要图标，可以设置`icon`为`false`
* 可以设置`is-dot`为`true`，在没有数据时，内容显示为一个"●"替代默认的"没有更多了"
* 可以通过配置`load-text`配置提示的文字，该参数为一个对象值，可以修改默认的文字提示，见如下：

```html
<template>
	<u-loadmore :status="status" :icon-type="iconType" :load-text="loadText" />
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// 定义响应式数据
const status = ref<string>('loadmore')
const iconType = ref<string>('flower')

// 使用 reactive 定义 loadText 对象
const loadText = reactive({
	loadmore: '轻轻上拉',
	loading: '努力加载中',
	nomore: '实在没有了'
})
</script>
```

## 手动触发加载更多

有时候可能会因为网络，或者数据不满一页的原因，导致无法上拉触发`onReachBottom`生命周期，这时候(需`status`为`loadmore`状态)，用户点击组件，就会触发`loadmore`
事件，可以在回调中，进行状态的控制和数据的加载，同时也可以修改`loadText`的`loadmore`为"上拉或点击加载更多"进行更加人性化的提示。

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| status | 组件状态  | String | loadmore | loading / nomore |
| bg-color | 组件背景颜色，在页面是非白色时会用到(默认为transparent)  | String	 | #ffffff | - |
| icon | 加载中时是否显示图标  | Boolean | true | false |
| icon-type | 加载中时的图标类型， | String | circle | flower |
| icon-color | `icon-type`为`circle`时有效，加载中的动画图标的颜色  | String | #b7b7b7 | - |
| is-dot |  `status`为`nomore`时，内容显示为一个"●" | Boolean | false | true |
| color | 字体颜色  | String | #606266 | - |
| font-size | 字体大小，单位rpx  | String | Number | 28 | - |
| load-text | 自定义显示的文字，见上方说明示例  | Object | - | - |
| margin-top | 与前一个元素的距离，单位rpx | String | Number  | 0 | - |
| margin-bottom | 与后一个元素的距离，单位rpx | String | Number  | 0 | - |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| loadmore | `status`为`loadmore`时，点击组件会发出此事件 | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/mask.md'
---
# Mask 遮罩层&#x20;

创建一个遮罩层，用于强调特定的页面元素，并阻止用户对遮罩下层的内容进行操作，一般用于弹窗场景

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`show`参数配置是否显示遮罩
* 遮罩被点击时，会发送一个`click`事件，如不需要此事件，请设置`mask-click-able`参数为`false`

```html
<template>
	<u-mask :show="show" @click="show = false"></u-mask>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(true)
</script>
```

## 嵌入内容

通过默认插槽可以在遮罩层上嵌入任意内容\
注意：如果不想让`slot`插槽内容的点击事件冒泡到遮罩，请给指定元素添加上`@tap.stop`

```html
<template>
	<u-mask :show="show" @click="show = false">
		<view class="warp">
			<view class="rect" @tap.stop></view>
		</view>
	</u-mask>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(true)
</script>

<style scoped>
.warp {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 100%;
}

.rect {
	width: 120px;
	height: 120px;
	background-color: #fff;
}
</style>
```

## 遮罩样式

* 通过`duration`设置遮罩淡入淡出的时长，单位`ms`
* 通过`zoom`设置遮罩淡入淡出时是否带有轻微的缩放效果，内部通过`transform: scale(1.2, 1.2)`实现
* 通过`custom-style`传入一个对象，自定义样式，如"{backgroundColor: 'red', color: 'blue'}"

```html
<u-mask :show="show" :duration="400" :zoom="true" :custom-style="{background: 'rgba(0, 0, 0, 0.5)'}"></u-mask>
```

## API

## Props

| 参数      | 说明        | 类型     |  默认值  |  可选值   |
|-----------|-----------|----------|----------|---------|
| show | 是否显示遮罩  | Boolean | false | true |
| z-index | z-index 层级 | String | Number  | 10070 | - |
| duration | 动画时长，单位毫秒 | String | Number  | 300 | - |
| zoom | 是否使用`scale`对遮罩进行缩放 | Boolean  | true | false |
| mask-click-able | 遮罩是否可点击，为`false`时点击不会发送`click`事件 | Boolean  | true | false |

## Events

|事件名|说明|回调参数|
|:-|:-|:-|
| click | `mask-click-able`为`true`时，点击遮罩发送此事件 | - |

## Slot

|名称|说明|
|:-|:-|
| default | 默认插槽，用于在遮罩层上方嵌入内容 |

---

---
url: 'https://uviewpro.cn/zh/tools/md5.md'
---
# md5 加密

该`md5`加密方法，需要手动`import`库函数，调用`md5`方法即可使用，可以对字符串加密为32位的字符串结果，如需进一步了解，
详见[MD5百度百科](https://baike.baidu.com/item/MD5)

使用方法：

```js
import { ref, onMounted } from 'vue';
import md5Libs from "uview-pro/libs/function/md5";

const md5Result = ref('');

onMounted(() => {
  md5Result.value = md5Libs.md5('uView');
  console.log(md5Result.value);
  // 结果为：55c859b4750225eb1cdbd9e0403ee274
});
```

---

---
url: 'https://uviewpro.cn/zh/components/messageInput.md'
---
# MessageInput 验证码输入&#x20;

该组件一般用于验证用户短信验证码的场景，也可以结合uView的[键盘组件](/zh/components/keyboard.html)使用

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`mode`参数模式，可取如下值：
* `box`(默认)-输入位置位一个方框
* `bottomLine`-底部显示一条横线
* `middleLine`-中部显示一条横线

```html
<u-message-input mode="bottomLine"></u-message-input>
```

## 设置最大长度和初始值

* 通过`maxlength`参数配置可输入的方框个数，如5位验证码，该值设置为5即可
* 如果需要显示默认值，请通过`value`参数配置

```html
<u-message-input maxlength="5" value="46821"></u-message-input>
```

## 是否自动获取焦点

如果需要一打开页面，就自动弹出键盘获取焦点，请配置`focus`值为true，否则需要用户手动点击输入区域才能唤起键盘

```html
<u-message-input :focus="true"></u-message-input>
```

## 配置呼吸灯效果

配置`breathe`为`true`，当前激活输入框的样式会有一个类似光标一闪一闪的由浅到深的效果

```html
<u-message-input :breathe="true"></u-message-input>
```

## 用"●"替代输入内容

`dot-fill`参数配置后，输入内容将不可见，用点替代，事件回调中会返回真实值

```html
<u-message-input :dot-fill="true"></u-message-input>
```

## 禁止唤起系统键盘

uView有[键盘](/zh/components/keyboard.html)组件，如果您想结合键盘组件进行自定义的输入效果，就需要设置`disabled-keyboard`为`true`，来保证点击
输入框时不会触发系统自带的键盘，否则会造成冲突。

## 事件回调

* 每当输入内容发生改变，会回调一个`change`事件，内容为当前输入的字符串，如"395"
* 当输入的内容长度(字符个数)达到`maxlength`值后，会触发`finish`事件，同时也会触发`change`事件

```html
<template>
	<view>
		<u-message-input @change="change" @finish="finish"></u-message-input>
	</view>
</template>

<script setup lang="ts">
// 定义 change 事件处理函数
const change = (e: string) => {
	console.log('内容改变，当前值为：' + e)
}

// 定义 finish 事件处理函数
const finish = (e: string) => {
	console.log('输入结束，当前值为：' + e)
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| maxlength | 输入字符个数 | String | Number | 4 | - |
| dot-fill | 是否用圆点填充  | Boolean | false | true |
| mode | 模式选择，见上方"基本使用"说明 | String | box | bottomLine / middleLine |
| value | 预置值 | String | Number | - | - |
| breathe | 是否开启呼吸效果，见上方说明 | Boolean | true | false |
| focus | 是否自动获取焦点 | Boolean | false | true |
| bold | 字体和输入横线是否加粗 | Boolean | true | false |
| font-size | 字体大小，单位rpx | String | Number | 60 | - |
| active-color | 当前激活输入框的样式 | String | #2979ff | - |
| inactive-color | 非激活输入框的样式，文字颜色同此值 | String | #606266 | - |
| width | 输入框的宽度(高等于宽)，单位rpx | String | Number | 80 | - |
| disabled-keyboard | 禁止点击输入框唤起系统键盘 | Boolean  | false | true |

## Events

| 事件名 | 说明 | 回调参数 | 版本 |
| :- | :- | :- | :- |
| change | 输入内容发生改变时触发，具体见上方说明 | value：当前输入的值 | - |
| finish | 输入字符个数达`maxlength`值时触发，见上方说明 | value：当前输入的值 | - |

---

---
url: 'https://uviewpro.cn/zh/components/modal.md'
---
# Modal 模态框&#x20;

弹出模态框，常用于消息提示、消息确认、在当前页面内完成特定的交互操作。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

默认情况下，模态框只有一个`确认`按钮：

* 请至少要配置弹框的内容参数`content`。
* 通过`v-model`绑定一个布尔变量来控制模态框的显示与否。

```html
<template>
	<view>
		<u-modal v-model="show" :content="content"></u-modal>
		<u-button @click="open">
			打开模态框
		</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
const content = ref<string>('东临碣石，以观沧海')

// 定义打开模态框的方法
const open = () => {
	show.value = true
}
</script>
```

## 传入富文本内容

有时候我们需要给模态框的内容，不一定是纯文本的字符串，可能会需要换行，嵌入其他元素等，这时候我们可以使用`slot`功能，再结合uni-app`rictText`组件，
就能传入富文本内容了，如下演示：

```html
<template>
	<view>
		<u-modal v-model="show" :title-style="{color: 'red'}">
			<view class="slot-content">
				<rich-text :nodes="content"></rich-text>
			</view>
		</u-modal>
		<u-button @click="open">
			打开模态框
		</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
const content = ref<string>(`空山新雨后<br>天气晚来秋`)

// 定义打开模态框的方法
const open = () => {
	show.value = true
}
</script>

<style lang="scss" scoped>
.slot-content {
	font-size: 28rpx;
	color: $u-content-color;
	padding-left: 30rpx;
}
</style>
```

## 异步关闭

异步关闭只对"确定"按钮起作用，需要设置`async-close`为`true`，当点击确定按钮的时候，按钮的文字变成一个loading动画，此动画的颜色为
`confirm-color`参数的颜色，同时Modal不会自动关闭，需要手动设置通过`v-model`绑定的变量为`false`来实现手动关闭。

```html
<template>
	<view class="">
		<u-modal v-model="show" @confirm="confirm" ref="uModalRef" :async-close="true"></u-modal>
		<u-button @click="showModal">弹起Modal</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)

// 定义组件引用
const uModalRef = ref<any>(null)

// 定义显示模态框的方法
const showModal = () => {
	show.value = true
}

// 定义确认按钮的回调函数
const confirm = () => {
	setTimeout(() => {
		// 3秒后自动关闭
		show.value = false
		// 如果不想关闭，而单是清除loading状态，需要通过ref手动调用方法
		// uModalRef.value?.clearLoading()
	}, 3000)
}
</script>
```

## 点击遮罩关闭

有时候我们不显示"关闭"按钮的时候，需要点击遮罩也可以关闭Modal，这时通过配置`mask-close-able`为`true`即可

```html
<u-modal v-model="show" :mask-close-able="true"></u-modal>
```

## 控制模态框宽度

可以通过设置`width`参数控制模态框的宽度，此值可以为数值(单位rpx)，百分比，`auto`等。

```html
<u-modal v-model="show" width="70%"></u-modal>
```

## 自定义样式

此组件有完善的自定义功能，可以配置标题，内容，按钮等样式(传入对象形式)，具体参数详见底部的API说明

```html
<u-modal v-model="show" :title-style="{color: 'red'}"></u-modal>
```

## 缩放效果

开启缩放效果，在打开和收起模态框的时候，会带有缩放效果，具体效果请见示例，此效果默认开启，通过`zoom`参数配置

```html
<u-modal v-model="show" :zoom="false"></u-modal>
```

## API

## Props

注意：需要给`modal`组件通过`v-model`绑定一个布尔值，来初始化`modal`的状态，随后该值被双向绑定。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| show | 是否显示模态框，请赋值给`v-model` | Boolean  | false | true |
| z-index | 层级  | String | Number | 1075 | - |
| title | 标题内容  | String | 提示 | - |
| width | 模态框宽度，数值时单位为rpx | String | Number  | 600 | 百分比 / auto |
| content | 模态框内容，如传入`slot`内容，则此参数无效 | String  | 内容 | - |
| show-title | 是否显示标题 | Boolean  | true | false |
| show-confirm-button | 是否显示确认按钮 | Boolean  | true | false |
| show-cancel-button | 是否显示取消按钮 | Boolean  | false | true |
| confirm-text | 确认按钮的文字 | String  | 确认 | - |
| cancel-text | 取消按钮的文字 | String  | 取消 | - |
| cancel-color | 取消按钮的颜色 | String  | #606266 | - |
| confirm-color | 确认按钮的颜色 | String  | #2979ff | - |
| border-radius | 模态框圆角值，单位rpx | String | Number  | 16 | - |
| title-style | 自定义标题样式，对象形式 | Object  | - | - |
| content-style | 自定义内容样式，对象形式 | Object  | - | - |
| cancel-style | 自定义取消按钮样式，对象形式 | Object  | - | - |
| confirm-style | 自定义确认按钮样式，对象形式 | Object  | - | - |
| zoom | 是否开启缩放模式 | Boolean  | true | false |
| async-close | 是否异步关闭，只对确定按钮有效，见上方说明 | Boolean  | false | true |
| mask-close-able | 是否允许点击遮罩关闭Modal | Boolean  | false | true |
| negative-top | 往上偏移的值，以避免可能弹出的键盘重合，单位任意，数值则默认为rpx单位  | String | Number | 0 | - |

## Event

|事件名|说明|回调参数|
|:-|:-|:-|
| confirm | 点击确认按钮时触发 | - |
| cancel | 点击取消按钮时触发 | - |

## Method

此方法需要通过ref调用，详见上方的"异步关闭"

|事件名|说明|
|:-|:-|
| clearLoading | 异步控制时，通过调用此方法，可以不关闭Modal，而单是清除loading状态 |

## Slots

| 名称 | 说明 |
|:-|:-|
| default | 传入自定义内容，一般为富文本，见上方说明 |
| confirm-button | 传入自定义按钮，用于在微信小程序弹窗通过按钮授权的场景 |

---

---
url: 'https://uviewpro.cn/zh/tools/mpShare.md'
---
# mpShare 小程序分享

此功能，是对uni的[onShareAppMessage 生命周期](https://uniapp.dcloud.io/api/plugins/share?id=onshareappmessage)的封装。

这里说的小程序，指的是"微信小程序、百度小程序、头条小程序、QQ小程序，支付宝小程序等"。

由于小程序的分享(微信、头条平台)，需要监听页面的`onShareAppMessage`生命周期，小程序需要在页面声明了此生命周期，点击右上角的"胶囊"才会有分享功能，
而一般情况下，我们希望每个页面都可以分享，那就需要每个页面都写一遍这个生命周期，是很繁琐的。

基于以上，uView通过`mixin`的形式，给每一个页面注入了`onShareAppMessage`生命周期，让您简单引入，无需任何后续操作，即可让每一个页面都有分享功能(仅针对小程序)。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|x|x|√|√|√|√|√|

## 基本使用

需要注意的是，小程序(uni)没有提供类似"getNavigationBarTitle"这样的接口，所以我们无法获取当前页面导航栏的标题，换言之，我们想要每个页面个性化的
分享标题，需要手动设置，否则**默认为小程序的名称**。

:::tip 注意：
分享功能是默认关闭的，但是我们写好各项配置，您只要在`main.js`中引入对应的文件即可，我们没有默认引入，是因为某些用户并不需要此功能。
:::

打开小程序分享功能：

```js
// main.js

// 其他内容

// 引入uView对小程序分享的mixin封装
let mpShare = require('uview-pro/libs/mixin/mpShare.js');
Vue.mixin(mpShare)

// 其他内容
```

分享功能，一般有三个参数，如下：

```js
// 该对象已集成到this.$u中，内部属性如下
uni.$u.mpShare = {
	title: '', // 默认为小程序名称，可自定义
	path: '', // 默认为当前页面路径，一般无需修改，QQ小程序不支持
	// 分享图标，路径可以是本地文件路径、代码包文件路径或者网络图片路径。
	// 支持PNG及JPG，默认为当前页面的截图
	imageUrl: '' 
}
```

以上这些，uView已通过`mixin`集成，当某一个页面您需要自定义分享信息时，可以通过"uni.$u.mpShare"对进行修改，在页面的`onLoad`生命周期修改即可。

```vue
<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'

onLoad(() => {
  uni.$u.mpShare.title = '天苍苍野茫茫，风吹草低见牛羊';
})
</script>
```

## 重写"onShareAppMessage"生命周期

如果您基于自己的一些业务逻辑，需要更加自定义的实现逻辑，可以在页面中重写`onShareAppMessage`生命周期即可覆盖uView通过`mixin`监听的`onShareAppMessage`生命周期。

```vue
<script setup lang="ts">
// 这里如果写成onShareAppMessage: res => { ... }形式的箭头函数，在内部会无法获得this
export function onShareAppMessage(res: any) {
  if (res.from === 'button') {// 来自页面内分享按钮
    console.log(res.target)
  }
  return {
    title: '自定义分享标题',
    path: '/pages/test/test?id=123'
  }
}
</script>
```

## 分享到朋友圈

此功能为微信小程序最新加入的功能，仅适用于微信小程序，uView也全局监听了此生命周期。

同理，你也可以在页面中重写`onShareTimeline`生命周期即可覆盖uView通过`mixin`监听的`onShareTimeline`生命周期。

```vue
<script setup lang="ts">
export function onShareTimeline(res: any) {
  if (res.from === 'button') {// 来自页面内分享按钮
    console.log(res.target)
  }
  return {
    title: '自定义分享标题',
    path: '/pages/test/test?id=123'
  }
}
</script>
```

---

---
url: 'https://uviewpro.cn/zh/components/navbar.md'
---
# Navbar 自定义导航栏&#x20;

此组件一般用于在特殊情况下，需要自定义导航栏的时候用到，一般建议使用 uni-app 带的导航栏。

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

默认情况下，该组件只有向左的箭头，**点击**可以返回上一页，如果您想将自定义导航栏用在 tabbar(不存在要返回的逻辑)页面，应该将`is-back`设置为`false`，
这样会隐藏左边的返回图标区域。

* 如果想在返回箭头的右边自定义类似"返回"字样，可以将`back-text`设置为"返回"，前提是`is-back`要为`true`(默认)
* 通过`title`参数传入需要显示的标题，通过`title-width`(rpx)设置标题区域的宽度，文字超出会通过省略号隐藏
* 通过`is-fixed`配置是否将导航栏固定在顶部

:::tip 说明

* 在小程序中，导航栏会自动适配导航栏右侧的胶囊位置，避开该区域
* 组件底部默认有一条下边框，如您不需要，可以设置`border-bottom`为`false`即可
  :::

```html
<template>
  <view>
    <u-navbar back-text="返回" title="剑未配妥，出门已是江湖"></u-navbar>
    <view class="content">
      <!-- 正文内容 -->
    </view>
  </view>
</template>
```

## 注意事项

既然是要自定义导航栏，那么首先就要取消系统自带的导航栏，需要在 uni-app 目的根目录的"pages.json"中设置，同时在此设置状态栏字体的颜色(H5 无效)，
自定义导航栏后，如果想通过"uni.setNavigationBarColor"动态设置导航栏颜色相关参数，是可能会出问题的，请勿使用此方式。

```js
// pages.json

"pages": [
	// navbar-自定义导航栏
	{
		"path": "/pages/navbar/index",
		"style": {
			"navigationStyle": "custom" ,// 隐藏系统导航栏
			"navigationBarTextStyle": "white" // 状态栏字体为白色，只能为 white-白色，black-黑色 二选一
		}
	}
]
```

## 导航栏高度

可以通过`height`(单位**px**，默认 44，和 uni-app 统导航栏高度一致)配置导航栏的高度，此高度为导航栏内容的高度，不含状态栏的高度，组件内部会自动
加上状态栏的高度，并填充状态栏的占位区域。

注意上方说的 uni-app 方的高度，这里指的是 H5，和 APP。至于各家小程序，由于受导航栏右侧胶囊的影响，目前组件内部给安卓设定的导航栏高度为`48px`，iOS 设定的导航栏高度为`44`，这是结合了大量的
实践的出来的结果，具备完好的兼容性。

## 自定义导航栏内容

一般需要自定义导航栏内部的内容的时候，分几种情况：

* `is-back`为`false`可以去除导航栏左侧默认的返回图标和文字。
* 如有必要，将`title`设置空字符串，同时将会去除导航栏中间显示标题的占位区域。

当将`is-back`设置为`false`，`title`设置为空字符串之后，导航栏将不会有任何默认的内容，您可以通过`slot`传入任意自定义内容，在 APP 和小程序上，导航栏
会自动添加状态栏的占位区域。

**注意：** 通过自定义`slot`传入的内容，为了能在导航栏中垂直居中，您可能需要注意下方示例的 css 的`slot-wrap`类的内容：

```html
<template>
  <view>
    <u-navbar :is-back="false" title="">
      <view class="slot-wrap"> ...... </view>
    </u-navbar>
    <view class="content">
      <!-- 正文内容 -->
    </view>
  </view>
</template>

<style scoped lang="scss">
  .slot-wrap {
    display: flex;
    align-items: center;
    /* 如果您想让slot内容占满整个导航栏的宽度 */
    /* flex: 1; */
    /* 如果您想让slot内容与导航栏左右有空隙 */
    /* padding: 0 30rpx; */
  }
</style>
```

## 自定义导航栏背景颜色

uView 提供了一个`background`参数(需对象形式)，可以自定义导航栏的背景颜色：

* 这个颜色，在 APP 和小程序上，包括状态的颜色在内
* 如果是定义纯色的背景，可以设置`backgroundColor`属性
* 如果是定义渐变的背景，可以设置`backgroundImage`属性
* 如果是定义背景图，可以设置`background`属性，还可以加上其他属性，比如`no-repeat`，`center`等

```html
<template>
  <view>
    <u-navbar :is-back="false" title="" :background="background"> </u-navbar>
    <view class="content">
      <!-- 正文内容 -->
    </view>
  </view>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

// 定义响应式背景数据
const background = reactive({
  backgroundColor: "#001f3f",

  // 导航栏背景图
  // background: 'url(https://cdn.uviewpro.cn/uview/xxx.jpg) no-repeat',
  // 还可以设置背景图size属性
  // backgroundSize: 'cover',

  // 渐变色
  // backgroundImage: 'linear-gradient(45deg, rgb(28, 187, 180), rgb(141, 198, 63))'
})
</script>
```

## API

## Props

|参数|说明|类型|默认值|可选值|
|---|---|---|---|---|
|height|导航栏高度(不包括状态栏高度在内，内部自动加上)，注意这里的单位是**px**|String | Number|44|-|
|back-icon-color|左边返回图标的颜色|String|#606266|-|
|back-icon-name|左边返回图标的名称，只能为 uView 自带的图标|String|nav-back|-|
|back-icon-size|左边返回图标的大小，单位 rpx|String | Number|30|-|
|back-text|返回图标右边的辅助提示文字|String|-|-|
|back-text-style|返回图标右边的辅助提示文字的样式，对象形式|Object|{ color: '#606266' }|-|
|title|导航栏标题，如设置为空字符，将会隐藏标题占位区域|String|-|-|
|title-width|导航栏标题的最大宽度，内容超出会以省略号隐藏，单位 rpx|String | Number|250|-|
|title-color|标题的颜色|String|#606266|-|
|title-size|导航栏标题字体大小，单位 rpx |String | Number|32|-|
|z-index|固定在顶部时的`z-index`值|String | Number|980|-|
|is-back|是否显示导航栏左边返回图标和辅助文字|Boolean|true|false|
|background|导航栏背景设置(APP 和小程序上包括状态栏的颜色)，见上方说明|Object|{ background: '#ffffff' }|-|
|is-fixed|导航栏是否固定在顶部|Boolean|true|false|
|border-bottom|导航栏底部是否显示下边框，如定义了较深的背景颜色，可取消此值|Boolean|true|false|
|custom-back|自定义返回逻辑方法，如传入，点击返回按钮执行函数，否则正常返回上一页，注意模板中不需要写方法参数的括号|Function|-|-|
|immersive|沉浸式，允许 fixed 定位后导航栏塌陷，仅 fixed 定位下生效|Boolean|false|true|
|title-bold|导航栏标题字体是否加粗|Boolean|false|true|

## Slot

|名称|说明|
|---|---|
|default|自定义中间部分的内容|
|left|自定义左侧部分内容|
|right|自定义右侧部分内容|

---

---
url: 'https://uviewpro.cn/zh/components/noNetwork.md'
---
# NoNetwork 无网络提示&#x20;

该组件无需任何配置，引入即可，内部自动处理所有功能和事件，有如下特点：

* 如果没有网络，该组件会以`fixed`定位，并且以很大的`z-index`值覆盖原来的内容。一旦有网络了，会自动隐藏该组件，实现自动化
* 在APP上，嵌入了5+接口，可以直接打开手机的设置页面，方便用户进行网络相关的设置

::: warning 说明

1. 应用有网络时，是不会触发本组件的，为了测试此功能，请关闭手机的数据连接以及WiFi即可
2. 由于普通的组件无法覆盖原生组件，所以本组件不适用那些有`video`，`map`等原生表现的组件的页面，可以自行使用uni的`cover-view`组件修改
   :::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|x|√|

## 基本使用

```html
<template>
	<view>
		<view class="u-text">
			这里是页面正式内容
		</view>
		<u-no-network></u-no-network>
	</view>
</template>

<script setup lang="ts">
// 无网络提示组件无需任何逻辑处理，因此 script setup 块为空
</script>

<style lang="scss" scoped>
.u-text {
	padding-top: 300rpx;
	font-size: 30rpx;
	color: $u-type-primary;
	text-align: center;
}
</style>
```

## 兼容性

* `头条小程序`不支持监听网络状态变化，故本组件不支持`头条小程序`

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| tips | 没有网络时的提示语 | String | 哎呀，网络信号丢失 | - |
| zIndex | 组件的`z-index`值  | String | Number | 10080 | - |
| image | 无网络的图片提示，可用的src地址或base64图片 | String | - | - |

## Events

| 事件名 | 说明 | 回调参数 |
| :- | :- | :- |
| retry | 用户点击页面的"重试"按钮时触发 | - |

---

---
url: 'https://uviewpro.cn/zh/components/noticeBar.md'
---
# NoticeBar 滚动通知&#x20;

该组件用于滚动通告场景，有多种模式可供选择

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`list`数组参数设置需要滚动的内容
* 滚动`mode`参数有两种模式，分别是`horizontal`水平滚动，`vertical`垂直滚动。其中水平滚动又可以通过`is-circular`来配置是衔接滚动(`true`)还是步进滚动(`false`)，
  衔接滚动滚动会把`list`数组元素拼接成一个字符串形式进行滚动，步进滚动模式类似轮播图水平滚动的形式，具体效果请见实例

```html
<template>
	<view>
		<u-notice-bar mode="horizontal" :list="list"></u-notice-bar>
		
		<u-notice-bar mode="horizontal" :is-circular="false" :list="list"></u-notice-bar>
		
		<u-notice-bar mode="vertical" :list="list"></u-notice-bar>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const list = ref<string[]>([
	'寒雨连江夜入吴',
	'平明送客楚山孤',
	'洛阳亲友如相问',
	'一片冰心在玉壶'
])
</script>
```

## 配置主题

* 通过`type`参数可以配置5种主题，即`primary`、`warning`(默认)、`error`、`info`、`success`、`none`

说明：`none`主题默认没有背景颜色

```html
<u-notice-bar type="error" :list="list"></u-notice-bar>
```

## 配置图标

* `volume-icon`参数配置是否显示左侧的音量小喇叭图标，默认显示
* `more-icon`配置是否显示右侧的向右箭头，默认关闭
* `close-icon`配置是否显示关闭的图标，默认关闭

```html
<u-notice-bar :volume-icon="false" :list="list"></u-notice-bar>

<u-notice-bar :more-icon="true" :list="list"></u-notice-bar>

<u-notice-bar :close-icon="true" :list="list"></u-notice-bar>
```

## 配置滚动速度

* `mode`为`vertical`(垂直滚动)，或者`mode`为`horizontal`且`is-circular`为`false`时，两者都可视为"步进"滚动，此时通过`duration`设置滚动周期时长
* `mode`为`horizontal`且`is-circular`为`true`时，可视为"水平衔接滚动"，此时uView加入了一个滚动因子参数，可确保在任意多内容情况下，滚动速度恒定不变，
  可通过`speed`参数配置每秒滚动的距离，单位为`rpx`

```html
<u-notice-bar :mode="vertical" :duration="1500" :list="list"></u-notice-bar>

<u-notice-bar :mode="vertical" :is-circular="false" :duration="1500" :list="list"></u-notice-bar>

<u-notice-bar :mode="vertical" :is-circular="true" :speed="200"  :list="list"></u-notice-bar>
```

## 控制滚动的开始和暂停

* `autoplay`参数默认为`true`，控制是否自动播放滚动通告
* `play-state`参数为`paused`，滚动会暂停，为`play`滚动继续播放

```html
<u-notice-bar :autoplay="true" play-state="paused" :list="list"></u-notice-bar>
```

## 事件回调

* `more-icon`参数为`true`时，点击向右图标会回调一个`getMore`事件
* `close-icon`参数为`true`时，点击关闭箭头图标会触发一个`close`事件
* 点击通告栏的文字时，会触发`click`事件，回调参数为当前文字所在`list`数组参数的索引值

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| list | 滚动内容，数组形式，见上方说明 | Array | - | - |
| type | 显示的主题  | String | warning | primary / info / error / success / none |
| volume-icon | 是否显示小喇叭图标 | Boolean | true | false |
| more-icon | 是否显示右边的向右箭头 | Boolean | false | true |
| close-icon | 是否显示关闭图标 | Boolean | false | true |
| autoplay | 是否自动播放 | Boolean | true | false |
| color | 文字颜色 | String | - | - |
| bg-color | 背景颜色 | String | Number | - | - |
| mode | 滚动模式 | String | horizontal(水平滚动) | vertical(垂直滚动) |
| show | 是否显示 | Boolean | true | false |
| volume-size | 左边喇叭的大小 | String | Number | 34 | - |
| font-size | 字体大小，单位rpx | String | Number | 28 | - |
| duration | 滚动周期时长，只对步进模式有效，横向衔接模式无效，单位ms | String | Number | 2000 | - |
| speed | 水平滚动时的滚动速度，即每秒移动多少距离，只对水平衔接方式有效，单位rpx | String | Number | 160 | - |
| is-circular | `mode`为`horizontal`时，指明是否水平衔接滚动 | Boolean | true | false |
| play-state | 播放状态，play - 播放，paused - 暂停 | String | play | paused |
| disable-touch | 是否禁止通过手动滑动切换通知，只有mode = vertical，或者mode = horizontal且is-circular = false时有效；只支持App 2.5.5+、H5 2.5.5+、支付宝小程序、字节跳动小程序| Boolean | true | false |
| padding | 内置滚动通知的内边距，字符串，类似"16rpx 20rpx" | String | 18rpx 24rpx | - |
| border-radius | 圆角值，单位rpx | String \ Number | 0 | - |
| no-list-hidden | `list`为空数组时，是否显示组件 | Boolean | true | false |

## Events

详细解释见上方说明

| 事件名 | 说明 | 回调参数 | 版本 |
| :- | :- | :- | :- |
| click | 点击通告文字触发，只有mode = vertical，或者mode = horizontal且is-circular = false时有效 | index：当前文字所在`list`数组的索引值 | - |
| close | 点击右侧关闭图标触发 | - | - |
| getMore | 点击右侧向右图标触发 | - | - |
| end | 列表的消息每次被播放一个周期时触发，只有mode = vertical，或者mode = horizontal且is-circular = false时有效 | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/npmSetting.md'
---
# npm 安装方式配置

## 关于 SCSS

uView Pro 依赖 SCSS，您必须要安装此插件，否则无法正常运行。

* 如果您的项目是由`HBuilder X`创建的，相信已经安装 scss 插件，如果没有，请在 HX 菜单的 工具->插件安装中找到"scss/sass 编译"插件进行安装，
  如不生效，重启 HX 即可
* 如果您的项目是由 vue-cli 创建的，请通过以下命令安装对 sass(scss)的支持，如果已安装，请略过。

```bash
# 安装sass
npm i sass -D

# 安装sass-loader
npm i sass-loader -D
```

:::tip 注意
sass、sass-loader 版本过高或过低，导致编译异常，因此推荐统一并锁定依赖版本：

```json
"sass": "1.63.2",
"sass-loader": "10.4.1"
```

:::

## 准备工作

在进行配置之前，请确保您已经根据[安装](install.html)中的步骤对 uView Pro 进行了 npm 安装，如果没有，请先执行安装：

## 1. 引入 uView Pro 主库

在 `main.ts` 中引入并注册 uView Pro：

```js
// main.ts
import { createSSRApp } from 'vue'
// npm 方式
import uViewPro from 'uview-pro'

export function createApp() {
  const app = createSSRApp(App)
  app.use(uViewPro)
  return {
    app
  }
}
```

## 2. 引入全局样式

在 `uni.scss` 中引入主题样式：

```scss
/* uni.scss */
// npm 方式
@import 'uview-pro/theme.scss';
```

在 `App.vue` 首行引入基础样式：

```scss
<style lang="scss">
  // npm 方式
  @import "uview-pro/index.scss";
</style>
```

## 3. 配置 easycom 自动引入组件

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
      // npm 方式
      "^u-(.*)": "uview-pro/components/u-$1/u-$1.vue"
    }
  },
  "pages": [
    // ...
  ]
}
```

:::tip 注意

* 1.修改 `easycom` 规则后需重启 HX 或重新编译项目。
* 2.请确保 `pages.json` 中只有一个 easycom 字段，否则请自行合并多个规则。
* 3.一定要放在 `custom` 内，否则无效。
  :::

## 4. Volar 类型提示支持

如需在 CLI 项目中获得 Volar 的全局类型提示，请在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    // npm 方式
    "types": ["uview-pro/types"]
  }
}
```

> HBuilderX 项目暂不支持 tsconfig.json 的 types 配置，CLI 项目推荐配置以获得最佳 TS 体验。

## 5. 组件使用

配置完成后，无需 import 和 components 注册，可直接在 SFC 中使用 uView Pro 组件：

```vue
<template>
  <u-button type="primary">按钮</u-button>
</template>
```

---

---
url: 'https://uviewpro.cn/zh/components/numberBox.md'
---
# NumberBox 步进器&#x20;

该组件一般用于商城购物选择物品数量的场景

注意：该输入框只能输入大于或等于0的整数，不支持小数输入

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`v-model`绑定`value`初始值，此值是双向绑定的，**无需**在回调中将返回的数值重新赋值给`value`。

```html
<template>
	<u-number-box v-model="value" @change="valChange"></u-number-box>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<number>(0)

// 定义值变化的回调函数
const valChange = (e: { value: number }) => {
	console.log('当前值为: ' + e.value)
}
</script>
```

## 步长设置

* 通过`step`属性设置每次点击增加或减少按钮时变化的值，默认为1

**注意：** `step`参数支持小数值，如`1.1`、`0.3`等

下面示例每次都会加2或者减2

```html
<u-number-box :step="2"></u-number-box>
```

## 限制输入范围

通过`min`和`max`参数限制输的入值最小值和最大值

```html
<u-number-box :min="1" :max="100"></u-number-box>
```

## 禁用状态

通过设置`disabled`参数来禁用输入框，禁用状态下无法点击加减按钮或修改输入框的值

```html
<u-number-box :disabled="true"></u-number-box>
```

## 自定义大小

* 通过`input-width`参数设置输入框的宽度
* 通过`input-height`参数设置输入框和按钮的高度，单位都是rpx

```html
<u-number-box :input-width="100" :input-height="60"></u-number-box>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 输入框初始值 | Number | 1 | - |
| bg-color | 输入框和按钮的背景颜色  | String | #F2F3F5 | - |
| min | 用户可输入的最小值 | Number | 0 | - |
| max | 用户可输入的最大值 | Number | 99999 | - |
| step | 步长，每次加或减的值，支持小数值，如需小数，请设置`positive-integer`为`false` | Number | 1 | - |
| disabled | 是否禁用操作，禁用后无法加减或手动修改输入框的值 | Boolean | false | true |
| size | 输入框文字和按钮字体大小，单位rpx | String | Number | 26 | - |
| color | 输入框文字和加减按钮图标的颜色 | String | #323233 | - |
| input-width | 输入框宽度，单位rpx | String | Number | 80 | - |
| input-height | 输入框和按钮的高度，单位rpx | String | Number | 50 | - |
| index | 事件回调时用以区分当前发生变化的是哪个输入框 | String | Number | - | - |
| disabled-input | 是否禁止输入框手动输入值 | Boolean | false | true |
| cursor-spacing | 指定光标于键盘的距离，避免键盘遮挡输入框，单位rpx | String | Number | 200 | - |
| long-press | 是否开启长按连续递增或递减 | Boolean | true | false |
| press-time  | 开启长按触发后，每触发一次需要多久，单位ms | String | Number | 250 | - |
| positive-integer | 是否只能输入正整数 | Boolean | true | false |

## Events

| 事件名 | 说明 | 回调参数 | 版本 |
| :- | :- | :- | :- |
| change | 输入框内容发生变化时触发，对象形式 | value：输入框当前值，index：通过props传递的`index`值 | - |
| blur | 输入框失去焦点时触发，对象形式 | value：输入框当前值，index：通过props传递的`index`值 | - |
| minus | 点击减少按钮时触发(按钮可点击情况下)，对象形式 | value：输入框当前值，index：通过props传递的`index`值 | - |
| plus | 点击增加按钮时触发(按钮可点击情况下)，对象形式 | value：输入框当前值，index：通过props传递的`index`值 | - |
| blur  | 输入框失去焦点时触发，对象形式 | value：输入框当前值，index：通过props传递的`index`值 | - |

---

---
url: 'https://uviewpro.cn/zh/components/nvue.md'
---
# Nvue 特性相关

前言：uView 在 1.x 版本，只有部分组件支持`nvue`，不推荐在`nvue`项目中使用，uView Pro 也不建议在`nvue`项目中使用，我们在这里做一个专题，列出一些`nvue`上的坑，希望能帮助到您。

## Text 组件

* 我们在`vue`中，可以将文本相关的内容放到`view`或者`text`组件，这都是没问题的，但是在`nvue`中，需要动态响应(双向绑定)的内容，必须放在`text`标签，如果放在`view`可以正常显示，但是无法双向绑定。

* 在`nvue`中，文本的样式无法继承父元素的颜色(color)，必须具体到给每一个`text`元素定义类名，在通过指定的类名给赋予颜色值，其他类似出现不能继承父组件的情况，也可参考此做法。

* 在`nvue`中，`text`组件不能换行写内容，否则会出现无法去除的周边空白内容(类似被加上了`padding`或者`margin`的效果)，如下：

```html
<!-- nvue中错误写法 -->
<text> 桃花潭水深千尺 </text>

<!-- nvue中正确写法 -->
<text>不及汪伦送我情</text>
```

## 事件冒泡

`weex`事件冒泡相关文档 —— [事件冒泡](https://weex.apache.org/zh/docs/events/event-bubbling.html#%E9%98%BB%E6%AD%A2%E5%86%92%E6%B3%A1)

在`weex`原文中，需要给给页面(组件)根元素设置`bubble="true"`才能产生事件冒泡机制，但是在`uni-app`的`nvue`中，已自动加上类似`bubble="true"`的操作，无需用户额外干预，自动就会获得事件冒泡的机制。另外，在 nvue 中，我们可以通过如下方式阻止事件冒泡：

```html
<template>
    <view @tap="parentClick">
        <text @tap="childClick">点击我</text>
    </view>
</template>

<script setup lang="ts">
// 定义子元素点击事件处理函数
const childClick = (e: Event) => {
    console.log('内部被点击')
    e.stopPropagation()
}

// 定义父元素点击事件处理函数
const parentClick = () => {
    console.log('父元素将不会捕获冒泡事件')
}
</script>
```

## line-height

在`nvue`中，`line-height`与字体大小`font-size`无关，如果赋予数值，单位默认为`px`，这意味着不可以如下使用：

```css
.box {
  /* vue正常，nvue中会导致行高只有1px */
  line-height: 1;
}
```

## 样式穿透

在`weex`(`nvue`)中有如此描述：[在 Weex 里， 每一个 Vue 组件的样式都是 scoped](https://weex.apache.org/zh/guide/use-vue-in-weex.html#%E5%B9%B3%E5%8F%B0%E7%9A%84%E5%B7%AE%E5%BC%82)，这说明`vue`中的的`/deep/`和`:deep`在`nvue`中都是无效，修改子组件样式只能通过传参进行，而不能进行样式穿透。

## 字体引入不能加引号

`nvue`下，`font-family`的字体引入，不能加引号，否则会导致字体图标无法显示，如下：

```css
/* 错误写法 */
font-family: "uicon-iconfont";

/* 正确写法 */
font-family: uicon-iconfont;
```

## Scss 中的:export 无效

在`vue`中，我们可以通过`*.scss`中使用[:export](https://www.jianshu.com/p/069f4f79de16)进行变量导出，供`js`和`css`共同使用变量，但是`nvue`中不支持此写法，请勿使用。

## transition 属性不能简写

在`vue`中，我们可以很方便的简写`transition`属性，但是`nvue`中，必须分开写才有效，如下：

* [weex 文档关于 transition 的描述](https://weex.apache.org/zh/docs/styles/common-styles.html#transition)

```css
/* 如下写法，vue有效，nvue无效 */
transition: opacity 0.3s ease-in;

/* nvue页面需要拆分成如下写法 */
transition-property: opacity;
transition-duration: 0.3s;
transition-timing-function: ease-in;
```

## box-shadow

据关于[weex 关于 box-shadow 文档](https://weex.apache.org/zh/docs/styles/common-styles.html#%E9%98%B4%E5%BD%B1-box-shadow)描述，`weex`不支持`android`上的`box-shadow`属性，但是经实测，在`nvue`(uni-app 改良后台的`weex`)上`android`，是支持的`box-shadow`属性效果的。

需要说明的是，在`IOS`上，目前(2020-10-30)不允许将`box-shadow`值设置为`none`，否则会出现锐利的高亮白色边框，由于`nvue`支持`rgba`透明度，我们可以通过如下方式实现类似`none`的效果：

```css
.box {
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
}
```

## border-radius

[在`weex`文档中有明确的说明](https://weex.apache.org/zh/docs/styles/common-styles.html#border-radius)，`border-radius`支持简写形式，但是在`nvue`的`android`端，`border-radius`必须分开写才有效，如下：

```css
/* nvue下，安卓不支持此写法 */
.box {
  border-radius: 10px;
}

/* 必须如下写法才能兼容 */
.box {
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
```

## 关于\<template/> 和 \<block/>

以下文字取自 uni-app 文档原文，[点此查看](https://uniapp.dcloud.io/frame?id=template-block)：

```
`<template/>` 和 `<block/>` 并不是一个组件，它们仅仅是一个包装元素，不会在页面中做任何渲染，只接受控制属性。
`<block/>` 在不同的平台表现存在一定差异，推荐统一使用 `<template/>`。
```

上面说，二者不会在页面做任何的渲染，但是在`nvue`中，`<block/>`确确实实被渲染成为一个`<block/>`元素，由于`nvue`默认`flex`布局，且为
`column`竖向布局，这可能会导致`<block/>`标签下存在多个其他元素时，这些元素会竖向排列，您不得不额外对`<block/>`元素设置样式，所以我们建议只要是`nvue`的场景，一律使用`<template/>`而不是`<block/>` 标签

---

---
url: 'https://uviewpro.cn/zh/components/intro.md'
---
# Overview 组件总览

以下为 uView Pro 所有组件分组总览，搜索组件名称后可跳转至详细文档：

---

---
url: 'https://uviewpro.cn/zh/components/pagination.md'
---
# Pagination 分页 &#x20;

分页组件（Pagination）用于在数据量较大的情况下，将数据进行分页，并允许用户进行主动点击跳转。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本用法

```html
<u-pagination v-model="current" :total="21"></u-pagination>
```

## 使用图标

```html
<u-pagination v-model="current1" :total="35" show-icon></u-pagination>
```

## 自定义图标（仅支持内置图标）

```html
<u-pagination
    v-model="current2"
    :total="49"
    show-icon
    prev-icon="arrow-left-double"
    next-icon="arrow-right-double"
></u-pagination>
```

## 触发 change 事件

```html
<template>
  <u-pagination v-model="current3" :total="50" @change="handleChange"></u-pagination>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { $u } from 'uview-pro'
import type { PaginationChangePayload } from 'uview-pro/types/global';

const current3 = ref(1);

// 触发 change 事件
function handleChange(val: PaginationChangePayload) {
    $u.toast(`触发器被点击：${val.type}`);
}
```

## API

## Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|:- |:- |:- |:-: |:-: |
| prevText | 左侧按钮文字 | String | 上一页 | - |
| nextText | 右侧按钮文字 | String | 下一页 | - |
| total | 总条目数 | Number | Number | - |
| pageSize | 每页数据量 | Number | 10 | - |
| showIcon | 是否以 icon 形式展示按钮 | Boolean | false | - |
| prevIcon | 左侧按钮图标，仅支持内置图标 | String | arrow-left | - |
| nextIcon | 右侧按钮图标，仅支持内置图标 | String | arrow-right | - |

## Events

| 事件名 | 说明 | 回调参数 |
|:-|:-|:-|
| change | 切换分页事件 | `{ type: string, current: number }` current 为当前页，type 值为：next/prev，表示点击的是上一页还是下一页 |

## Slots

| 名称 | 说明 |
|:-|:-|
| default | 分页内容 |

---

---
url: 'https://uviewpro.cn/zh/components/picker.md'
---
# Picker 选择器&#x20;

此选择器有四种弹出模式

1. 一是时间模式，可以配置年，日，月，时，分，秒参数
2. 二是地区模式，可以配置省，市，区参数
3. 三是单列模式
4. 四是多列模式

::: warning 说明
不再建议使用此组件的单列和多列模式，因为已经有更友好，简单易用，专门用于处理列选择的[Select 列选择器](/zh/components/select.html)组件，
以后此组件将专注于时间和地区的选择。
:::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`mode`参数设置为`time`、`region`、`selector`、`multiSelector`，区分时间、地区、单列，多列模式。
* 通过v-model双向绑定一个值为布尔值的变量，来打开或者收起picker。

```html
<template>
	<view>
		<u-picker v-model="show" mode="time"></u-picker>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
</script>
```

## 一、时间和地区模式

### 1. 设置默认值

* 如果`mode`为`time`，可以通过`default-time`参数设置打开时的默认时间，格式如"2025-07-02 13:01:00"、"2025-07-02 13:01"
* 如果`mode`为`region`，可以通过`default-region`(Array格式)中文的省市区名称，如：`["河北省", "秦皇岛市", "北戴河区"]`，或者代号的
  省市区，如：`["13", "1303", "130304"]`。

**注意**：这些省市区的名称和代码，须是uView的`Picker`组件自身提供的，否则可能无法匹配

```html
<template>
	<u-picker mode="time" v-model="show"></u-picker>
	
	<u-picker mode="region" v-model="show" :area-code='["13", "1303", "130304"]'></u-picker>
</template>
```

### 2. 设置需要显示的参数

* 时间模式时：通过`params`参数传入一个对象给组件，给需要显示的参数属性置为`true`，可选的参数有：`year`、`month`、`day`、`hour`、`minute`、`second`。
  其中，`hour`、`minute`、`second`值默认为`false`，其他值默认为`true`
* 地区模式时：可选的参数有：`province`、`city`、`area`，默认都为`true`

下方示例时间模式，只会显示年，月，日3个参数可供选择：

```html
<template>
	<u-picker mode="time" v-model="show" :params="params"></u-picker>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)

// 定义响应式参数对象
const params = reactive({
	year: true,
	month: true,
	day: true,
	hour: false,
	minute: false,
	second: false
})
</script>
```

### 3. 回调参数

当点击`picker`的"取消"或者"确定"按钮时，会分别产生回调事件`cancel`和`confirm`，均为会返回组件内部的当前值。回调的参数为一个对象，属性和传递给`picker`组件的`params`对象为`true`的属性一致。

注意：`mode`为`region`时，回调对象属性为一个对象，分别有`label`和`value`属性，见如下说明：

```js
// 组件内部parmas参数默认值：
let params = {
	year: true,
	month: true,
	day: true,
	hour: false,
	minute: false,
	second: false,
	province: true,
	city: true,
	area: true,
	timestamp: true,
}


// 如果params值如下(时间选择模式)：：
let params = {
	year: true,
	month: true,
	day: true,
	hour: false,
	minute: false,
	second: false,
	// 选择时间的时间戳
	timestamp: true,
}

// 那么回调的参数可能如下：
{
	year: '2020',
	month: '05',
	day: '10'
}


// 如果params值如下(地区选择模式)：
let params = {
	province: true,
	city: true,
	area: true
}

// 那么回调的参数可能如下：
{
	area: {
		label: "宝安区",
		value: "440306"
	},
	city: {
		label: "深圳市",
		value: "4403"
	},
	province: {
		label: "广东省",
		value: "44"
	},
}
```

## 二、单列和多列模式

**不再建议使用此组件的单列和多列模式，因为已经有更友好，简单易用，专门用于处理列选择的[Select 列选择器](/zh/components/select.html)组件。**

### 1. 设置默认值

* 如果`mode`为`selector`(单列)，可以通过设置`default-selector`为单元素的数组，表示选中单列中的第几个(索引从0开始)，如: `[1]`表示选中单列的第二个。
* 如果`mode`为`multiSelector`(多列)，可以通过设置`default-selector`为多元素的数组(元素数量等于列数)，分别表示选中每一列的第几个(索引从0开始)，如`[0, 1, 2]`
  表示共有3列，分别选中第一列的第一个，第二列的第二个，第三列的第三个。

```html
<template>
	<u-picker mode="selector" v-model="show"  :default-selector="[0]"></u-picker>
	
	<u-picker mode="multiSelector" v-model="show"  :default-selector='[0, 1, 3]'></u-picker>
</template>
```

### 2. 设置数据

由于单列和多列模式不像时间和地区模式，没有内置数据，故需要您手动传入可选值，通过`range`参数(数组)传入对应的数据，单列时为一维数组，多列时为二维数组。

如果您数组中的元素为对象的话，可以通过指定`range-key`参数，让组件内部知道您想把对象的哪个属性当做要显示的值。

```html
<template>
	<view class="">
		<u-picker mode="selector" v-model="show" :default-selector="[0]" :range="selector"></u-picker>
		
		<u-picker mode="selector" v-model="show" :default-selector="[0]" :range="selectorObj" range-key="cateName"></u-picker>
		
		<u-picker mode="multiSelector" v-model="show" :default-selector="[0, 1]" :range="multiSelector"></u-picker>
	</view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// 定义响应式数据
const show = ref<boolean>(true)

// 定义选择器数据
const selector = ref<number[]>([1, 2, 3])

// 定义多列选择器数据
const multiSelector = ref<number[][]>([
	[1, 2, 3], 
	[4, 5, 6]
])

// 定义对象选择器数据
const selectorObj = reactive([
	{
		cateName: '1',
		id: 1
	},
	{
		cateName: '2',
		id: 2
	}
])
</script>
```

### 3. 回调参数

当点击`picker`的"取消"或者"确定"按钮时，会分别产生回调事件`cancel`和`confirm`，均为会返回组件内部的当前值。回调的参数为一个数组，分别表示
当前各列选中的列索引值(从0开始)。

* 单列模式

回调参数可能为`[3]`，表示选中传入数组的第四个值(从0开始)

* 多列模式

回调参数可能为`[1, 0, 3]`，表示3列中，第一列选中了第二个值，第二列选中了第一个值，第三列选中了第四个值。

其中，我们使用多列模式，一般都需要联动选择，在多列模式下，有一个`columnchange`事件，任意列改变都会触发该事件，回调参数为`{column: column, index: index}`，
`column`表示第几列发生了变化(从0开始)，`index`表示当前的下标值，如`{column: 1, index: 2}`表示第二列(从0开始)发生了变化，下标变成了`2`，您可以
根据这个回调，对应的修改`default-selector`参数，让多列中的其他列联动起来。

此处演示较为复杂，请见uView的演示代码，在[安装](/zh/components/install.html)页下载`演示项目`方式，内有所有演示的示例，是一个完整的HX工程。

## API

## Props

注意：props中没有控制Picker打开与收起的参数，因为这是通过v-model绑定变量实现的，见上方说明。

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|:-|:-|:-|:-|:-|
| params | 需要显示的参数，见上方说明，mode=region或mode=time时有效 | `Object` | - | - |
| mode | 模式选择 | `String` | `time` | `region` / `selector` / `multiSelector` |
| start-year | 可选的开始年份，mode=time时有效 | `String \| Number` | `1950` | - |
| end-year | 可选的结束年份，mode=time时有效 | `String \| Number` | `2050` | - |
| safe-area-inset-bottom | 是否开启底部安全区适配 | `Boolean` | `false` | `true` |
| cancel-color | 取消按钮的颜色 | `String` | `#606266` | - |
| confirm-color | 确认按钮的颜色 | `String` | `#2979ff` | - |
| default-time | 默认选中的时间，mode=time时有效，需在`onReady`生命周期赋值 | `String` | - | - |
| default-region | 默认选中的地区，中文形式，mode=region时有效，需在`onReady`生命周期赋值 | `Array` | - | - |
| area-code | 默认选中的地区，编号形式，mode=region时有效 | `Array` | - | - |
| default-selector | 数组形式，表示选择`range`对应项的索引，见上方说明 | `Array` | `[]` | - |
| mask-close-able | 是否允许通过点击遮罩关闭Picker | `Boolean` | `true` | `false` |
| show-time-tag | 时间模式时，是否显示后面的年月日中文提示 | `Boolean` | `true` | `false` |
| z-index | 弹出时的z-index值 | `String \| Number` | `10075` | - |
| range | 自定义选择的数据，mode=selector或mode=multiSelector时有效 | `Array` | `[]` | - |
| range-key | 当`range`参数的元素为对象时，指定要显示的key值 | `String` | - | - |
| title | 顶部中间的标题 | `String` | - | - |
| confirm-text | 确认按钮的文字 | `String` | `确认` | - |
| cancel-text | 取消按钮的文字 | `String` | `取消` | - |
| preserve-selection | 是否保留用户上次确认的选择 | `Boolean` | `true` | `false` |

## Events

| 事件名 | 说明 | 回调参数 | 版本 |
|:-|:-|:-|:-|
| confirm | 点击确定按钮，返回当前选择的值 | `Object` | - |
| cancel | 点击取消按钮，返回当前选择的值 | `Object` | - |
| columnchange | 列改变时触发(仅mode=multiSelector) | `{column, index}` | - |

---

---
url: 'https://uviewpro.cn/zh/components/popup.md'
---
# Popup 弹出层&#x20;

弹出层容器，用于展示弹窗、信息提示等内容，支持上、下、左、右和中部弹出。组件只提供容器，内部内容由用户自定义

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 弹出层的内容通过`slot`传入，由用户自定义
* 通过`v-model`绑定一个布尔值的变量控制弹出层的打开和收起

```html
<template>
	<view>
		<u-popup v-model="show">
			<view>出淤泥而不染，濯清涟而不妖</view>
		</u-popup>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
</script>
```

## 设置弹出层的方向

* 可以通过`mode`参数设置，可以设置为`left`、`top`、`right`、`bottom`、`center`

```html
<template>
	<u-popup v-model="show" mode="top">
		<view>
			人生若只如初见，何事秋风悲画扇
		</view>
	</u-popup>
</template>
```

## 设置弹出层的圆角

可以给`border-radius`设置一个值来给弹窗增加圆角，单位rpx。

```html
<template>
	<u-popup v-model="show" mode="top" border-radius="14">
		<view>
			人生若只如初见，何事秋风悲画扇
		</view>
	</u-popup>
</template>
```

## 控制弹窗的宽度 | 高度

这里说的宽度，指的是左边，右边，中部弹出的场景，高度指的是顶部和底部弹出的场景(因为这两个场景宽度都是100%)。\
uView提供了`length`来控制此种情况，此值可以是`数值`(单位rpx)，`auto`，`百分比`等，内部会自动处理对应的逻辑。
如果为`auto`的时候，表示弹窗的宽度 | 高度由内容撑开。

**`width`和`height`参数：**

优先推荐`width`和`height`参数，并且优先级会高于`length`，这3个参数都可以设置`百分比`、`auto`、`数值`(单位rpx)、或者是带`px`和`rpx`单位的字符串：

* `width`只对`mode = left | center | right`模式有效
* `height`只对`mode = top | center | bottom`模式有效

:::tip 提示
内置了`scroll-view`元素，内如内容超出容器的高度，将会自动获得**垂直**滚动的特性，如果您因为在`slot`内容做了滚动的处理，而造成了
冲突的话，请移除自定义关于滚动部分的逻辑。
:::

```html
<template>
	<u-popup v-model="show" mode="top" length="60%">
		<view>
			等闲变却故人心，却道故人心易变
		</view>
	</u-popup>
	
	<u-popup v-model="show" mode="center" width="500rpx" height="600px">
		<view>
			骊山语罢清宵半，泪雨霖铃终不怨
		</view>
	</u-popup>
</template>
```

## 内容局部滚动

如果您需要让弹窗中的内容局部滚动，局部固定，比如商城底部弹出SKU选择的场景，可以按如下思路进行处理：

1. 在弹窗内容中放一个`scroll-view`组件，设置为竖向滚动，并指定高度(必须)
2. 在`scroll-view`组件下方放一块无需滚动内容，如下：

```html
<template>
	<view class="">
		<u-button @click="show = true">打开弹窗</u-button>
		<u-popup mode="bottom" v-model="show">
			<view class="content">
				<scroll-view scroll-y="true" style="height: 300rpx;">
					<view>
						<view v-for="index in 20" :key="index">
							第{{index}}个Item
						</view>
					</view>
				</scroll-view>
				<view class="confrim-btn">
					<u-button @click="show = false">确定</u-button>
				</view>
			</view>
		</u-popup>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const show = ref<boolean>(false)
</script>

<style lang="scss" scoped>
.content {
	padding: 24rpx;
	text-align: center;
}
</style>
```

## API

## Props

注意：props中没有控制弹窗打开与收起的参数，因为这是通过v-model绑定变量实现的，见上方说明。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| mode | 弹出方向  | String	 | left | top / right / bottom / center |
| mask | 是否显示遮罩  | Boolean | true | false |
| length | mode=left | 见上方说明 | String | Number | auto | - |
| zoom | 是否开启缩放动画，只在`mode`为`center`时有效  | Boolean | true | false |
| safe-area-inset-bottom | 是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明) | Boolean  | false | true |
| mask-close-able | 点击遮罩是否可以关闭弹出层  | Boolean | true | false |
| border-radius | 弹窗圆角值  | Number | String | 0 | - |
| z-index | 弹出内容的`z-index`值  | Number | String | 10075 | - |
| closeable | 是否显示关闭图标  | Boolean | false | true |
| close-icon | 关闭图标的名称，只能uView的内置图标  | String | close | - |
| close-icon-pos | 自定义关闭图标位置，top-left为左上角，top-right为右上角，bottom-left为左下角，bottom-right为右下角  | String | top-right | top-left / bottom-left / bottom-right |
| close-icon-color | 关闭图标的颜色  | String | #909399 | - |
| close-icon-size | 关闭图标的大小，单位rpx  | String | Number | 30 | - |
| width  | mode = left | center | right时有效，优先级高于`length`  | String | Number | - | - |
| height  | mode = top | center | bottom时有效，优先级高于`length`  | String | Number | - | - |
| negative-top | 中部弹出时，以避免可能弹出的键盘重合，往上偏移的值，单位任意，数值则默认为rpx单位  | String | Number | 0 | - |
| mask-custom-style | 遮罩自定义样式，一般用于修改遮罩透明度对象形式，如：`{background: 'rgba(0, 0, 0, 0.5)'}`  | Object | - | - |
| duration  | 遮罩打开或收起的动画过渡时间，单位ms | String | Number | 250 | - |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| open | 弹出层打开 | - | - |
| close | 弹出层收起 | - | - |

---

---
url: 'https://uviewpro.cn/zh/tools/queryParams.md'
---
# queryParams 对象转URL参数

该方法，可以将一个对象形式参数转换成`get`传参所需参数形式，如把`{name: 'lisa', age: 20}`转换成`?name=lisa&age=20`\
用途：可以用于`uni.navigateTo`接口传参等场景，无需自己手动拼接`URL`参数

### queryParams(data, isPrefix = true, arrayFormat = 'brackets')

* `data` \<Object> 对象值，如`{name: 'lisa', age: 20}`
* `isPrefix` \<Boolean> 是否在返回的字符串前加上"?"，默认为`true`
* `arrayFormat` \<Boolean> 属性为数组的情况下的处理办法，默认为`brackets`，见后面说明

```js
import { ref, onMounted } from 'vue';

const queryParams = ref({
  name: 'lisa',
  age: 20
});

onMounted(() => {
  console.log(uni.$u.queryParams(queryParams.value));
  // 结果为：?name=lisa&age=20
});
```

### arrayFormat参数说明

如果您传入的`data`对象内部某些属性值为数组的情况下，您可能需要留意这个参数的配置：\
该参数可选值有4个：`indices`，`brackets`，`repeat`，`comma`，具体效果请见下方的演示说明

```js
import { ref, onMounted } from 'vue';

const queryParams = ref({
  name: '冷月夜',
  fruits: ['apple', 'banana', 'orange']
});

onMounted(() => {
  console.log(uni.$u.queryParams(queryParams.value, true, 'indices'));
  // 结果为：?name=冷月夜&fruits[0]=apple&fruits[1]=banana&fruits[2]=orange
  
  console.log(uni.$u.queryParams(queryParams.value, true, 'brackets'));
  // 结果为：?name=冷月夜&fruits[]=apple&fruits[]=banana&fruits[]=orange
  
  console.log(uni.$u.queryParams(queryParams.value, true, 'repeat'));
  // 结果为：?name=冷月夜&fruits=apple&fruits=banana&fruits=orange
  
  console.log(uni.$u.queryParams(queryParams.value, true, 'comma'));
  // 结果为：?name=冷月夜&fruits=apple,banana,orange
});
```

---

---
url: 'https://uviewpro.cn/zh/components/radio.md'
---
# Radio 单选框&#x20;

单选框用于有一个选择，用户只能选择其中一个的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 该组件需要搭配`radioGroup`组件使用，以便用户进行操作时，获得当前单选框组的选中情况，当然，您也可以单独对某个`radio`进行事件监听
* 通过`v-model`给`radioGroup`组件绑定一个变量，这个绑定的变量是双向的(初始值只能是`true`或者`false`)，也就是说，您可以无需监听`radio`或者`radioGroup`组件的`change`事件，也能知道哪个
  被勾选了

**注意：** 由于`radio`组件需要由`radioGroup`组件提供参数值，这些父子组件间通过Vue的"provide/inject"特性注入依赖，
所以您必须使用`radioGroup`包裹`radio`组件才能正常使用。

```html
<template>
	<view class="">
		<u-radio-group v-model="value" @change="radioGroupChange">
			<u-radio 
				@change="radioChange" 
				v-for="(item, index) in list" :key="index" 
				:name="item.name"
				:disabled="item.disabled"
			>
				{{item.name}}
			</u-radio>
		</u-radio-group>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义列表数据接口
interface RadioItem {
	name: string
	disabled: boolean
}

// 定义响应式数据
const list = ref<RadioItem[]>([
	{
		name: 'apple',
		disabled: false
	},
	{
		name: 'banner',
		disabled: false
	},
	{
		name: 'orange',
		disabled: false
	}
])

const value = ref<string>('orange')

// 定义事件处理函数
const radioChange = (e: any) => {
	// console.log(e);
}

const radioGroupChange = (e: any) => {
	// console.log(e);
}
</script>
```

## 禁用radio

设置`disabled`为`true`，即可禁用某个组件，让用户无法点击，禁用分为两种状态，一是未勾选前禁用，这时只显示一个灰色的区域。二是已勾选后
再禁用，会有灰色的勾选的图标，但此时依然是不可操作的。

```html
<u-radio-group v-model="value">
	<u-radio :disabled="true">明月几时有</u-radio>
</u-radio-group>
```

## 自定义形状

可以通过设置`shape`为`square`或者`circle`，将单选框设置为方形或者圆形

```html
<u-radio-group v-model="value">
	<u-radio shape="circle">月明人倚楼</u-radio>
</u-radio-group>
```

## 自定义颜色

此处所指的颜色，为`radio`选中时的背景颜色，参数为`active-color`

```html
<u-radio-group v-model="value">
	<u-radio active-color="red">思悠悠，恨悠悠，恨到归时方始休</u-radio>
</u-radio-group>
```

## 文本是否可点击

设置`label-disabled`为`true`，点击文本时，无法操作`radio`

```html
<u-radio-group v-model="value">
	<u-radio :label-disabled="false">门掩黄昏，无计留春住</u-radio>
</u-radio-group>
```

## API

## Radio Props

注意：`radio`和`radio-group`二者同名参数中，`radio`的参数优先级更高。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| icon-size | 图标大小，单位rpx  | String | Number | - | - |
| label-size | label字体大小，单位rpx  | String | Number | - | - |
| name | `radio`组件的标示符  | String | Number | - | - |
| shape | 形状，见上方说明 | String  | - | circle / square |
| disabled | 是否禁用 | Boolean  | - | false / true |
| label-disabled | 是否禁止点击文本操作`radio` | Boolean  | - | true / false |
| active-color | 选中时的颜色，如设置`radioGroup`的`active-color`将失效 | String  | - | - |

## radioGroup Props

注意：需要给`radioGroup`组件通过`v-model`绑定一个**变量**，来初始化`radio`的状态，随后该值被双向绑定，
当用户勾单选框时，该值在`radio`内部被修改为`name`值，并反映到父组件，换言之，您无需监听`radio`的`change`事件，也能知道哪个`radio`被选中了。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 被选中`radio`双向绑定的值，如果初始值为某一个`radio`的`name`，该`radio`将会默认被选中 | String \ Number | - | - |
| disabled | 是否禁用所有`radio`  | Boolean | false | true |
| label-disabled | 是否禁止点击文本操作`radio` | Boolean  | false | true |
| shape | 形状，见上方说明 | String  | circle | square |
| icon-size | 图标大小，单位rpx  | String \ Number | 20 | - |
| active-color | 选中时的颜色，应用到所有子`Radio`组件 | String  | #2979ff | - |
| size | radio组件整体的大小，单位rpx  | String \ Number | 34 | - |
| width | `radio`的宽度，需带单位，如`50%`，`150rpx` | String | Number | auto | - |
| wrap | 是否每个`radio`占一行 | Boolean  | false | true |

## radio Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 某个`radio`状态发生变化时触发(选中状态) | name: 通过`props`传递的`name`参数 | - |

## radioGroup Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 任一个`radio`状态发生变化时触发 | name: 值为`radio`通过`props`传递的`name`值 | - |

---

---
url: 'https://uviewpro.cn/zh/tools/random.md'
---
# random 随机数值

## random(min, max)

该方法可以返回在"min"和"max"之间的数值，要求"min"和"max"都为数值，且"max"大于或等于"min"，否则返回0.

* `min` \<Number> 最小值，最小值可以等于该值
* `max` \<Number> 最大值，最大值可以等于该值

```js
console.log(uni.$u.random(1, 3));
```

---

---
url: 'https://uviewpro.cn/zh/tools/randomArray.md'
---
# randomArray 数组乱序

## randomArray(array)

该函数可以打乱一维数组元素的顺序，这是随机过程

* `array` \<Array> 一维数组

```js
import { ref, onMounted } from 'vue';

const array = ref([1, 2, 3, 4, 5]);

onMounted(() => {
  console.log(uni.$u.randomArray(array.value));
});
```

---

---
url: 'https://uviewpro.cn/zh/components/rate.md'
---
# Rate 评分&#x20;

该组件一般用于满意度调查，星型评分的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`count`参数设置总共有多少颗星星可选择
* 通过`v-model`双向绑定初始化时默认选中的星星数量
* \~~通过`current`设置初始化时默认选中的星星数量~~(建议使用v-model的方式，此参数为了向前兼容依然有效，但优先级低于`v-model`)

```html
<template>
	<u-rate :count="count" v-model="value"></u-rate>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const count = ref<number>(4)
const value = ref<number>(2)
</script>
```

## 自定义样式

* 通过`active-color`设置选中的星星的颜色
* 通过`inactive-color`设置未选中时星星的颜色
* 通过`gutter`设置星星的间距，左右内边距各占`gutter`的一半

```html
<u-rate active-color="#FA3534" inactive-color="#b2b2b2" gutter="20"></u-rate>
```

## 自定义图标

* 通过`active-icon`设置激活的图标
* 通过`inactive-icon`设置未激活的图标
* 通过`custom-prefix`设置自定义图标，详见：[扩展自定义图标库](https://uviewpro.cn/zh/guide/customIcon.html)

下方示例为使用心形图标替代默认的星星图标：

```html
<u-rate active-icon="heart-fill" inactive-icon="heart"></u-rate>
```

## 评分分级分层

* 通过`colors`设置不同颜色区分评分层级
* 通过`icons`设置不同类型图标区分评分层级

```html
<template>
  <view>
    <u-rate v-model="value" :colors="colors" :icons="icons" inactive-icon="thumb-up"></u-rate>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<number>(2)
const colors = ref<string[]>(['#ffc454', '#ffb409', '#ff9500'])
const icons = ref<string[]>(['thumb-down-fill', 'thumb-down-fill', 'thumb-up-fill', 'thumb-up-fill'])
</script>
```

## 最少选中的数量

```html
<u-rate :min-count="5"></u-rate>
```

## 禁用状态

禁用下，无法点击或者滑动选择，但是可以通过`current`设置默认选中的数量，禁用状态下用来展示分数，允许出现半星

```html
<u-rate :current="3.7" :disabled="true" :allow-half="true"></u-rate>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 双向绑定选择星星的数量 | String | Number | 0 | - |
| count | 最多可选的星星数量 | String | Number | 5 | - |
| current | 默认选中的星星数量，建议使用`v-model`方式  | String | Number | 0 | - |
| disabled | 是否禁止用户操作 | Boolean | false | true |
| size | 星星的大小，单位rpx | String | Number | 32 | - |
| inactive-color | 未选中星星的颜色 | String | #b2b2b2 | - |
| active-color | 选中的星星颜色 | String | #FA3534 | - |
| gutter | 星星之间的距离 | String | Number | 10 | - |
| min-count | 最少选中星星的个数 | String | Number | 0 | - |
| active-icon | 选中时的图标名，只能为uView的内置图标 | String | star-fill | - |
| inactive-icon | 未选中时的图标名，只能为uView的内置图标 | String | star | - |
| custom-prefix | 自定义字体图标库时，需要写上此值，详见：[扩展自定义图标库](https://uviewpro.cn/zh/guide/customIcon.html) | String  | uicon | - |
| colors | 颜色分级显示，可以用不同颜色区分评分层级 | Array  | - | - |
| icons | 图标分级显示，可以用不同类型的icon区分评分层级 | Array  | - | - |
| allow-half | 是否允许半星选择（仅当禁用状态disabled=true时有效） | Boolean | false | true |

## Events

| 事件名 | 说明 | 回调参数 |
| :- | :- | :- |
| change | 选中的星星发生变化时触发 | value：当前选中的星星的数量，如果使用`v-model`双向绑定方式，无需监听此事件|

---

---
url: 'https://uviewpro.cn/zh/components/readMore.md'
---
# ReadMore 展开阅读更多&#x20;

该组件一般用于内容较长，预先收起一部分，点击展开全部内容的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过slot传入正文内容

```html
<template>
	<u-read-more>
		<rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const content = ref<string>(`山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。
苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。
无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？`)
</script>
```

## 展开收起

配置`toggle`为`true`，展开后可以收起，否则展开后没有收起的按钮

```html
<u-read-more :toggle="true">
	<rich-text :nodes="content"></rich-text>
</u-read-more>
```

## 配置展开高度

可以配置一个高度，单位rpx，只有slot传入的内容高度超出这个值，才会出现"展开阅读全文"字样的按钮

```html
<u-read-more show-height="600">
	<rich-text :nodes="content"></rich-text>
</u-read-more>
```

## 异步初始化

有时候需要展示的内容是从后端获取的，组件内部的`mounted`生命周期初始化时，请求尚未回来，会导致
内容的高度在初始化有误差。可以在请求完毕渲染后(指的是this.$nextTick)，通过`ref`调用组件的`init`方法，重新初始化

```html
<template>
	<u-read-more ref="uReadMoreRef">
		<rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 定义响应式数据
const content = ref<string>('')
const uReadMoreRef = ref<any>(null)

// 模拟页面加载完成生命周期
onMounted(() => {
	// 模拟后端请求
	setTimeout(() => {
		content.value = `山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。
		苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。
		无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？`
		
		// 使用 nextTick 确保 DOM 更新后初始化组件
		setTimeout(() => {
			if (uReadMoreRef.value && uReadMoreRef.value.init) {
				uReadMoreRef.value.init()
			}
		}, 0)
	}, 2000)
})
</script>
```

## 自定义样式

此组件上边部分有一个白色虚化的阴影，用以将点击区域与文字内容进行融合，如果您不想要这个阴影，可以调整`shadow-style`对象，此对象内部如下：

```css
{
	backgroundImage: "linear-gradient(-180deg, rgba(255, 255, 255, 0) 0%, #fff 80%)",
	paddingTop: "300rpx",
	marginTop: "-300rpx"
}
```

如果您不想要阴影，将`backgroundImage`设置为`none`即可，关于`paddingTop`和`marginTop`自行调整至合适数值即可。

```html
<template>
	<u-read-more ref="uReadMore" :shadow-style="shadowStyle" :show-height="200">
		<rich-text :nodes="content"></rich-text>
	</u-read-more>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// 定义响应式数据
const content = ref<string>('')
const uReadMore = ref<any>(null)

// 定义阴影样式对象
const shadowStyle = reactive({
	backgroundImage: "none",
	paddingTop: "0",
	marginTop: "20rpx"
})
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| show-height | 内容超出此高度才会显示展开全文按钮，单位rpx | String | Number | 400 | - |
| toggle | 展开后是否显示收起按钮 | Boolean  | false | true |
| close-text | 关闭时的提示文字 | String  | 展开阅读全文 | - |
| font-size | 提示文字的大小，单位rpx | String | Number  | 28 | - |
| open-text | 展开时的提示文字 | String  | 收起 | - |
| color | 提示文字的颜色 | String  | #2979ff | - |
| shadow-style | 对阴影的自定义处理，对象形式 | Object  | 见上方说明 | - |
| text-indent | 段落首行缩进的字符个数，无需缩进请设置为0 | String  | 2em | - |
| index | 用于在`open`和`close`事件中当作回调参数返回 | String | Number  | - | - |

## Methods

此方法如要通过ref手动调用

| 名称          | 说明            |
|-------------  |---------------- |
| init | 重新初始化组件内部高度计算过程，如果内嵌组件时可能需要用到 |

## Events

| 事件名 | 说明 | 回调参数 |
| :- | :- | :- |
| open | 内容被展开时触发 | index - props中传入的`index`参数值 |
| close | 内容被收起时触发 | index - props中传入的`index`参数值 |

---

---
url: 'https://uviewpro.cn/zh/components/rootPortal.md'
---
# RootPortal 根节点传送 &#x20;

使整个子树从页面中脱离出来，类似于在 CSS 中使用 fixed position 的效果。主要用于制作弹窗、弹出层等。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|×|×|×|

* **H5 端**：使用 `teleport` 特性，详见[teleport文档](https://cn.vuejs.org/guide/built-ins/teleport.html#teleport)
* **微信小程序和支付宝小程序**：使用 `root-portal` 组件，详见[微信小程序root-portal](https://developers.weixin.qq.com/miniprogram/dev/component/root-portal.html)和[支付宝小程序root-portal](https://opendocs.alipay.com/mini/05snwp?pathHash=bccb8999)
* **App 端**：使用 renderjs 实现
* **其他平台**：不支持此功能

:::tip 提示
根节点传送组件仅支持`微信小程序`、`支付宝小程序`、`APP`和`H5`平台，组件会自动根据平台选择合适的实现方式：

这类场景最常见的例子就是全屏的模态框。理想情况下，我们希望触发模态框的按钮和模态框本身的代码是在同一个单文件组件中，因为它们都与组件的开关状态有关。但这意味着该模态框将与按钮一起渲染在应用 DOM 结构里很深的地方。这会导致该模态框的 CSS 布局代码很难写。
:::

## 基本用法

使用 `u-root-portal` 将内容渲染到根节点，避免被父组件的样式影响。

```html
<u-button type="primary" @click="show = true">显示弹窗</u-button>
<u-root-portal v-if="show">
  <view class="modal">
    <view class="modal-content">
      <text>这是一个全局弹窗</text>
      <u-button @click="show = false">关闭</u-button>
    </view>
  </view>
</u-root-portal>
```

```scss
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}
```

## API

## Slots

| 名称    | 说明                         |
| ------- | ---------------------------- |
| default | 默认插槽，用于渲染传送内容   |

---

---
url: 'https://uviewpro.cn/zh/tools/route.md'
---
# route 路由跳转

### route(Object)

此为一个路由跳转方法，内部是对uni多个路由跳转api的封装，更方便使用

Object参数说明：

| 参数名      |     类型       |      默认值      |   是否必填      |  说明   |
|-------------  |---------------- |---------------|------------------ |-------- |
| type | String  | navigateTo | false | `navigateTo`或`to`对应`uni.navigateTo`，`redirect`或`redirectTo`对应`uni.redirectTo`，`switchTab`或`tab`对应`uni.switchTab`，`reLaunch`对应`uni.reLaunch`，`navigateBack`或`back`对应`uni.navigateBack`|
| url | String  | -	 | false | `type`为`navigateTo`，`redirectTo`，`switchTab`，`reLaunch`时为必填 |
| delta | Number | 1  | false | `type`为`navigateBack`时用到，表示返回的页面数 |
| params | Object | -  | false | 传递的对象形式的参数，如`{name: 'lisa', age: 18}` |
| animationType | String | pop-in  | false | 只在APP生效，详见[窗口动画](https://uniapp.dcloud.io/api/router?id=animation) |
| animationDuration | Number | 300  | false | 动画持续时间，单位ms |

```js
import { ref, onMounted } from 'vue';

const route = ref(null);

onMounted(() => {
  setTimeout(() => {
    uni.$u.route({
      url: 'pages/components/empty/index',
      params: {
        name: 'lisa'
      }
    });
  }, 2000);
});
```

## 简写

注：为了方便简写和调用，可以直接传递一个`url`地址替代`Object`，它只能执行`uni.navigateTo`类型的地址，**不支持跳转到Tabbar页面**，
如果有参数需要携带，以对象形式写到方法的第二个参数中。

```js
// 无参数
uni.$u.route('/pages/components/empty/index');


// 带参数
uni.$u.route('/pages/components/empty/index', {
	name: 'lisa',
	age: 20
});
```

---

---
url: 'https://uviewpro.cn/zh/components/search.md'
---
# Search 搜索&#x20;

搜索组件，集成了常见搜索框所需功能，用户可以一键引入，开箱即用。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`placeholder`参数设置占位内容
* 通过`v-model`双向绑定一个**变量**值，设置初始化时搜索框的值，如果初始内容为空，那么请绑定一个值为空字符的变量。

**说明：** 因为是双向绑定的，所以当组件内容输入框内容变化时，也会实时的反映到绑定的`keyword`变量，这意味着，您**无需**监听`change`事件，
也能实时的得知输入框的内容。

```html
<template>
	<u-search placeholder="日照香炉生紫烟" v-model="keyword"></u-search>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const keyword = ref<string>('遥看瀑布挂前川')
</script>
```

## 设置输入框形状

通过`shape`设置输入框两端的形状，`square`-方形带圆角，`round`(默认)-半圆形

```html
<u-search shape="round"></u-search>
```

## 是否开启清除控件

`clearabled`(默认为`true`)设置为`true`的话，输入框有内容时，右边会显示一个清除的图标

```html
<u-search :clearabled="true"></u-search>
```

## 是否开启右边控件

该控件为类似按钮形式，可以设置为"搜索"或者"取消"等内容，如果开启动画效果，用户确认搜索后，该控件会自动消失

* `show-action`配置是否开启右边按钮控件
* `action-text`配置控件内容
* `animation`(默认为`false`)设置为`true`的话，失去焦点，或者点击控件按钮时，控件自动消失，并且带有动画效果

::: warning 说明

1. 如果不想点击右侧控件时自动消失，请把`animation`设置为`false`
2. 右侧控件的默认文字为"搜索"(它本意为控件，碰巧内容为"搜索"二字，并非说它就是一个搜索按钮)，点击它的时候触发的是`custom`事件，而不是`search`事件
   :::

```html
<u-search :show-action="true" action-text="搜索" :animation="true"></u-search>
```

## 自定义样式

* 通过`input-align`设置输入框内容的对其方式，和css的`text-align`同理
* 通过`border-color`设置整个搜索组件的边框，只要配置了颜色，才会出现边框
* 通过`height`设置组件高度
* 通过`disabled`设置是否禁用输入框
* 通过`bg-color`设置是搜索组件背景颜色

```html
<u-search input-align="center" height="70"></u-search>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 双向绑定输入框搜索值 | String | - | - |
| shape | 搜索框形状，round-圆形，square-方形 | String | round | square |
| bg-color | 搜索框背景颜色  | String | #f2f2f2 | - |
| border-color | 边框颜色，配置了颜色，才会有边框  | String | - | - |
| placeholder | 占位文字内容 | String | 请输入关键字 | - |
| clearabled | 是否启用清除控件 | Boolean | true | false |
| focus | 是否自动获得焦点 | Boolean | false | true |
| show-action | 是否显示右侧控件(右侧的"搜索"按钮) | Boolean | true | false |
| action-text | 右侧控件文字 | String | 搜索 | - |
| action-style | 右侧控件的样式，对象形式 | Object | - | - |
| input-align | 输入框内容水平对齐方式 | String | left | center / right |
| disabled | 是否启用输入框 | Boolean | false | true |
| animation | 是否开启动画，见上方说明 | Boolean | false | true |
| height | 输入框高度，单位rpx | String | Number | 64 | - |
| search-icon-color | 搜索图标的颜色，默认同输入框字体颜色 | String | - | - |
| color | 输入框字体颜色 | String | #606266 | - |
| placeholder-color | placeholder的颜色 | String | #909399 | - |
| margin | 组件与其他上下左右元素之间的距离，带单位的字符串形式，如"30rpx"、"30rpx 20rpx"等写法 | String | - | - |
| maxlength | 输入框最大能输入的长度，-1为不限制长度 | String | Number | -1 | - |
| input-style | 自定义输入框样式，对象形式 | Object | - | - |
| search-icon | 输入框左边的图标，可以为uView图标名称或图片路径 | String | search | - |

## Events

您可以通过监听`change`事件，在回调中将返回的结果绑定一个变量去获得用户的输入内容。\
但如"基本使用"中的说明一样，您双向绑定了一个变量后，无需监听`change`事件也是可以的。

| 事件名 | 说明 | 回调参数 | 版本 |
| :- | :- | :- | :- |
| change | 输入框内容发生变化时触发 | value：输入框的值 | - |
| search | 用户确定搜索时触发，用户按回车键，或者手机键盘右下角的"搜索"键时触发 | value：输入框的值 | - |
| custom | 用户点击右侧控件时触发 | value：输入框的值 | - |
| blur | 输入框失去焦点时触发 | value：输入框的值 | - |
| focus | 输入框获得焦点时触发 | value：输入框的值 | - |
| clear | 配置了`clearabled`后，清空内容时会发出此事件 | - | - |
| click | `disabled`为`true`时，点击输入框，发出此事件，用于跳转搜索页 | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/section.md'
---
# Section 查看更多&#x20;

该组件一般用于分类信息有很多，但是限于篇幅只能列出一部分，让用户通过"查看更多"获得更多信息的场景，实际效果见演示。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

说明：此组件会在最左边显示一个竖条

* 通过`title`参数设置主标题
* 通过`sub-title`参数设置副标题

```html
<u-section title="今日热门" sub-title="查看更多"></u-section>
```

## 是否显示右边内容

可以通过设置`right`为`false`来隐藏右边的内容

```html
<u-section title="今日热门" :right="false"></u-section>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| title | 左边主标题 | String | - | - |
| sub-title | 右边副标题 | String  | 更多 | - |
| right | 是否显示右边的内容 | Boolean  | true | false |
| show-line | 是否显示左边的竖条 | Boolean  | true | false |
| font-size | 主标题的字体大小 | String | Number  | 28 | - |
| bold | 主标题是否加粗 | Boolean  | true | false |
| color | 主标题颜色 | String  | #303133 | - |
| sub-color | 右边副标题的颜色(右箭头同此颜色) | String  | #909399 | - |
| line-color | 左边竖线的颜色，默认同`color`参数值 | String  | - | - |
| arrow | 是否显示右边箭头 | Boolean  | true | false |

## Events

| 事件名 | 说明 | 回调参数 | 版本 |
| :- | :- | :- | :- |
| click | 组件右侧的内容被点击时触发，用于跳转"更多" | - | - |

## Slot

| 名称          | 说明            |
|-------------  |---------------- |
| right | 自定义右侧内容  |

---

---
url: 'https://uviewpro.cn/zh/components/select.md'
---
# Select 列选择器&#x20;

此选择器用于单列，多列，多列联动的选择场景。

**注意：** 新版本不建议使用`Picker`组件的单列和多列模式，`Select`组件是专门为列选择而构造的组件，更简单易用。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

所有的配置模式中，都要求传入数组的元素(对象)中含有`value`和`label`属性(可以通过`value-name`和`label-name`参数自定义)，
`value`用于在回调时，区别选择了哪一个(针对开发者)，`label`用于展示在选择器中，供用户选择和查看(针对用户)。

* 通过v-model绑定一个布尔值变量，用于控制组件的弹出与收起。
* 组件共有3种模式，通过配置`mode`参数实现，如下：

1. mode = single-column，为单列选择模式。
2. mode = mutil-column，为多列选择模式。
3. mode = mutil-column-auto，为多列联动模式，多列联动的数据格式比较特殊，见下方说明。

```html
<template>
	<view>
		<u-select v-model="show" :list="list"></u-select>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义列表项接口
interface ListItem {
	value: string
	label: string
}

// 定义响应式数据
const show = ref<boolean>(false)
const list = ref<ListItem[]>([
	{
		value: '1',
		label: '江'
	},
	{
		value: '2',
		label: '湖'
	}
])
</script>
```

## 单列模式

此方式使用较为简单，需要传入一个一维数组，数组的元素为对象，要求必须有`value`和`label`属性，这两个值也将会在回调中被返回。

```html
<template>
	<u-select v-model="show" mode="single-column" :list="list" @confirm="confirm"></u-select>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义列表项接口
interface ListItem {
	value: string
	label: string
}

// 定义响应式数据
const show = ref<boolean>(true)
const list = ref<ListItem[]>([
	{
		value: '1',
		label: '江'
	},
	{
		value: '2',
		label: '湖'
	}
])

// 定义确认回调函数
const confirm = (e: any[]) => {
	// 注意返回值为一个数组，单列时取数组的第一个元素即可(只有一个元素)
	console.log(e)
}
</script>
```

## 多列模式

此模式类似于单列模式，不同之处在于`list`参数为二维数组，同样要求数组的元素必须要有`value`和`label`属性，回调参数为包含多个元素的数组，
分别表示每一列的选择情况。

```html
<template>
	<u-select v-model="show" mode="mutil-column" :list="list" @confirm="confirm"></u-select>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义列表项接口
interface ListItem {
	value: string
	label: string
}

// 定义二维数组类型
type MultiColumnList = ListItem[][]

// 定义响应式数据
const show = ref<boolean>(true)
const list = ref<MultiColumnList>([
	[
		{
			value: '1',
			label: '江'
		},
		{
			value: '2',
			label: '湖'
		}
	],
	[
		{
			value: '3',
			label: '夜'
		},
		{
			value: '4',
			label: '雨'
		}
	]
])

// 定义确认回调函数
const confirm = (e: any[]) => {
	// 回调参数为包含多个元素的数组，每个元素分别反应每一列的选择情况
	console.log(e)
}
</script>
```

## 多列联动模式

由于需要多列联动，此模式和上面的"多列模式"基本相同，但是也有区别的地方，因为需要"联动"，需要在每个对象中多一个`children`属性，用于标识
它的子列(后一列)的可选值，回调参数和"多列模式"一致。

```html
<template>
	<u-select v-model="show" mode="mutil-column-auto" :list="list" @confirm="confirm"></u-select>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义联动列表项接口
interface LinkedListItem {
	value: number
	label: string
	children?: LinkedListItem[]
}

// 定义响应式数据
const show = ref<boolean>(true)
const list = ref<LinkedListItem[]>([
	{
		value: 1,
		label: '中国',
		children: [
			{
				value: 2,
				label: '广东',
				children: [
					{
						value: 3,
						label: '深圳'
					},
					{
						value: 4,
						label: '广州'
					}
				]
			},
			{
				value: 5,
				label: '广西',
				children: [
					{
						value: 6,
						label: '南宁'
					},
					{
						value: 7,
						label: '桂林'
					}
				]
			}
		]
	},
	{
		value: 8,
		label: '美国',
		children: [
			{
				value: 9,
				label: '纽约',
				children: [
					{
						value: 10,
						label: '皇后街区'
					}
				]
			}
		]
	}
])

// 定义确认回调函数
const confirm = (e: any[]) => {
	console.log(e)
}
</script>
```

## 默认值

此组件的所有模式，都可以设置默认值，通过`default-value`数组参数配置，数组元素的0表示选中每列的哪个值(从0开始)，下面分别对几种模式进行说明：

**注意：** `default-value`数组的长度，必须与列数相同，否则无效。

1. 单列模式

如设置`default-value`为`[1]`表示默认选中第2个(从0开始)，`[5]`表示选中第6个。

2. 多列模式

如设置`default-value`为`[1, 3]`表示第一列默认选中第2个，第二列默认选中第4个。

3. 多列联动模式

配置方法同"多列模式"，见上。

## 回调参数

**注意：** 如果您觉得回调的`value`和`label`属性还无法满足您的需求，您可以在传递给`list`的参数中多带一个`extra`属性，如果有此属性，
在回调中将会多返回一个`extra`属性值。

1. 单列模式

此模式点击`确定`或`取消`按钮，会返回一个只有一个元素的数组，此元素即为回调结果，数组内容可能如下：

```js
res = [
	{
		label: '雪月夜',
		value: '1',
		// 如果传递给"list"的对象中有extra属性，将会在此返回
		// extra: 'xxx'
	}
]
```

2. 多列模式

此模式点击`确定`或`取消`按钮，会返回一个有多个元素的数组，元素的数量和列数相等，第0个元素(索引从0开始)与第一列(也可以认为是第0列)相匹配，以此类推，
返回结果可能如下：

```js
res = [
	{
		label: '雪月夜',
		value: '1'
	},
	{
		label: '冷夜雨',
		value: '2'
	},
]
```

3. 多列联动

返回结果同上方的"多列模式"。

## API

## Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|---|---|---:|:---:|---|
| mode | 模式选择，"single-column" - 单列模式，"mutil-column" - 多列模式，"mutil-column-auto" - 多列联动模式 | String | `single-column` | `mutil-column` / `mutil-column-auto` |
| list | 列数据，数组形式，见上方说明 | Array | - | - |
| v-model | 布尔值变量，用于控制选择器的弹出与收起 | Boolean | `false` | `true` |
| safe-area-inset-bottom | 是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明) | Boolean | `false` | `true` |
| cancel-color | 取消按钮的颜色 | String | `#606266` | - |
| confirm-color | 确认按钮的颜色 | String | `#2979ff` | - |
| default-value | 提供的默认选中的下标，见上方说明 | Array | - | - |
| mask-close-able | 是否允许通过点击遮罩关闭 Picker | Boolean | `true` | `false` |
| z-index | 弹出时的 `z-index` 值 | `String \| Number` | `10075` | - |
| value-name | 自定义 `list` 数据的 `value` 属性名 | String | `value` | - |
| label-name | 自定义 `list` 数据的 `label` 属性名 | String | `label` | - |
| child-name | 自定义 `list` 数据的 `children` 属性名（仅对多列联动模式有效） | String | `children` | - |
| title | 顶部中间的标题 | String | - | - |
| confirm-text | 确认按钮的文字 | String | `确认` | - |
| cancel-text | 取消按钮的文字 | String | `取消` | - |
| preserve-selection  | 是否保留用户上次确认的选择（true：优先使用已保存的选择；false：优先使用外部传入的 defaultValue） | Boolean | `true` | `false` |

## Events

| 事件名 | 说明 | 回调参数 | 版本 |
|---|---|---|---|
| confirm | 点击确定按钮，返回当前选择的值 | Array：见上方“回调参数”部分说明 | - |
| cancel | 点击取消按钮，返回当前选择的值 | Array：见上方“回调参数”部分说明 | - |

---

---
url: 'https://uviewpro.cn/zh/components/skeleton.md'
---
# Skeleton 骨架屏 &#x20;

骨架屏一般用于页面在请求远程数据尚未完成时，页面用灰色块预显示本来的页面结构，给用户更好的体验。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

组件由`标题`，`段落`和`头像`组件组件，其中`段落`需要通过`rows`参数配置才显示，可以通过`title`和`avatar`是否显示`标题`和`头像` 。\
该组件的使用，有几个需要注意的点，如下：

* `title`(可选)，是否显示`标题`占位行，该占位行不布满全屏宽度，同时与`段落`的距离较大以做明显区分
* `avatar`(可选)，是否在左上角位置显示圆形的`头像`占位区域
* `rows`(可选)，`段落`的行数
* `loading`(必选)，是否加载中状态，如果为\`true\`\`\`则显示骨架屏组件占位，否则显示插槽中的内容

数据请求完成后，将`loading`设置为`false`，会隐藏骨架组件

```html
<template>
	<u-skeleton
	    rows="3"
	    title
		loading
	></u-skeleton>
</template>
```

## 加载中动画

设置`animate`为`true`，加载中的骨架块将会有一个动画效果，用以加强视觉效果。

```html
<u-skeleton :loading="true" :animate="true"></u-skeleton>
```

## 显示头像

```html
<u-skeleton :loading="true" avatar rows="1"></u-skeleton>
```

## 插槽内容

可以通过插槽写入展示的内容，当请求结束，将`loading`设置为`false`，此时会隐藏骨架组件，同时展示插槽内容。

```html
<template>
	<u-skeleton
	    rows="2"
		:loading="loading"
		avatar
		:title="false"
	>
		<u-text>loading为false时，将会展示此处插槽内容</u-text>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(true)

onMounted(() => {
	// 延时2秒钟
	uni.$u.sleep(2000).then(() => {
		loading.value = false
	})
})
</script>
```

### API

### Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| :- | :- | :- | :- | :- |
| loading | 是否显示骨架占位图，设置为`false`将会展示子组件内容 | Boolean | true | false |
| animate | 是否开启动画效果 | Boolean | true | false |
| rows | 段落占位图行数 | Number | String | 0 | - |
| rowsWidth | 段落占位图的宽度，可以为百分比，数值，带单位字符串等，可通过数组传入指定每个段落行的宽度 | String | Array | Number | 100% | - |
| rowsHeight | 段落的高度 | String | Array | Number | 18 | - |
| title | 是否展示标题占位图 | Boolean | true | false |
| titleWidth | 标题的宽度 | String | Number | 50% | - |
| titleHeight | 标题的高度 | String | Number | 18 | - |
| avatar | 是否展示头像占位图 | Boolean | false | true |
| avatarSize | 头像占位图大小 | String | Number | 32 | - |
| avatarShape | 头像占位图的形状，circle-圆形，square-方形 | String | circle | square |

---

---
url: 'https://uviewpro.cn/zh/components/slider.md'
---
# Slider 滑动选择器&#x20;

该组件一般用于表单中，手动选择一个区间范围的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

需要通过`v-model`绑定一个值，来初始化滑块的选择值(0到100之间)，这个值是双向绑定的，您可以通过这个值，实时地得知内部的滑动结果。

```html
<template>
	<view class="wrap">
		<u-slider v-model="value"></u-slider>
	</view>
</template>
	
<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<number>(30)
</script>

<style scoped lang="scss">
.wrap {
	padding: 30rpx;
}
</style>
```

## 设置最大和最小值

通过`min`和`max`，可以设置滑块所能选择的最大和最小值

```html
<u-slider v-model="value" min="30" max="80"></u-slider>
```

## 设置步进值

通过`step`参数设置步进值，这个步进值为每次跳变的值，具体表现请见示例。

:::tip 提示
需要注意的是，这个`step`必须要被`max`值整除，否则会出现无法无法滑动到最大值的情况
:::

```html
<u-slider v-model="value" step="20" min="30" max="100"></u-slider>
```

## 自定义按钮的内容和样式

通过设置`use-slot`为`true`，可以以传入`slot`的形式，替换默认的滑块按钮。

以下示例结合了`value`值，在按钮上实时显示选择的值：

```html
<template>
	<view class="wrap">
		<u-slider v-model="value" :use-slot="true">
			<!-- 这里外面需要多一层view，否则".badge-button"样式可能不生效 -->
			<view class="">
				<view class="badge-button">
					{{value}}
				</view>
			</view>
		</u-slider>
	</view>
</template>
	
<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const value = ref<number>(30)
</script>

<style scoped lang="scss">
.wrap {
	padding: 30rpx;
}

.badge-button {
	padding: 4rpx 6rpx;
	background-color: $u-type-error;
	color: #fff;
	border-radius: 10rpx;
	font-size: 22rpx;
	line-height: 1;
}
</style>
```

## 自定义滑动选择器整体的样式

* 通过`inactive-color`配置底部滑动条背景颜色
* 通过`active-color`配置底部选择部分的背景颜色
* 通过`block-width`配置滑块宽度(高等于宽)
* 通过`block-color`配置滑动按钮按钮的颜色
* 通过`height`配置滑块条高度，单位rpx

其他更多参数详见底部API

```html
<u-slider v-model="value" block-width="40" block-color="red"></u-slider>
```

## API

## Props

|参数|说明|类型|默认值|可选值|版本|
|:-:|:-:|:-:|:-:|:-:|:-:|
|v-model|双向绑定滑块选择值|String | Number|0|-|-|
|min|可选的最小值(0-100之间)|String | Number|0|-|-|
|max|可选的最大值(0-100之间)|String | Number|100|-|-|
|step|选择的步长|String | Number|1|-|-|
|block-width|滑动按钮的宽度(高等于宽)，单位rpx|String | Number|30|-|-|
|height|滑动选择条的高度，单位rpx|String | Number|6|-|-|
|inactive-color|滑动选择条的底部背景颜色|String|#c0c4cc|-|-|
|active-color|底部选择部分的背景颜色|String|#2979ff|-|-|
|block-color|滑块背景颜色|String|#ffffff|-|-|
|block-style|给滑块按钮自定义样式，对象形式|Object|-|-|-|
|disabled|是否禁用滑块|Boolean|false|true|-|
|use-slot|是否使用slot传入自定义滑块|Boolean|false|true|-|
|start|滑块总体范围起点值|Number | String|0|-||
|end|滑块总体范围终点值|Number | String|100|-||
|showValue|是否显示滑块当前数值气泡|Boolean|false|true||
|valuePosition|滑块数值显示位置，top-上方，bottom-下方|'top' | 'bottom'|top|bottom||
|showEdgeValue|是否在起始和结束位置显示数值|Boolean|false|true||
|valuePosition|起始和结束数值显示位置，top-上方，bottom-下方|'top' | 'bottom'|top|bottom||

## Slot

|名称|说明|
|:-:|:-:|
|-|自定义滑块内容|

## Events

|事件名|说明|回调参数|
|:-:|:-:|:-:|
|start|触发滑块移动|-|
|moving|正在滑动中|-|
|end|滑动结束|-|

---

---
url: 'https://uviewpro.cn/zh/components/steps.md'
---
# Steps 步骤条&#x20;

该组件一般用于完成一个任务要分几个步骤，标识目前处于第几步的场景。

## 平台差异说明

| App | H5 | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ小程序 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| √ | √ | √ | √ | √ | √ | √ |

## 基本使用

* 通过`list`参数传入一个数组，标识步骤的总数
* 通过`current`参数标识目前处于第几步，从0开始

```html
<template>
	<view>
		<u-steps :list="numList" :current="1"></u-steps>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义步骤项接口
interface StepItem {
	name: string
}

// 定义响应式数据
const numList = ref<StepItem[]>([
	{
		name: '下单'
	}, 
	{
		name: '出库'
	}, 
	{
		name: '运输'
	}, 
	{
		name: '签收'
	}
])
</script>
```

## 设置步骤条的主题

* `type`值可选的有`primary`(默认)、`success`、`info`、`warning`、`error`
* `type`值和`active-color`(默认为空)为互斥关系，如果设置了`active-color`，会优先起作用

```html
<u-steps :list="numList" active-color="#fa3534"></u-steps>
```

## 设置步骤条的模式

`mode`可以设置为`dot`(圆点，默认值)或者`number`(数字)，二者有不同形式，见示例

```html
<u-steps :list="numList" mode="number"></u-steps>
```

## Step 组合&#x20;

`u-step` 为新增组件，可以完整替换 `u-steps` list 模式，同时也用于自定义步骤条的样式，将来可能会弃用 `list` 模式，推荐使用 `u-steps` 和 `u-step` 组合的方式：

```html
<template>
	<u-steps :direction="direction" :current="current" :mode="mode" :icon="icon">
		<u-step v-for="(item, index) in list" :key="index" :name="item.name" :desc="item.desc" />
	</u-steps>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import type { StepDirection, StepMode } from '@/uni_modules/uview-pro/types/global';

const list = ref([
	{
		name: '下单',
		desc: '10:30'
	},
	{
		name: '出库',
		desc: '11:00'
	},
	{
		name: '运输',
		desc: '14:00'
	},
	{
		name: '签收',
		desc: '18:30'
	}
]);
const current = ref(0);
const icon = ref('checkmark');
const mode = ref<StepMode>('number');
const direction = ref<StepDirection>('row');
</script>
```

## 自定义slot&#x20;

```html
<template>
	<u-steps :direction="direction" :current="current" :mode="mode" :icon="icon">
		<u-step name="预约">
			<template #desc>
				<text v-show="current < 0">自定义描述</text>
				<text v-show="current >= 0" class="custom-desc">自定义描述</text>
			</template>
		</u-step>
		<u-step desc="10:30">
			<template #name>
				<text v-show="current < 1">名额确认</text>
				<text v-show="current >= 1" class="custom-name">名额不足</text>
			</template>
		</u-step>
		<u-step desc="11:00">
			<template #name>
				<text v-show="current < 2">预约成功</text>
				<text v-show="current >= 2" class="custom-error-name">预约失败</text>
			</template>
			<template #icon>
				<u-icon size="32" color="red" name="close"></u-icon>
			</template>
		</u-step>
	</u-steps>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import type { StepDirection, StepMode } from '@/uni_modules/uview-pro/types/global';

const current = ref(0);
const icon = ref('checkmark');
const mode = ref<StepMode>('number');
const direction = ref<StepDirection>('row');
</script>
```

## API

## Steps Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| mode | 设置模式 | `String` | `dot` | `number` |
| list | 步骤数据数组（具体见示例） | `Array` | `[]` | - |
| current | 设置当前处于第几步 | `Number \| String` | `0` | - |
| direction | `row`-横向，`column`-竖向 | `String` | `row` | `column` |
| active-color | 已完成步骤的激活颜色，如设置，`type`值会失效 | `String` | - | - |
| un-active-color | 未激活的颜色，用于表示未完成步骤的颜色 | `String` | `#606266` | - |
| icon | `mode = number`时的自定义图标 | `String` | `checkmark` | - |

## Step Props&#x20;

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| mode | 设置模式 | `String` | `dot` | `number` |
| direction | `row`-横向，`column`-竖向 | `String` | `row` | `column` |
| active-color | 已完成步骤的激活颜色，如设置，`type`值会失效 | `String` | - | - |
| un-active-color | 未激活的颜色，用于表示未完成步骤的颜色 | `String` | `#606266` | - |
| icon | `mode = number`时的自定义图标 | `String` | `checkmark` | - |
| name | 标题 | `String` | - | - |
| desc | 描述 | `String` | - | - |

## Step Slots&#x20;

| 名称 | 说明 |
| --- | --- |
| `icon` | 自定义图标内容 |
| `name` | 自定义标题内容 |
| `desc` | 自定义描述内容 |

---

---
url: 'https://uviewpro.cn/zh/components/sticky.md'
---
# Sticky 吸顶&#x20;

该组件与CSS中`position: sticky`属性实现的效果一致，当组件达到预设的到顶部距离时，
就会固定在指定位置，组件位置大于预设的顶部距离时，会重新按照正常的布局排列。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`slot`，将需要吸顶的内容放在`Sticky`组件中即可，`slot`中只能有一个根元素

:::danger 注意！
由于页面依赖相关的原因的，部分页面会出现**Cannot read property 'bottom' of null**的报错，可以参考 [issue #239](https://github.com/YanxinNet/uView/issues/239) 进行处理。
:::

```html
<template>
	<view class="container">
		<u-sticky>
			<!-- 只能有一个根元素 -->
			<view class="sticky">
				宝剑锋从磨砺出,梅花香自苦寒来
			</view>
		</u-sticky>
	</view>
</template>

<style lang="scss" scoped>
	.container {
		height: 200vh;
		margin-top: 150rpx;
	}
	
	.sticky {
		width: 750rpx;
		height: 120rpx;
		background-color: #2979ff;
		color: #fff;
		padding: 24rpx;
	}
</style>
```

## 吸顶距离

通过`offset-top`参数设置组件在吸顶时与顶部的距离

```html
<u-sticky offset-top="200">
	<view>
		塞下秋来风景异，衡阳雁去无留意
	</view>
</u-sticky>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| offset-top | 吸顶时与顶部的距离，单位rpx  | String | Number | 0 | - |
| index | 自定义标识，用于区分是哪一个组件 | String | Number  | - | - |
| enable | 是否开启吸顶功能 | Boolean  | true | false |
| bg-color | 组件背景颜色 | String  | #ffffff | - |
| z-index | 吸顶时的`z-index`值 | String | Number  | 970 | - |
| h5-nav-height | 导航栏高度，自定义导航栏时(无导航栏时需设置为`0`)，需要传入此值，单位**px** | String | Number  | 44 | - |

## Event

|事件名|说明|回调参数|
|:-|:-|:-|
| fixed | 组件吸顶时触发 | index: 通过props传递的`index` |
| unfixed | 组件取消吸顶时触发 | index: 通过props传递的`index` |

---

---
url: 'https://uviewpro.cn/zh/components/subsection.md'
---
# Subsection 分段器&#x20;

该分段器一般用于用户从几个选项中选择某一个的场景

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`list`数组参数传递分段的选项
* 通过`current`指定初始化时激活的选项

```html
<template>
	<u-subsection :list="list" :current="1"></u-subsection>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义分段器选项接口
interface SubsectionItem {
	name: string
}

// 定义响应式数据
const list = ref<SubsectionItem[]>([
	{
		name: '待发货'
	}, 
	{
		name: '待付款'
	}, 
	{
		name: '待评价'
	}
])

// 定义当前选中索引
const current = ref<number>(1)
</script>
```

## 模式选择

通过`mode`设置分段器的模式

* 值为`button`时为按钮类型
* 值为`subsection`时为分段器形式

```html
<u-subsection :list="list" :current="1"></u-subsection>
```

## 是否开启动画效果

`animation`(默认为`true`)设置为`true`的话，分段器的三种模式滑块移动时都会有动画效果

```html
<u-subsection :animation="true"></u-subsection>
```

## 颜色配置

* 通过`active-color`配置激活选项的文字颜色，`mode`为`subsection`时无效，此时默认为白色：
* 通过`bgColor`配置背景颜色
* 通过`buttonColor`配置按钮颜色，`mode`为`button`时有效

```html
<u-subsection active-color="#ff9900"></u-subsection>
```

## 注意事项

如果想通过一个变量绑定`current`值，需要在`change`事件回调中修改此值，否则可能会由于`props`的限制，前后两次设置`current`为相同的值，
而导致无法通过修改`current`值触发分段器的变化。

```html
<template>
	<view>
		<u-subsection :list="list" :current="curNow" @change="sectionChange"></u-subsection>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义分段器选项接口
interface SubsectionItem {
	name: string
}

// 定义响应式数据
const list = ref<SubsectionItem[]>([
	{
		name: '待发货'
	}, 
	{
		name: '待付款'
	}, 
	{
		name: '待评价'
	}
])

const curNow = ref<number>(0)

// 定义分段器变化回调函数
const sectionChange = (index: number) => {
	curNow.value = index
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| list | 选项的数组，形式见上方"基本使用" | Array | - | - |
| current | 初始化时默认选中的选项索引值  | String | Number | 0 | - |
| active-color | 激活时的颜色 | String | #303133 | - |
| inactive-color | 未激活时的颜色 | String | #606266 | - |
| mode | 模式选择，见上方"模式选择"说明 | String | button | subsection |
| font-size | 字体大小，单位rpx | String | Number | 28 | - |
| height | 组件高度，单位rpx | String | Number | 70 | - |
| animation | 是否开启动画效果，见上方说明 | Boolean | true | false |
| bold | 激活选项的字体是否加粗 | Boolean | true | false |
| bg-color | 组件背景颜色，`mode`为`button`时有效 | String | #eeeeef | - |
| button-color | 按钮背景颜色，`mode`为`button`时有效 | String | #ffffff | - |

## Events

| 事件名 | 说明 | 回调参数 |
| :- | :- | :- |
| change | 分段器选项发生改变时触发 | index：选项的index索引值，从0开始 |

---

---
url: 'https://uviewpro.cn/zh/components/swipeAction.md'
---
# SwipeAction 滑动操作&#x20;

该组件一般用于左滑唤出操作菜单的场景，用的最多的是左滑删除操作。

::: warning 注意
如果把该组件通过 v-for 用于左滑删除的列表，请保证循环的`:key`是一个唯一值，可以用数据的 id 或者 title 替代。
不能是数组循环的 index，否则删除的时候，可能会出现数据错乱
:::

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

* 通过 slot 传入内部内容即可，可以将`v-for`的"index"索引值传递给`index`参数，用于点击时，在回调方法中对某一个数据进行操作(点击回调时第一个参数会返回此索引值)
* 内部的按钮通过`options`参数配置，此参数为一个数组，元素为对象，可以配置按钮的文字，背景颜色(建议只配置此两个参数即可)，**请勿配置宽高等属性**。

说明：有时候，我们在打开一个 swipeAction 的同时，需要自动关闭其他的 swipeAction，这时需要通过`open`事件实现，见如下：

```html
<template>
  <view>
    <u-swipe-action
      :show="item.show"
      :index="index"
      v-for="(item, index) in list"
      :key="item.id"
      @click="click"
      @open="open"
      :options="options"
    >
      <view class="item u-border-bottom">
        <image mode="aspectFill" :src="item.images" />
        <!-- 此层wrap在此为必写的，否则可能会出现标题定位错误 -->
        <view class="title-wrap">
          <text class="title u-line-2">{{ item.title }}</text>
        </view>
      </view>
    </u-swipe-action>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义列表项接口
interface ListItem {
  id: number
  title: string
  images: string
  show: boolean
}

// 定义选项按钮接口
interface OptionButton {
  text: string
  style: {
    backgroundColor: string
  }
}

// 定义响应式数据
const list = ref<ListItem[]>([
  {
    id: 1,
    title: "长安回望绣成堆，山顶千门次第开，一骑红尘妃子笑，无人知是荔枝来",
    images: "https://ik.imagekit.io/anyup/uview-pro/common/logo-new.png",
    show: false,
  },
  {
    id: 2,
    title: "新丰绿树起黄埃，数骑渔阳探使回，霓裳一曲千峰上，舞破中原始下来",
    images: "https://ik.imagekit.io/anyup/uview-pro/common/logo-new.png",
    show: false,
  },
  {
    id: 3,
    title: "登临送目，正故国晚秋，天气初肃。千里澄江似练，翠峰如簇",
    images: "https://ik.imagekit.io/anyup/uview-pro/common/logo-new.png",
    show: false,
  },
])

const disabled = ref<boolean>(false)
const btnWidth = ref<number>(180)
const show = ref<boolean>(false)

const options = ref<OptionButton[]>([
  {
    text: "收藏",
    style: {
      backgroundColor: "#007aff",
    },
  },
  {
    text: "删除",
    style: {
      backgroundColor: "#dd524d",
    },
  },
])

// 定义点击事件回调函数
const click = (index: number, index1: number) => {
  if (index1 == 1) {
    list.value.splice(index, 1)
    // uni.$u.toast(`删除了第${index}个cell`)
  } else {
    list.value[index].show = false
    // uni.$u.toast(`收藏成功`)
  }
}

// 定义打开事件回调函数
const open = (index: number) => {
  // 先将正在被操作的swipeAction标记为打开状态，否则由于props的特性限制，
  // 原本为'false'，再次设置为'false'会无效
  list.value[index].show = true
  list.value.map((val, idx) => {
    if (index != idx) list.value[idx].show = false
  })
}
</script>

<style lang="scss" scoped>
.item {
  display: flex;
  padding: 20rpx;
}

image {
  width: 120rpx;
  flex: 0 0 120rpx;
  height: 120rpx;
  margin-right: 20rpx;
  border-radius: 12rpx;
}

.title {
  text-align: left;
  font-size: 28rpx;
  color: $u-content-color;
  margin-top: 20rpx;
}
</style>
```

## 修改按钮样式

* 通过`options`参数配置按钮的数量和样式，见上方说明
* 通过`btn-width`设置按钮的宽度，单位 rpx

```html
<u-swipe-action btn-width="180" :options="options"> ... </u-swipe-action>
```

## 点击事件

`click`点击事件回调中，有两个参数，第一个参数为通过 Props 传入的`index`参数，第二个参数为滑动按钮的索引，即`options`数组的索引，
用于标识第几个按钮被点击。

## API

## Props

| 参数          | 说明                                                                      | 类型             | 默认值  | 可选值 |
| ------------- | ------------------------------------------------------------------------- | ---------------- | ------- | ------ |
| bg-color      | 整个组件背景颜色                                                          | String           | #ffffff | -      |
| index         | 标识符，点击时候用于区分点击了哪一个，用`v-for`循环时的 index 即可        | String | Number | -       | -      |
| btn-width     | 按钮宽度，单位 rpx                                                        | String | Number | 180     | -      |
| disabled      | 是否禁止某个 swipeAction 滑动                                             | Boolean          | false   | true   |
| vibrate-short | 是否使手机发生短促震动，目前只在 iOS 的微信小程序和微信小程序开发工具有效 | Boolean          | false   | true   |
| show          | 打开或者关闭某个组件                                                      | Boolean          | false   | true   |
| options       | 按钮组的配置参数，数组形式，见上方说明                                    | Array            | \[ ]     | -      |

## Event

| 事件名        | 说明               | 回调参数                                |
| :------------ | :----------------- | :-------------------------------------- |
| click         | 点击组件时触发     | (index1, index)，见上方"点击事件"的说明 |
| close         | 组件触发关闭状态时 | index: 通过 props 传递的`index`         |
| open          | 组件触发打开状态时 | index: 通过 props 传递的`index`         |
| content-click | 点击内容时触发     | index: 通过 props 传递的`index`         |

---

---
url: 'https://uviewpro.cn/zh/components/swiper.md'
---
# Swiper 轮播图&#x20;

该组件一般用于导航轮播，广告展示等场景,可开箱即用，具有如下特点：

* 内置多种指示器模式，可配置指示器位置
* 3D 轮播图效果
* 可配置是否显示标题

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

通过`list`参数传入轮播图列表值，该值为一个数组，元素为对象，见如下：

* `list`的"image"属性为轮播图的图片路径
* `list`的"title"属性为需要显示的标题

**说明：** 某些情况下

1. 您从服务端获取的数据，里面的数组对于图片的属性名不一定为`image`，如果让您再历遍修改为`image`属性，显然是不人性的，
   所以 uView 提供了一个`name`参数，比如您数组中的图片名称为`img`，您可以设置`u-swiper`组件的`name`参数为`img`值。

2. 您也可以直接传递一个元素为图片路径的数组给`list`参数，如下：

```html
<u-swiper :list="list"></u-swiper>

let list = [ '1.png', '2.png' ];
```

::: warning 注意
如果需要显示标题，还需要设置`title`参数为`true`
:::

```html
<template>
  <view class="wrap">
    <u-swiper :list="list"></u-swiper>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义轮播图项接口
interface SwiperItem {
  image: string
  title: string
}

// 定义响应式数据
const list = ref<SwiperItem[]>([
  {
    image: "https://cdn.uviewpro.cn/uview/xxx.png",
    title: "昨夜星辰昨夜风，画楼西畔桂堂东",
  },
  {
    image: "https://cdn.uviewpro.cn/uview/xxx.png",
    title: "身无彩凤双飞翼，心有灵犀一点通",
  },
  {
    image: "https://cdn.uviewpro.cn/uview/xxx.png",
    title: "谁念西风独自凉，萧萧黄叶闭疏窗，沉思往事立残阳",
  },
])
</script>

<style lang="scss" scoped>
.wrap {
  padding: 40rpx;
}
</style>
```

## 指示器类型

本组件内置了多种指示器，通过配置`mode`参数即可，有如下：

* `rect`-指示器为方块状
* `dot`-指示器为圆点
* `number`-指示器为数字
* `round`-激活的指示器为块状，未激活的未点状，为默认值
* `none`-不显示指示器

通过`indicator-pos`参数配置指示器的位置，有如下值：

* `topLeft`-指示器位于左上角
* `topCenter`-指示器位于上方中间位置
* `topRight`-指示器位于右上角
* `bottomLeft`-指示器位于左下角
* `bottomCenter`-指示器位于底部中间位置，为默认值
* `bottomRight`-指示器位于右下角

```html
<u-swiper :list="list" mode="dot" indicator-pos="bottomRight"></u-swiper>
```

## 是否开启 3D 效果

配置`effect3d`为`true`即可，该效果左右两边可以缩略形式预览前后一个 swiper-item 的一部分

```html
<u-swiper :list="list" :effect3d="true"></u-swiper>
```

## 控制轮播效果

* `autoplay`-是否自动轮播，默认为`true`
* `interval`-前后两张图自动轮播的时间间隔
* `duration`-切换一张轮播图所需的时间
* `circular`-是否衔接滑动，即到最后一张时，是否可以直接转到第一张

```html
<u-swiper :list="list" duration="3000" :circular="false"></u-swiper>
```

## API

## Props

| 参数                           | 说明                                                                               | 类型             | 默认值       | 可选值                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------- | ---------------- | ------------ | --------------------------------------------------------- |
| list                           | 轮播图数据，见上方"基本使用"说明                                                   | Array            | -            | -                                                         |
| title                          | 是否显示标题文字，需要配合`list`参数，见上方说明                                   | Boolean          | false        | true                                                      |
| mode                           | 指示器模式，见上方说明                                                             | String           | round        | rect / dot / number / none                                |
| height                         | 轮播图组件高度，单位 rpx                                                           | String | Number | 250          | -                                                         |
| indicator-pos                  | 指示器的位置                                                                       | String           | bottomCenter | topLeft / topCenter / topRight / bottomLeft / bottomRight |
| effect3d                       | 是否开启 3D 效果                                                                   | Boolean          | false        | true                                                      |
| autoplay                       | 是否自动播放                                                                       | Boolean          | true         | false                                                     |
| interval                       | 自动轮播时间间隔，单位 ms                                                          | String | Number | 2500         | -                                                         |
| circular                       | 是否衔接播放，见上方说明                                                           | Boolean          | true         | false                                                     |
| duration                       | 切换一张轮播图所需的时间，单位 ms                                                  | String | Number | 500          | -                                                         |
| border-radius                  | 轮播图圆角值，单位 rpx                                                             | String | Number | 8            | -                                                         |
| title-style                    | 自定义标题样式                                                                     | Object           | -            | -                                                         |
| effect3d-previous-margin       | effect3d = true 模式的情况下，激活项与前后项之间的距离，单位 rpx                   | String | Number | 50           | -                                                         |
| img-mode                       | 图片的裁剪模式，详见[image 组件裁剪模式](https://uniapp.dcloud.io/component/image) | String           | aspectFill   | -                                                         |
| name                           | 组件内部读取的`list`参数中的属性名，见上方说明                                     | string           | name         | -                                                         |
| bg-color                       | 背景颜色                                                                           | string           | #f3f4f6      | -                                                         |
| current | 初始化时，默认显示第几项                                                           | String | Number | 0            | -                                                         |

## Events

| 事件名 | 说明                               | 回调参数                             |
| :----- | :--------------------------------- | :----------------------------------- |
| click  | 点击轮播图时触发                   | index：点击了第几张图片，从 0 开始   |
| change | 轮播图切换时触发(自动或者手动切换) | index：切换到了第几张图片，从 0 开始 |

---

---
url: 'https://uviewpro.cn/zh/components/switch.md'
---
# Switch 开关选择器&#x20;

选择开关一般用于只有两个选择，且只能选其一的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过`v-model`绑定一个`布尔值`变量，这个变量是双向绑定的，当用户开或关选择器的时候，在父组件的该值也会相应的变为`true`或者`false`，也就是说，
您不用监听`change`事件，也能知道选择器当前处于**开**或者**关**的状态。

```html
<template>
	<u-switch v-model="checked"></u-switch>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义响应式数据
const checked = ref<boolean>(false)

// 定义switch变化回调函数
const change = (status: boolean) => {
	// switch打开或者关闭时触发，值为true或者false
	// 即使不监听此事件，checked此时也会相应的变成true或者false
	// console.log(status);
}
</script>
```

## 禁用switch

设置`disabled`为`true`，即可禁用某个组件，让用户无法点击，禁用分为两种状态：

* 一是关闭情况下的禁用，这时只显示一个白色的区域。
* 二是打开后再禁用，这时会在原有的颜色上加一个`opacity`透明度，但此时依然是不可操作的。

```html
<u-switch v-model="checked" :disabled="true"></u-switch>
```

## 加载中

通过设置`loading`变量为`true`，可以让`switch`处于加载中的状态，这时`switch`是不可操作的

```html
<u-switch v-model="checked" :loading="true"></u-switch>

<!-- 等价于 -->
<u-switch v-model="checked" loading></u-switch>
```

## 自定义颜色

```html
<u-switch v-model="checked" active-color="red" inactive-color="#eee"></u-switch>
```

## 自定义值

可以通过设置`active-value`和`inactive-value`来控制选择器打开或者关闭时，通过`change`事件发出的回调值。

```html
<u-switch v-model="checked" active-value="1" inactive-value="0"></u-switch>
```

## 异步控制

这种场景，一般发生在用户打开或者关闭选择器时，需要本地或者向后端请求判断，是否允许用户打开或者关闭的场景。

* 假设原来是打开状态

1. 您通过`watch`监听`v-model`绑定的`checked`变量，或者通过监听`switch`的`change`事件，得知`checked`变量发生了变化
2. 这时您可以通过设置`loading`为`true`，同时将`checked`值设置为`true`(因为用户已关闭，这里让它重新打开，并处于加载中)
3. 等请求结束后，根据判断结果，把`checked`值设置为`true`或者`false`，同时去掉加载中状态(`loading`设置为`false`)，让组件呈现最终的状态

* 假设原来处于关闭状态

处理方法同上，只不过对应的状态是反过来的

下面示例为原本是打开状态，用户把它关闭，我们通过异步控制的场景

:::warning 注意
此处示例中，我们通过`watch`监听`checked`变量为`false`的情景，在定时器模拟回调中又将`checked`设置为`false`，会造成无限循环，所以这里
引入了一个中间变量`controlStatus`来识别
:::

```html
<template>
	<u-switch v-model="checked" :loading="loading"></u-switch>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

// 定义响应式数据
const checked = ref<boolean>(true)
const loading = ref<boolean>(false)
// 中间变量，避免在watch中多次回调，造成无限循环
const controlStatus = ref<boolean>(false)

// 定义switch变化回调函数
const change = (status: boolean) => {
	// switch打开或者关闭时触发，值为true或者false
	// console.log(status);
}

// 监听checked变化
watch(checked, (val) => {
	// 等于false，意味着用户手动关闭了switch
	if (val == false) {
		if(controlStatus.value == true) {
			controlStatus.value = false;
			return ;
		}
		// 重新打开switch，并让它处于加载中的状态
		checked.value = true;
		loading.value = true;
		// 模拟向后端发起请求
		getRestultFromServer();
	}
})

// 模拟向后端发起请求
const getRestultFromServer = () => {
	// 通过定时器模拟向后端请求
	setTimeout(() => {
		controlStatus.value = true;
		// 后端允许用户关闭switch，设置checked为false，结束loading状态
		loading.value = false;
		checked.value = false;
	}, 1500);
}
</script>
```

## API

## Switch Props

注意：需要给`switch`组件通过`v-model`绑定一个布尔值，来初始化`switch`的状态，随后该值被双向绑定，
当用打开选择器时，该值在`switch`组件内部被修改为`true`，并反映到父组件，否则为`false`，换言之，您无需监听`switch`的`change`事件，也能
知道某一个`switch`是否被选中的状态

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| v-model | 双向绑定的数值  开始支持 Number | String   | Boolean | Number | String | false | - |
| loading | 是否处于加载中  | Boolean | false | true |
| disabled | 是否禁用  | Boolean | false | true |
| size | 开关尺寸，单位rpx | String | Number  | 50 | - |
| active-color | 打开时的背景色 | String  | #2979ff | - |
| inactive-color | 关闭时的背景色 | String  | #ffffff | - |
| vibrate-short | 是否使手机发生短促震动，目前只在iOS的微信小程序和微信小程序开发工具有效  | Boolean | false | true |
| active-value | 打开选择器时通过change事件发出的值 | Boolean | Number | String  | true | - |
| inactive-value | 关闭选择器时通过change事件发出的值 | Boolean | Number | String | false | - |

## Switch Event

|事件名|说明|回调参数|
|:-|:-|:-|
| change | 在`switch`打开或关闭时触发 | value：打开时为`active-value`值，关闭时为`inactive-value`值 |

---

---
url: 'https://uviewpro.cn/zh/components/tabbar.md'
---
# Tabbar 底部导航栏&#x20;

### 优点：

此组件一般用于应用的底部导航，具有如下特点：

* 可以设置凸起的按钮，且是全端通用的
* 图标可以使用字体图标(内置图标和扩展图标)或者图片
* 可以动态切换菜单的数量以及配置
* 切换菜单之前，可以进行回调鉴权
* 可以设置角标
* 有效防止组件区域高度塌陷，无需给父元素额外的内边距或者外边距来避开导航的区域

### 缺点：

虽然优点很多，但是如果用此组件模拟 tabbar 页面的话依然是瑜不掩瑕的，因为它同样带来很多难以解决的缺点：

* 首先是性能问题，在 uni-app 的 vue 版本上，自定义 tabbar 让您不得不在一个 webview 内模拟出多个页面，这存在严重的性能问题
* 相比原生的 uni-app 的 tabbar，自定义 tabbar 让你失去了路由管理的功能
* 渲染的速度比不上原生的 tabbar，但是这影响不大

:::tip 提示
以上的缺点，是指自定义模拟 tabbar 页面的情形，我们提供了一个解决方案，可以使用 uni-app 自带 tabbar 系统，保证性能的同时，又能尽情自定义 tabbar 导航栏，见下方`实战教程`说明。
:::

## 平台差异说明

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

## 基本使用

在使用的时候，需要注意组件的位置，要将它放在和页面包裹所有内容的元素同级的位置，否则可能会造成组件的高度塌陷，有如下几个需要注意的点：

* 通过`list`参数配置每一个 item 的参数
* 如果需要配置凸起的按钮，这个按钮的配置需要在`list`数组的**中间位置**，同时需要配置`mid-button`参数为`true`
* 将组件放在和页面包裹所有内容的元素同级的位置
* 通过`v-model`绑定一个数值变量，用于指示当前激活项的索引

下面解释`list`数组中元素参数的作用：

:::tip 提示

1. 自 `v0.4.7` 版本开始，`customIcon` 参数支持设置自定义的 `customPrefix`。

   * 当 `customIcon` 为 `boolean` 类型，那么 `u-icon` 的 `customPrefix` 默认为 `custom-icon`，当然，如果你使用的扩展图标库的 `prefix` 并非`custom-icon`，那么请将此参数设置为 `string`，设置的值即为真实的前缀，如：`customIcon: 'my-icon'`

2. 自 `v0.4.10` 版本开始，开始支持仅设置图标和文字显示。[查看issue](https://github.com/anyup/uView-Pro/issues/98)
   * 如果仅设置了 `iconPath` 和 `selectedIconPath`, 未设置 `text`，那么 `u-tabbar` 将会以纯图标显示，不会显示文字。如果仅设置了 `text`，那么 `u-tabbar` 默认会以纯文字显示，不会显示图标。支持设置 textSize 和 iconSize 两个参数，分别设置图标和文字的大小。
   * 图标大小优先级：midButtonSize > iconSize > props.iconSize
   * 文字大小优先级：textSize > props.textSize

:::

```js
let list = [
  {
    // 非凸起按钮未激活的图标，可以是uView内置图标名或自定义扩展图标库的图标
    // 或者png图标的【绝对路径】，建议尺寸为80px * 80px
    // 如果是中间凸起的按钮，只能使用图片，且建议为120px * 120px的png图片
    iconPath: "home",
    // 激活(选中)的图标，同上
    selectedIconPath: "home-fill",
    // 显示的提示文字
    text: "首页",
    // 红色角标显示的数字，如果需要移除角标，配置此参数为0即可
    count: 2,
    // 如果配置此值为true，那么角标将会以红点的形式显示
    isDot: true,
    // 如果使用自定义扩展的图标库字体，需配置此值为true
    // 自定义字体图标库教程：https://uviewpro.cn/zh/guide/customIcon.html
    customIcon: false,
    // 如果是凸起按钮项，需配置此值为true
    midButton: false,
    // 点击某一个item时，跳转的路径，此路径必须是pagees.json中tabBar字段中定义的路径
    pagePath: "", // 路径需要以"/"开头
    iconSize: 40, // 图标大小，不设置默认跟随prop为40rpx
    textSize: 26 // 文字大小，不设置默认跟随prop为26rpx
  },
];
```

### 示例代码

```html
<template>
  <view>
    <view class="u-page">
      <!-- 所有内容的容器 -->
    </view>
    <!-- 与包裹页面所有内容的元素u-page同级，且在它的下方 -->
    <u-tabbar v-model="current" :list="list" :mid-button="true"></u-tabbar>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TabbarItem } from 'uview-pro/types/global';

// 定义响应式数据
const list = ref<TabbarItem[]>([
  {
    iconPath: "home",
    selectedIconPath: "home-fill",
    text: "首页",
    count: 2,
    isDot: true,
    customIcon: false,
  },
  {
    iconPath: "photo",
    selectedIconPath: "photo-fill",
    text: "放映厅",
    customIcon: false,
  },
  {
    iconPath: "https://ik.imagekit.io/anyup/uview-pro/logo/default.png",
    selectedIconPath: "https://ik.imagekit.io/anyup/uview-pro/logo/default.png",
    text: "发布",
    midButton: true,
    customIcon: false,
  },
  {
    iconPath: "play-right",
    selectedIconPath: "play-right-fill",
    text: "直播",
    customIcon: false,
  },
  {
    iconPath: "account",
    selectedIconPath: "account-fill",
    text: "我的",
    count: 23,
    isDot: false,
    customIcon: false,
  },
])

const current = ref<number>(0)
</script>
```

## 外观配置

可以通过以下参数，进行组件的整体外观配置

* `height`配置导航栏高度，建议使用默认值即可，默认为`50px`，与 uni-app 自带系统导航栏高度一致
* `bg-color`组件的背景颜色
* `active-color`与`inactive-color`配置提示文字和图标的颜色(如果是字体图标的话)，可以搭配`bg-color`达到自定义导航栏主题的效果

## 切换前的回调

在点击切换之前，如果配置了`before-switch`参数并绑定的是一个方法的话，将会抛出点击项的索引，并执行此方法。

此回调可以返回一个`promise`、`true`，或者`false`，下面分别阐述三者的处理情况：

* `false`——如果返回`false`，将不会切换`tab`项
* `true`——如果返回`true`，将会切换`tab`项
* `promise`——如果返回的是一个`promise`，如果进入`then`回调，就会和返回`true`的情况一样，如果进入`catch`回调，就会和返回`false`的情况一样

下面举例说明：

由于篇幅问题，以下示例可不直接运行，仅作举例作用。

### 1. 普通返回

```html
<template>
  <u-tabbar :before-switch="beforeSwitch"></u-tabbar>
</template>

<script setup lang="ts">
// 定义切换前的回调函数
const beforeSwitch = (index: number): boolean => {
  // 只能切换偶数项
  if (index % 2 == 0) return true;
  else return false;
}
</script>
```

### 2. 请求之后再返回

```html
<template>
  <u-tabbar :before-switch="beforeSwitch"></u-tabbar>
</template>

<script setup lang="ts">
// 定义切换前的异步回调函数
const beforeSwitch = async (index: number): Promise<boolean> => {
  // await等待一个请求，请求回来后再返回true，再进行切换
  // let data = await uni.$u.post("url");
  // 模拟异步操作
  await new Promise(resolve => setTimeout(resolve, 1000));
  return true; // 或者根据逻辑返回false
}
</script>
```

### 3. 返回一个 Promise

```html
<template>
  <u-tabbar :before-switch="beforeSwitch"></u-tabbar>
</template>

<script setup lang="ts">
// 定义切换前返回Promise的回调函数
const beforeSwitch = (index: number): Promise<void> => {
  // 返回一个promise
  return new Promise((resolve, reject) => {
    // 模拟异步请求
    setTimeout(() => {
      // 模拟请求成功的情况
      const success = Math.random() > 0.5; // 50%概率成功
      
      if (success) {
        // resolve()之后，将会进入promise的组件内部的then回调，相当于返回true
        resolve();
      } else {
        // reject()之后，将会进入promise的组件内部的catch回调，相当于返回false
        reject();
      }
    }, 1000);
  });
}
</script>
```

## 边框

组件默认带了顶部边框，如果有配置中部凸起按钮的话，此按钮同时也会有外层边框，如果不需要，配置`border-top`为`false`即可。

## API

## Tabbar Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 | 最低版本 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| list | 各项的配置参数，见顶部说明，数组形式 | Array | - | - |
| show | 是否显示组件 | Boolean | true | false | - |
| v-model | 双向绑定的激活项的索引值 | String | Number | 0 | - | - |
| bg-color | 组件的背景颜色 | String | #ffffff | - | - |
| height | 高度，单位任意，数值则为 rpx 单位，不建议修改 | String | Number | 50px | - | - |
| icon-size | 非中部凸起图标的大小，单位任意，数值则为 rpx 单位 | String | Number | 40 | - | - |
| mid-button-size | 凸起的图标的大小，单位任意，数值则为 rpx 单位 | String | Number | 90 | - | - |
| active-color | 文字和字体图标激活时的颜色 | String | #303133 | - | - |
| inactive-color | 文字和字体图标未激活时的颜色 | String | #606266 | - | - |
| mid-button | 是否需要中部凸起的按钮，配置了此值，依然需要配置`list`参数中需凸起项的`midButton`为`true`，见上方说明 | Boolean | false | true | - |
| before-switch | 切换之前的回调钩子，见上方说明 | Function | - | - | - |
| border-top | 是否显示顶部的边框 | Boolean | true | false | - |
| hide-tab-bar | 是否隐藏原生 tabbar | Boolean | true | false | - |
| text-size | 文字的大小，单位任意，数值则为 rpx 单位 | String | Number | 26 | - |  |

## Events

| 事件名 | 说明 | 回调参数 |
| :--- | :--- | :--- |
| change | 切换选项时触发 | index：当前要切换项的索引 |

---

---
url: 'https://uviewpro.cn/zh/components/table.md'
---
# Table 表格&#x20;

表格组件一般用于展示大量结构化数据的场景

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

本组件标签类似HTML的table表格，由`table`、`tr`、`th`、`td`四个组件组成

* `table`组件裹在最外层，可以配置一些基础参数
* `tr`组件用于显示"行"数据
* `th`组件用于显示表头内容，类似`td`，不同之处在于字体加粗了，也带有背景颜色，也可以直接用`td`替代`th`
* `td`组件不是最小单位，为了合并单元格时，内部可以嵌入`tr`和`td`组件

```html
<template>
	<u-table>
		<u-tr>
			<u-th>学校</u-th>
			<u-th>班级</u-th>
			<u-th>年龄</u-th>
		</u-tr>
		<u-tr>
			<u-td>浙江大学</u-td>
			<u-td>二年级</u-td>
			<u-td>22</u-td>
		</u-tr>
		<u-tr>
			<u-td>清华大学</u-td>
			<u-td>05班</u-td>
			<u-td>20</u-td>
		</u-tr>
	</u-table>
</template>
```

## 兼容性

由于`头条小程序`的兼容性问题，您需要给表格相关的组件(`u-tr`、`u-th`、`u-td`)写上对应的类名才有效，如下：

```html
<u-table>
	<u-tr class="u-tr">
		<u-th class="u-th">姓名</u-th>
		<u-th class="u-th">年龄</u-th>
		<u-th class="u-th">籍贯</u-th>
		<u-th class="u-th">性别</u-th>
	</u-tr>
	<u-tr class="u-tr">
		<u-td class="u-td">吕布</u-td>
		<u-td class="u-td">22</u-td>
		<u-td class="u-td">楚河</u-td>
		<u-td class="u-td">男</u-td>
	</u-tr>
</u-table>
```

## API

## Table Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| border-color | 表格边框的颜色 | String | #e4e7ed | - |
| bg-color | 表格的背景颜色 | String | #ffffff | - |
| align | 单元格的内容对齐方式，作用类似css的`text-align` | String  | center | left / right |
| padding | 单元格的内边距，同css的`padding`写法 | String  | 10rpx 0 | - |
| font-size | 单元格字体大小，单位rpx | String | Number  | 28 | - |
| color | 单元格字体颜色 | String  | #606266 | - |
| th-style | `th`单元格的样式，对象形式(将`th`所需参数放在`table`组件，是为了避免每一个`th`组件要写一遍) | Object  | {} | - |

## Td Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| width | 单元格宽度百分比或者具体带单位的值，如30%， 200rpx等，一般使用百分比，单元格宽度默认为均分`tr`的长度 | String | Number | auto | - |

## Th Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| width | 标题单元格宽度百分比或者具体带单位的值，如30%， 200rpx等，一般使用百分比，单元格宽度默认为均分`tr`的长度 | String | Number | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/tabs.md'
---
# tabs 标签&#x20;

该组件，是一个tabs标签组件，在标签多的时候，可以配置为左右滑动，标签少的时候，可以禁止滑动。
该组件的一个特点是配置为滚动模式时，激活的tab会自动移动到组件的中间位置。


uView中，共有2个组件可以实现tabs标签切换，分别是`tabs`组件，`tabsSwiper`组件，他们的异同点是：

* `tabs`组件可以不结合uni-app`swiper`轮播组件使用，`tabsSwiper`组件是必须要结uni-app`swiper`轮播组件才能使用的。
* `tabs`组件使用更简洁明了(这也是其存在的理由)，`tabsSwiper`组件配置相对复杂一些。
* `tabsSwiper`组件相比`tabs`组件，由于搭配了uni-app`swiper`轮播组件，获得了滑块跟随，标签颜色渐变等效果(请在演示中扫码查看效果)，而`tabs`组件是不具备的。

总的来说，二者配置参数和功能都差不多，看用户的需求自行衡量该使用哪一个组件。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过设置`is-scroll`(默认为`true`)，配置tabs组件的内容是否可以左右拖动，一般4个标签以下时，无需拖动，设置为`false`，5个标签以上，建议可以左右拖动。
* tabs标签的切换，需要绑定`current`值，在`change`事件回调中可以得到`index`，将其赋值给`current`即可。

具体的标签，通过`list`参数配置，该参数要求为数组，元素为对象，对象要有`name`属性，见示例：

:::tip 说明
`is-scroll`参数很重要，如果您的tabs项只有几个，且不想tabs导航栏可以被左右滑动的话，请一定要设置`is-scroll`为`false`，因为它默认为`true`。
:::

```html
<template>
	<u-tabs :list="list" :is-scroll="false" :current="current" @change="change"></u-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义Tab项接口
interface TabItem {
	name: string
	count?: number,
	hidden?: boolean // 是否显示 v0.3.16版本开始支持
}

// 定义响应式数据
const list = ref<TabItem[]>([
	{
		name: '待收货'
	}, {
		name: '待付款'
	}, {
		name: '待评价',
		count: 5
	}
])

const current = ref<number>(0)

// 定义change事件回调函数
const change = (index: number) => {
	current.value = index
}
</script>
```

## 控制组件读取的数组元素属性名

某些情况下，数据可能是从后端获取的，`list`所需的数组中不一定会有`name`属性，比如可能为`cate_name`，如果这种情况还需一定要提供`name`属性
会导致用户需要循环一遍，把`cate_name`改成`name`，显然不人性的，所以uView给tabsSwiper组件提供了一个`name`参数，您可以设置其值为`cate_name`，组件内部会读取数组中的`cate_name`属性，而不是默认的`name`属性。

新增的`count`属性，您可以设置其值为`cate_count`，组件内部会读取数组中的`cate_count`属性，而不是默认的`count`属性。

```html
<template>
	<u-tabs :list="list" :is-scroll="false" :current="current" @change="change"></u-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义Tab项接口
interface TabItem {
	name: string
	count?: number
}

// 定义响应式数据
const list = ref<TabItem[]>([
	{
		name: '待收货'
	}, {
		name: '待付款'
	}, {
		name: '待评价',
		count: 5
	}
])

const current = ref<number>(0)

// 定义change事件回调函数
const change = (index: number) => {
	current.value = index
}
</script>
```

## 手动配置激活的标签

可以通过`current`控制tabs当前的第几个tab处于激活状态

```html
<u-tabs ref="uTabsRef" :list="list" current="2"></u-tabs>
```

## 控制tabs组件的宽度

有时候我们并不想让tabs组件占满整个屏幕的宽度，如果有此需求，可以给tabs外面嵌套一个view元素，控制这个view的宽度或者内外边距，view里面的tabs组件
宽度也会相应的发生变化。

```html
<view style="width: 400rpx;">
	<u-tabs ref="uTabsRef" :list="list" current="2"></u-tabs>
</view>
```

## 控制底部滑块的样式

1. 可以通过`active-color`控制颜色(同时为当前活动tab文字颜色和滑块的颜色)。
2. `bar-width`控制滑块的长度(rpx)。
3. `bar-height`控制滑块高度。

```html
<u-tabs ref="uTabsRef" :list="list" bar-height="6" bar-width="40" active-color="#2979ff"></u-tabs>
```

## 控制tabs组件的活动tab样式

1. 通过`active-color`和`inactive-color`控制tabs的激活和非激活颜色。
2. `font-size`为tabs文字大小。
3. `current`为初始化tabs的激活tab索引，默认为0。`gutter`为单个tab标签的左右内边距之和，即左右各占`gutter`的一半。

```html
<u-tabs ref="uTabsRef" :list="list" active-color="#2979ff" inactive-color="#606266" font-size="30" :current="current"></u-tabs>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| is-scroll | tabs是否可以左右拖动  | Boolean | true | false |
| list | 标签数组，元素为对象，如\[{name: '推荐'}] | Array  | - | - |
| current | 指定哪个tab为激活状态 | String | Number  | 0，即`list`的第一项 | - |
| height | 导航栏的高度，单位rpx | String | Number  | 80 | - |
| font-size | tab文字大小，单位rpx | String | Number  | 30 | - |
| duration | 滑块移动一次所需的时间，单位**秒** | String | Number  | 0.5 | - |
| active-color | 滑块和激活tab文字的颜色  | String | #2979ff | - |
| inactive-color | tabs文字颜色 | String  | #303133 | - |
| bar-width | 滑块宽度，单位rpx | String | Number  | 40 | - |
| bar-height | 滑块高度，单位rpx | String | Number  | 6 | - |
| gutter | 单个tab标签的左右内边距之和，单位rpx | String | Number  | 40 | - |
| bg-color | tabs导航栏的背景颜色 | string  | #ffffff | - |
| name | 组件内部读取的`list`参数中的属性名（tab名称），见上方说明 | string  | name | - |
| bold | 激活选项的字体是否加粗 | Boolean | true | false |
| show-bar | 是否显示底部的滑块 | Boolean | true | false |
| bar-style | 底部滑块的样式，对象形式 | Object | {} | - |
| active-item-style | 当前活动Item的样式，对象形式 | Object | {} | - |
| item-width | 标签的宽度，单位rpx | String | Number  | auto | - |
| count | 组件内部读取的`list`参数中的属性名（badge徽标数），用法与`name`一致，见上方说明 | string  | count | - |
| offset | 设置badge的位置偏移，格式为 \[x, y]，也即设置的为`top`和`right`的值，单位rpx。 | Array  | \[5, 20] | - |

## Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
|change|点击标签时触发|index: 点击了第几个tab，索引从0开始|-|

---

---
url: 'https://uviewpro.cn/zh/components/tabsSwiper.md'
---
# tabsSwiper 全屏选项卡&#x20;

该组件内部实现主要依托于uni-app`scroll-view`和`swiper`组件，主要特色是切换过程中，tabsSwiper文字的颜色可以渐变，底部滑块可以
跟随式滑动，活动tab滚动居中等。应用场景可以用于需要左右切换页面，比如商城的订单中心(待收货-待付款-待评价-已退货)等应用场景。


uView中，共有2个组件可以实现tabs标签切换，分别是`tabs`组件，`tabsSwiper`组件，他们的异同点是：

* `tabs`组件可以不结合uni-app`swiper`轮播组件使用，`tabsSwiper`组件是必须要结uni-app`swiper`轮播组件才能使用的。
* `tabs`组件使用更简洁明了(这也是其存在的理由)，`tabsSwiper`组件配置相对复杂一些。
* `tabsSwiper`组件相比`tabs`组件，由于搭配了uni-app`swiper`轮播组件，获得了滑块跟随，标签颜色渐变等效果(请在演示中扫码查看效果)，而`tabs`组件是不具备的。

总的来说，二者配置参数和功能都差不多，看用户的需求自行衡量该使用哪一个组件。



::: warning 注意

1. 由于支付宝小程序不支持uni的`swiper`组件`transition`事件的`dx`参数，故此组件不支持支付宝小程序
2. 此组件目前为uView的`vue`版本，非`nvue`版本(制作中)，内部使用uni-app`swiper`组件为基础，`swiper`是单页组件，
   适合做简单列表左右滑动，因为性能问题，用swiper做复杂长列表，需要较高的优化技巧以及接受一些限制。如果要实现类似腾讯新闻APP首页可以左右
   滑动复杂的多个tab切换，不建议使用本组件，如果使用，请自行测试列表很长时的切换流畅度。后续uView会对`nvue`进行兼容，增强此组件在APP上的能力。\
   官方有一个`nvue`新闻模板示例，内有左右滑动tab功能，具体参考：\
   [插件市场新闻模板示例](https://ext.dcloud.net.cn/plugin?id=103)
   :::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|x|√|√|√|

## 基本使用

通过设置`is-scroll`(默认为`true`)，配置tabsSwiper组件的内容是否可以左右拖动，一般4个标签以下时，无需拖动，设置为`false`，5个标签以上，建议可以左右拖动。
具体的标签，通过`list`参数配置，该参数要求为数组，元素为对象，对象要有`name`属性，见示例：

:::tip 说明
`is-scroll`参数很重要，如果您的tabs项只有几个，且不想tabs导航栏可以被左右滑动的话，请一定要设置`is-scroll`为`false`，因为它默认为`true`。
:::

```html
<template>
	<u-tabs-swiper ref="uTabsSwiperRef" :list="list" :is-scroll="false"></u-tabs-swiper>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义Tab项接口
interface TabItem {
	name: string
	count?: number
}

// 定义响应式数据
const list = ref<TabItem[]>([
	{
		name: '待收货'
	}, {
		name: '待付款'
	}, {
		name: '待评价',
		count: 5
	}
])
</script>
```

## 控制组件读取的数组元素属性名

某些情况下，数据可能是从后端获取的，`list`所需的数组中不一定会有`name`属性，比如可能为`cate_name`，如果这种情况还需一定要提供`name`属性
会导致用户需要循环一遍，把`cate_name`改成`name`，显然不人性的，所以uView给tabsSwiper组件提供了一个`name`参数，您可以设置其值为`cate_name`，组件内部
会读取数组中的`cate_name`属性，而不是默认的`name`属性。

同理，`count`属性，您可以设置其值为`cate_count`，组件内部会读取数组中的`cate_count`属性，而不是默认的`count`属性。

```html
<template>
  <u-tabs-swiper
    ref="uTabsSwiperRef"
    name="cate_name"
    count="cate_count"
    :list="list"
    :is-scroll="false"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface CateTab {
  cate_name: string
  cate_count?: number
}

const list = ref<CateTab[]>([
  { cate_name: '待收货' },
  { cate_name: '待付款' },
  { cate_name: '待评价', cate_count: 5 }
])
</script>
```

## 控制底部滑块的样式

1. 可以通过`active-color`控制颜色(同时为当前活动tab文字颜色和滑块的颜色)。
2. `bar-width`控制滑块的长度(rpx)。
3. `bar-height`控制滑块高度。

```html
<u-tabs-swiper ref="uTabsSwiperRef" :list="list" bar-height="6" bar-width="40" active-color="#2979ff"></u-tabs-swiper>
```

## 控制tabsSwiper组件的活动tab样式

1. 通过`active-color`和`inactive-color`控制tabsSwiper的激活和非激活颜色。
2. `font-size`为tabsSwiper文字大小。
3. `current`为初始化tabsSwiper的激活tab索引，默认为0。`gutter`为单个tab标签的左右内边距之和，即左右各占`gutter`的一半。

```html
<u-tabs-swiper ref="uTabsSwiperRef" :list="list" active-color="#2979ff" inactive-color="#606266" font-size="30" current="0"></u-tabs-swiper>
```

## 使用案例

该组件**必须**搭配uni-app`swiper`组件才能使用，可以实现左右滑动，同时还可以搭配uView的`loadmore`实现底部加载更多的功能，注意：

* 必须要给组件设置`ref`属性，因为结合uni的`swiper`组件时需要调用tabsSwiper内部的方法，详见示例。
* 本示例中在`swiper-item`中嵌套了`可选`的uni-app`scroll-view`组件，uni官方不建议在APP-vue和小程序中`scroll-view`中使用map、video等原生组件，
* 必须将组件的`current`参数，设置为`animationfinish`中的返回值。

具体请参考：[uni的scroll-view组件文档](https://uniapp.dcloud.io/component/scroll-view)

注意：由于tabsSwiper组件需要结合uni的`swiper`组件使用，过程较为复杂，故此示例代码仅作参考使用，请勿直接复制粘贴使用，
具体使用方法请下载查阅uView的tabsSwiper案例。

```html
<template>
  <view>
    <view>
      <u-tabs-swiper
        ref="uTabsRef"
        :list="list"
        :current="current"
        @change="tabsChange"
        :is-scroll="false"
        swiperWidth="750"
      ></u-tabs-swiper>
    </view>
    <swiper
      :current="swiperCurrent"
      @transition="transition"
      @animationfinish="animationfinish"
    >
      <swiper-item
        class="swiper-item"
        v-for="(item, index) in list"
        :key="index"
      >
        <scroll-view
          scroll-y
          style="height: 800rpx;width: 100%;"
          @scrolltolower="onreachBottom"
        >
          ...
        </scroll-view>
      </swiper-item>
    </swiper>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface TabItem {
  name: string
}

const list = ref<TabItem[]>([
  { name: '十年' },
  { name: '青春' },
  { name: '之约' }
])

// tabs组件的current值，表示当前活动的tab选项
const current = ref(0)
// swiper组件的current值，表示当前那个swiper-item是活动的
const swiperCurrent = ref(0)
const uTabsRef = ref()

function tabsChange(index: number) {
  swiperCurrent.value = index
}

function transition(e: any) {
  const dx = e.detail.dx
  uTabsRef.value?.setDx(dx)
}

// 由于swiper的内部机制问题，快速切换swiper不会触发dx的连续变化，需要在结束时重置状态
// swiper滑动结束，分别设置tabs和swiper的状态
function animationfinish(e: any) {
  const curr = e.detail.current
  uTabsRef.value?.setFinishCurrent(curr)
  swiperCurrent.value = curr
  current.value = curr
}

function onreachBottom() {
  // scroll-view到底部加载更多
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| is-scroll | tabs是否可以左右拖动  | Boolean | true | false |
| list | 标签数组，元素为对象，如\[{name: '推荐'}] | Array  | - | - |
| current | 指定哪个tab为激活状态 | String | Number  | 0，即`list`的第一项 | - |
| height | 导航栏的高度，单位rpx | String | Number  | 80 | - |
| font-size | tab文字大小，单位rpx | String | Number  | 30 | - |
| swiper-width | tabs组件外部swiper的宽度，默认为屏幕宽度，单位rpx | string | Number  | 750 | - |
| active-color | 滑块和激活tab文字的颜色  | String | #2979ff | - |
| inactive-color | tabs文字颜色 | String  | #303133 | - |
| bar-width | 滑块宽度，单位rpx | String | Number  | 40 | - |
| bar-height | 滑块高度，单位rpx | String | Number  | 6 | - |
| gutter | 单个tab标签的左右内边距之和，单位rpx | String | Number  | 40 | - |
| bg-color | tabs导航栏的背景颜色 | string  | #ffffff | - |
| name | 组件内部读取的`list`参数中的属性名（tab名称），见上方说明 | string  | name | - |
| bold | 激活选项的字体是否加粗 | Boolean | true | false |
| show-bar | 是否显示底部的滑块 | Boolean | true | false |
| bar-style | 底部滑块的样式，对象形式 | Object | {} | - |
| active-item-style | 当前活动Item的样式，对象形式 | Object | {} | - |
| count | 组件内部读取的`list`参数中的属性名（badge徽标数），用法与`name`一致，见上方说明 | string  | count | - |
| offset | 设置badge的位置偏移，格式为 \[x, y]，也即设置的为`top`和`right`的值，单位rpx。 | Array  | \[5, 20] | - |

## Events

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
|change|点击标签时触发|index: 点击了第几个tab，索引从0开始|-|

---

---
url: 'https://uviewpro.cn/zh/components/tag.md'
---
# Tag 标签&#x20;

该组件一般用于标记和选择，有如下特点：

* `mode`参数可以设置3种模式，`dark`(深色背景)、`light`(浅色背景)、`plain`(白色背景)
* `shape`参数可以设置多种形状，`circle`（两边半圆形）, `square`（方形，带圆角），`circleLeft`（左边半圆），`circleRight`（右边半圆）
* `type`参数可以设置5种主题，`primary`，`success`，`warning`，`error`，`info`

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`type`参数设置主题类型，默认为`primary`
* `text`设置标签内容

```html
<u-tag text="雪月夜" type="success" />
```

## 设置标签的类型

* 通过设置`mode`参数，可以设置标签的类型，`dark`(深色背景)、`light`(浅色背景)、`plain`(白色背景)

```html
<u-tag text="一丘之貉" mode="dark" />
<u-tag text="沆瀣一气" mode="light" />
<u-tag text="狼狈为奸" mode="plain" />
```

## 设置标签的形状

通过`shape`参数，可以设置标签的形状，默认是`square`（方形，带圆角），可选：`circle`（两边半圆形）, `circleLeft`（左边半圆），`circleRight`（右边半圆）

```html
<u-tag text="主谓宾" shape="circle" />
<u-tag text="定状补" shape="circleLeft" />
```

## 设置标签是否可以关闭

设置`closeable`参数为`true`，会在标签上自动添加一个关闭图标\
设置可关闭后，点击关闭按钮，会发出`close`事件，回调中手动设置`show`参数为`false`，可以隐藏`Tag`

```html
<template>
	<u-tag text="要清楚" closeable :show="show" @close="tagClick" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref(true)

function tagClick(index: number) {
	show.value = false
}
</script>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| type | 主题类型  | String	 | primary | success / info / warning / error |
| size | 标签大小  | String	 | default | mini |
| shape | 标签形状 | String | square | circle / circleLeft / circleRight |
| text | 标签的文字内容 | String | - | - |
| bg-color | 自定义标签的背景颜色 | String  | - | - |
| color | 文字的颜色 | String  | - | - |
| border-color | 标签的边框颜色  | String | - | - |
| close-color | 关闭按钮的颜色  | String | - | - |
| index | 点击标签时，会通过`click`事件返回该值  | String | Number | - | - |
| mode | 模式选择，见上方说明 | String | light | dark / plain |
| closeable | 是否可关闭，设置为`true`，文字右边会出现一个关闭图标  | Boolean | false | true |
| show | 标签显示与否  | Boolean | true | false |

## Slot

| 名称          | 说明            |
|-------------  |---------------- |
| default  | 同 text prop |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| click | 点击标签触发 | index: 传递的`index`参数值 | - |
| close | `closeable`为`true`时，点击标签关闭按钮触发 | index: 传递的`index`参数值 | - |

---

---
url: 'https://uviewpro.cn/zh/tools/test.md'
---
# test 规则校验

uView内置了一些校验规则，如是否手机号，邮箱号，URL等\
这些规则方法，挂载在`$u.test`下面，如验证是否手机号：`$u.test.mobile('13888889999')`，如果验证通过，返回`true`，否则返回`false`

## 是否验证码

### code(value, len = 6)

校验是否验证码(要求为数字)，返回`true`或者`false`。

* `value` \<String> 验证码字符串
* `len` \<Number> 验证码长度，默认为6

```js
console.log(uni.$u.test.code('4567', 4));
```

## 是否数组

### array(array)

校验是否数组，返回`true`或者`false`。

* `array` \<Array> 数组

```js
console.log(uni.$u.test.array([1, 2, 3]));
```

## 是否Json字符串

### jsonString(json)

校验是否数组，返回`true`或者`false`。

* `json` \<Json> Json字符串

注意：请留意json字符串的要求：

1. 整体为一个字符串
2. 字符串对象内的属性需要用`""`双引号包含

```js
console.log(uni.$u.test.jsonString('{"a": 1}'));
```

## 是否对象

### object(object)

校验是否数组，返回`true`或者`false`。

* `object` \<Object> 对象

```js
console.log(uni.$u.test.object({a: 1}));
```

## 是否邮箱号

### email(email)

校验是否邮箱号，返回`true`或者`false`。

* `email` \<String> 字符串

```js
console.log(uni.$u.test.email('123465798@gmail.com'));
```

## 是否手机号

### mobile(mobile)

校验是否手机号，返回`true`或者`false`。

* `mobile` \<String> 字符串

```js
console.log(uni.$u.test.mobile('13845678900'));
```

## 是否URL

### url(url)

校验是否URL链接，返回`true`或者`false`。

* `url` \<String> 字符串

```js
console.log(uni.$u.test.url('https://uviewpro.cn'));
```

## 是否为空

这里指的“空”，包含如下几种情况：

* 值为`undefined`(一种类型)，非字符串`"undefined"`
* 字符串长度为0，也即空字符串
* 值为`false`(布尔类型)，非字符串`"false"`
* 值为数值`0`(非字符串`"0"`)，或者`NaN`
* 值为`null`，空对象`{}`，或者长度为0的数组

### isEmpty(value)

校验值是否为空，返回`true`或者`false`。\
此方法等同于`empty`名称，但是为了更语义化，推荐用`isEmpty`名称。

* `value` \<any> 字符串

```js
console.log(uni.$u.test.isEmpty(false));
```

## 是否普通日期

验证一个字符串是否日期，返回`true`或者`false`，如下行为正确：

* `2020-02-10`、`2020-02-10 08:32:10`、`2020/02/10 3:10`、`2020/02/10 03:10`、`2020/02-10 3:10`

如下为错误：

* `2020年02月10日`、`2020-02-10 25:32`

总的来说，年月日之间可以用"/"或者"-"分隔(不能用中文分隔)，时分秒之间用":"分隔，数值不能超出范围，如月份不能为13，则检验成功，否则失败。

### date(date)

* `date` \<String> 日期字符串

```js
console.log(uni.$u.test.date('2020-02-10 08:32:10'));
```

## 是否十进制数值

整数，小数，负数，带千分位数(2,359.08)等可以检验通过，返回`true`或者`false`。

### number(number)

* `number` \<String> 数字

```js
console.log(uni.$u.test.number('2020'));
```

## 是否整数

所有字符都在`0-9`之间，才校验通过，结果返回`true`或者`false`。

### digits(number)

* `number` \<String> 数字

```js
console.log(uni.$u.test.digits('2020'));
```

## 是否身份证号

身份证号，包括尾数为"X"的类型，可以校验通过，结果返回`true`或者`false`。

### idCard(idCard)

* `idCard` \<String> 身份证号

```js
console.log(uni.$u.test.idCard('110101199003070134'));
```

## 是否车牌号

可以校验旧车牌号和新能源类型车牌号，结果返回`true`或者`false`。

### carNo(carNo)

* `carNo` \<String> 车牌号

```js
console.log(uni.$u.test.carNo('京A88888'));
```

## 是否金额

最多两位小数，可以带千分位，结果返回`true`或者`false`。

### amount(amount)

* `amount` \<String> 金额字符串

```js
console.log(uni.$u.test.amount('3,233.08'));
```

## 是否汉字

可以为单个汉字，或者汉字组成的字符串，结果返回`true`或者`false`。

### chinese(zh)

* `zh` \<String> 中文字符串

```js
console.log(uni.$u.test.chinese('更上一层楼'));
```

## 是否字母

只能为"a-z"或者"A-Z"之间的字符，结果返回`true`或者`false`。

### letter(en)

* `en` \<String> 字母串

```js
console.log(uni.$u.test.letter('uView'));
```

## 是否字母或者数字

只能是字母或者数字，结果返回`true`或者`false`。

### enOrNum(str)

* `str` \<String> 字母或者数字字符串

```js
console.log(uni.$u.test.enOrNum('uView'));
```

## 是否包含某个值

字符串中是否包含某一个子字符串，区分大小写，结果返回`true`或者`false`。

### contains(str, subStr)

* `str` \<String> 字符串
* `subStr` \<String> 子字符串

```js
console.log(uni.$u.test.contains('uView', 'View'));
```

## 数值是否在某个范围内

如30在"29-35"这个范围内，不在"25-28"这个范围内，结果返回`true`或者`false`。

### range(number, range)

* `number` \<Number> 数值
* `range` \<Array> 如"\[25-35]"

```js
console.log(uni.$u.test.range(35, [30, 34]));
```

## 字符串长度是否在某个范围内

如"abc"长度为3，范围在"2-5"这个区间，结果返回`true`或者`false`。

### rangeLength(str, range)

* `str` \<String> 数值
* `range` \<Array> 如"\[25, 35]"

```js
console.log(uni.$u.test.rangeLength('abc', [3, 10]));
```

---

---
url: 'https://uviewpro.cn/zh/components/text.md'
---
# Text 文本 &#x20;

此组件集成了文本类在项目中的常用功能，包括状态，拨打电话，格式化日期，\*替换，超链接...等功能。
您大可不必在使用特殊文本时自己定义，text组件几乎涵盖您能使用的大部分场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 通过`text`参数设置文本内容。推荐您使用`:text='value'`的形式

```html
<u-text text="我用十年青春,赴你最后之约"></u-text>
```

## 设置主题

* 通过`type`参数设置文本主题，我们提供了五类属性。
* `primary  error  success  warning  info`

```html
<u-text type="primary" text="主色"></u-text>
<u-text type="error"   text="错误"></u-text>
<u-text type="success" text="成功"></u-text>
<u-text type="warning" text="警告"></u-text>
<u-text type="info"    text="信息"></u-text>
```

## 拨打电话

* 通过将`mode`属性设置为`phone`即可调用拨打电话，提供加密值`encrypt`
* 除此之外还有格式化日期，姓名脱敏，超链接，千分位金额等属性，将在以下实例中展示

```html
<u-text mode="phone" text="15019479320"></u-text>
```

## 日期格式化

```html
<u-text mode="date" text="1612959739"></u-text>
```

## 姓名脱敏

```html
<u-text mode="name" text="张三三" format="encrypt"></u-text>
```

## 超链接

添加`href`指定链接地址

```html
<u-text mode="link" text="Go to uView docs" href="https://www.uviewui.com" ></u-text>
```

## 显示金额

```html
<u-text mode="price" text="728732.32"></u-text>
```

## 前后图标

添加`prefixIcon,suffixIcon`指定图标和位置，`iconStyle`设置图标大小

```html
<u-text prefixIcon="baidu" iconStyle="font-size: 19px" text="百度一下,你就知道"></u-text>
<u-text suffixIcon="arrow-leftward" iconStyle="font-size: 18px" text="查看更多"></u-text>
```

## 超出隐藏

内置了文字超出隐藏样式，设置`lines`属性表明几行后隐藏

```html
<u-text 
    :lines="2" 
    text="uView Pro 是在 uView 1.8.8 官方组件库基础上，采用 Vue3 全新语法彻底重构的 uni-app 生态框架。不同于
    市面上的其他 uView 框架等兼容 Vue3 的方案，uView Pro 并非简单兼容，而是对每一个组件和工具进行源码级重构，
    充分发挥 Vue3 的响应式和组合式优势，API 设计更现代，性能更优越。">
</u-text>
```

## 小程序开放能力

针对小程序开放能力，我们提供了分享，请在小程序环境下使用

```html
<u-text text="分享到微信" openType="share" type="success" @click="clickHandler"></u-text>
<script>
	export default {
		onLoad() {},
		methods: {
			clickHandler() {
				// #ifndef MP-WEIXIN
				uni.$u.toast('请在微信小程序内查看效果')
				// #endif
			}
		},
	}
</script>
```

## API

## List Props

|参数|说明|类型|默认值|可选值|
|:-|:-|:-|:-|:-|
|type|主题颜色|String|-|-|
|show|是否显示|Boolean|true|false|
|text|显示的值|String|Number|-|-|
|prefixIcon|前置图标|String|-|-|
|suffixIcon|后置图标|String|-|-|
|mode|文本处理的匹配模式text-普通文本，price-价格，phone-手机号，name-姓名，date-日期，link-超链接|String|-||
|href|mode=link下，配置的链接|String|-|-|
|format|格式化规则|String|Function|-|-|
|call|mode=phone时，点击文本是否拨打电话|Boolean|false|true|
|openType|小程序的打开方式|String|-|-|
|bold|是否粗体，默认normal|Boolean|false|true|
|block|是否块状|Boolean|false|true|
|lines|文本显示的行数，如果设置，超出此行数，将会显示省略号|String|Number|-|-|
|color|文本颜色|String|#303133|-|
|size|字体大小|String|Number|15|-|
|iconStyle|图标的样式|Object|String|15px|-|
|decoration|文字装饰，下划线，中划线等|String|none|underline/line-through|
|margin|外边距，对象、字符串，数值形式均可|Object|Number|String|-|-|
|lineHeight|文本行高|Number|String|-|-|
|align|文本对齐方式(仅block="true"方式生效)|String|left|center/right|
|wordWrap|文字换行|String|normal|break-word/anywhere|

## List Events

|事件名|说明|回调参数|
|:-|:-|:-|
|click|点击触发事件|-|

---

---
url: 'https://uviewpro.cn/zh/components/textarea.md'
---
# Textarea 文本域 &#x20;

文本域此组件满足了可能出现的表单信息补充，编辑等实际逻辑的功能，内置了字数校验等，和 [u-input](/zh/components/input.html) 的 textarea 基本一致。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

```html
<template>
  <u-textarea v-model="value1" placeholder="请输入内容" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const value1 = ref<string>('')
</script>
```

## 字数统计

```html
<template>
  <u-textarea v-model="value2" placeholder="请输入内容" count />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const value2 = ref<string>('统计字数')
</script>
```

## 自动增高

```html
<template>
  <u-textarea v-model="value3" placeholder="请输入内容" autoHeight />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const value3 = ref<string>('')
</script>
```

## 禁用状态

设置`disabled`属性实现进行禁用，您也可以动态设置是否禁用

```html
<template>
  <u-textarea v-model="value4" placeholder="文本域已被禁用" disabled count />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const value4 = ref<string>('')
</script>
```

## 下划线模式

设置`border="bottom"`属性单独设置底部下划线

```html
<template>
  <u-textarea v-model="value5" placeholder="请输入内容" border="bottom" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
const value5 = ref<string>('')
</script>
```

## 格式化处理

如有需要，可以通过`formatter`参数编写自定义格式化规则。

```html
<template>
	<u-textarea v-model="value" :formatter="formatter" ref="textarea" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const value = ref<string>('')
const textarea = ref<any>(null)

function formatter(val: string) {
	// 让输入框只能输入数值，过滤其他字符
	return val.replace(/[^0-9]/ig, '')
}
</script>
```

## API

## Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
|:- |:- |:- |:-: |:-: |
| value | 输入框的内容 | String | String | - | - |
| placeholder | 输入框为空时占位符 | Number | String | - | - |
| height | 输入框高度 | String | Number | 70 | - |
| confirmType | 设置键盘右下角按钮的文字，仅微信小程序、App-vue 和 H5 有效 | String | done | - |
| disabled | 是否禁用 | Boolean | false | true |
| count | 是否显示统计字数 | Boolean | false | true |
| focus | 是否自动获取焦点，nvue 不支持，H5 取决于浏览器实现 | Boolean | false | true |
| autoHeight | 是否自动增加高度 | Boolean | false | true |
| ignoreCompositionEvent | 是否忽略组件内对文本合成系统事件的处理。为 false 时将触发 compositionstart、compositionend、compositionupdate 事件，且在文本合成期间会触发 input 事件 | Boolean | true | false |
| fixed | 如果 textarea 在一个 position:fixed 的区域，需要显示指定属性 fixed 为 true | Boolean | false | true |
| cursorSpacing | 指定光标与键盘的距离 | Number | 0 | - |
| cursor | 指定 focus 时的光标位置 | Number | String | - | - |
| showConfirmBar | 是否显示键盘上方带有“完成”按钮的那一栏 | Boolean | true | false |
| selectionStart | 光标起始位置，自动聚焦时有效，需与 selectionEnd 搭配使用 | Number | -1 | - |
| selectionEnd | 光标结束位置，自动聚焦时有效，需与 selectionStart 搭配使用 | Number | -1 | - |
| adjustPosition | 键盘弹起时，是否自动上推页面 | Boolean | true | false |
| disableDefaultPadding | 是否去掉 iOS 下的默认内边距（仅微信小程序有效） | Boolean | false | true |
| holdKeyboard | focus 时，点击页面不会收起键盘（仅微信小程序有效） | Boolean | false | true |
| maxlength | 最大输入长度，设置为 -1 时不限制最大长度 | String | Number | 140 | - |
| border | 边框类型：surround-四周边框，none-无边框，bottom-底部边框 | String | surround | bottom |
| placeholderClass | 指定 placeholder 的样式类，注意当页面或组件使用 scoped 时需在类名前写 /deep/ | String | textarea-placeholder | - |
| placeholderStyle | 指定 placeholder 的样式，字符串或对象形式，如 "color: red;" | String | Object | color: #c0c4cc | - |
| formatter | 输入过滤或格式化函数 | Function | null | - |
| ignoreCompositionEvent | 是否忽略组件内对文本合成系统事件的处理 | Boolean | true | false |

## Events

| 事件名 | 说明 | 回调参数 |
|:-|:-|:-|
| focus | 输入框聚焦时触发，`event.detail = { value, height }`，height 为键盘高度 | event |
| blur | 输入框失去焦点时触发，`event.detail = {value, cursor}` | event |
| linechange | 输入框行数变化时调用，`event.detail = {height: 0, heightRpx: 0, lineCount: 0}` | event |
| input | 当键盘输入时，触发 `input` 事件 | `event.detail.value` |
| confirm | 点击完成时， 触发 `confirm` 事件 | event |
| keyboardheightchange | 键盘高度发生变化的时候触发此事件 | event |

---

---
url: 'https://uviewpro.cn/zh/tools/debounce.md'
---
# throttle & debounce节流防抖

### 何谓节流和防抖？

* 节流\
  节流的意思是，规定时间内，只触发一次。比如我们设定500ms，在这个时间内，无论点击按钮多少次，它都只会触发一次。具体场景可以是抢购时候，由于有无数人
  快速点击按钮，如果每次点击都发送请求，就会给服务器造成巨大的压力，但是我们进行节流后，就会大大减少请求的次数。

* 防抖\
  防抖的意思是，在连续的操作中，无论进行了多长时间，只有某一次的操作后在指定的时间内没有再操作，这一次才被判定有效。具体场景可以搜索框输入关键字过程中实时
  请求服务器匹配搜索结果，如果不进行处理，那么就是输入框内容一直变化，导致一直发送请求。如果进行防抖处理，结果就是当我们输入内容完成后，一定时间(比如500ms)没有再
  输入内容，这时再触发请求。

结合以上两种情况，回到我们最实际的场景，比如防止表单提交按钮被多次触发，我们应该选择使用`节流`而不是`防抖`方案。

:::tip 温馨提示
uView内置的按钮组件`u-button`内部已做节流处理，无需外部再做节流处理。配置`throttle-time`参数，可以设置节流的时间，详见[Button 按钮](/zh/components/button.html)
:::

## 节流

### throttle(func, wait = 500, immediate = true)

规定时间内，只触发一次，可以通过设置`immediate`来决定触发的时机在这个时间的开始，还是结束的时候执行。

* `func` \<Function> 触发回调执行的函数
* `wait` \<Number> 时间间隔，单位ms
* `immediate` \<Number> 在开始还是结束处触发，比如设置`wait`为1000ms，如果在一秒内进行了5次操作，只触发一次，如果`immediate`为`true`，那么就会在第一次操作
  触发回调，如果为`false`，就会在第5次操作触发回调。

```html
<template>
    <view class="">
		<!-- 此处用法为在模板中使用，无需写this，直接$u.throttle()即可 -->
    	<view class="throttle" @tap="$u.throttle(btnAClick, 500)">
    		露从今夜白
    	</view>
    	<view class="throttle" @tap="btnBClick">
    		月是故乡明
    	</view>
    </view>
</template>

<script setup lang="ts">
import { $u } from 'uview-pro'

function btnAClick() {
	console.log('btnClick');
},
function btnBClick() {
	$u.throttle(toNext, 500)
},
function toNext() {
	console.log('btnBClick');
}
</script>

<style lang="scss">
    .throttle {
		margin-top: 50rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100rpx;
		border: 1px solid $u-type-primary;
	}
</style>
```

## 防抖

### debounce(func, wait = 500, immediate = false)

在连续的操作中，无论进行了多长时间，只有某一次的操作后在指定的时间内没有再操作，这一次才被判定有效

* `func` \<Function> 触发回调执行的函数
* `wait` \<Number> 时间间隔，单位ms
* `immediate` \<Number> 在开始还是结束处触发，如非特殊情况，一般默认为`false`即可

```html
<template>
    <view class="">
		<!-- 此处用法为在模板中使用，无需写this，直接$u.debounce()即可 -->
    	<view class="debounce" @tap="$u.debounce(btnAClick, 500)">
    		露从今夜白
    	</view>
    	<view class="debounce" @tap="btnBClick">
    		月是故乡明
    	</view>
    </view>
</template>

<script setup lang="ts">
import { $u } from 'uview-pro'

function btnAClick() {
	console.log('btnClick');
},
function btnBClick() {
	$u.debounce(toNext, 500)
},
function toNext() {
	console.log('btnBClick');
}
</script>

<style lang="scss">
    .debounce {
		margin-top: 50rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100rpx;
		border: 1px solid $u-type-primary;
	}
</style>
```

---

---
url: 'https://uviewpro.cn/zh/tools/time.md'
---
# time 时间格式

## 格式化时间

### timeFormat | date(timestamp, format = "yyyy-mm-dd")

**注意**：date和timeFormat为同功能不同名函数，无论用哪个方法名，都是一样的。

该函数必须传入第一个参数，第二个参数是可选的，函数返回一个格式化好的时间。

* `time` \<String> 任何合法的时间格式、`秒`或`毫秒`的时间戳
* `format` \<String> 时间格式，可选。默认为`yyyy-mm-dd`，年为"yyyy"，月为"mm"，日为"dd"，时为"hh"，分为"MM"，秒为"ss"，格式可以自由搭配，如：
  `yyyy:mm:dd`，`yyyy-mm-dd`，`yyyy年mm月dd日`，`yyyy年mm月dd日 hh时MM分ss秒`，`yyyy/mm/dd/`，`MM:ss`等组合

```html
<template>
	<view>
		<view>
			时间为：{{ $u.timeFormat(timestamp, 'yyyy年mm月dd日') }}
		</view>
		<view>
			时间为：{{ time }}
		</view>
	</view>
</template>

<script setup>
import { $u } from 'uview-pro'
import { ref, onMounted } from 'vue';

const time = ref(null);
const timestamp = ref('1581170184');

onMounted(() => {
  time.value = $u.timeFormat(timestamp.value, 'yyyy-mm-dd');
});
</script>
```

## 多久以前

### timeFrom(time, format = String | false)

该函数必须传入第一个参数，格式为任何合法的时间格式、`秒`或`毫秒`的时间戳，第二个参数是可选的，返回的值类似`刚刚`，`25分钟前`，`3小时前`，`7天前`的结果。
如果第二个参数是时间的格式，当前和传入时间戳相差大于一个月时，返回格式化好的时间；如果第二个参数为`false`，则不会返回格式化好的时间，而是诸如"xxx年前"的结果。

* `timestamp` \<String> 时间戳
* `format` \<String / false> 时间格式，默认为`yyyy-mm-dd`，年为"yyyy"，月为"mm"，日为"dd"，时为"hh"，分为"MM"，秒为"ss"，格式可以自由搭配，如：
  `yyyy:mm:dd`，`yyyy-mm-dd`，`yyyy年mm月dd日`，`yyyy年mm月dd日 hh时MM分ss秒`，`yyyy/mm/dd/`，`MM:ss`等组合。
  如果时间戳距离此时的时间，大于一个月，则返回一个格式化好的时间，如果此参数为`false`，返回均为"多久之前"的结果。

```html
<template>
	<view>
		<view>
			时间为：{{ $u.timeFrom(timestamp, 'yyyy年mm月dd日') }}
		</view>
		<view>
			时间为：{{ time }}
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { $u } from 'uview-pro';

const time = ref(null);
const timestamp = ref('1581170184');

onMounted(() => {
  time.value = $u.timeFrom(timestamp.value, 'yyyy年mm月dd日');
});
</script>
```

---

---
url: 'https://uviewpro.cn/zh/components/timeLine.md'
---
# TimeLine 时间轴&#x20;

时间轴组件一般用于物流信息展示，各种跟时间相关的记录等场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 该组件左边图标默认为显示一个点，如需自定义，请通过name为`node`的`slot`传入内容
* 组件右边内容为了更强的自定义，需要请通过name为`content`的`slot`传入

以下为基本示例，完整示例请见演示部分

```html
<template>
	<u-time-line>
		<u-time-line-item nodeTop="2">
			<!-- 此处自定义了左边内容，用一个图标替代 -->
			<template v-slot:node>
				<view class="u-node" style="background: #19be6b;">
					<!-- 此处为uView的icon组件 -->
					<u-icon name="pushpin-fill" color="#fff" :size="24"></u-icon>
				</view>
			</template>
			<template v-slot:content>
				<view>
					<view class="u-order-title">待取件</view>
					<view class="u-order-desc">[自提柜]您的快件已放在楼下侧门，直走前方53.6米，左拐约10步，再右拐直走，见一红灯笼停下，叩门三下，喊“芝麻开门”即可。</view>
					<view class="u-order-time">2019-05-08 12:12</view>
				</view>
			</template>
		</u-time-line-item>
		<u-time-line-item>
			<!-- 此处没有自定义左边的内容，会默认显示一个点 -->
			<template v-slot:content>
				<view>
					<view class="u-order-desc">【深圳市】日照香炉生紫烟，遥看瀑布挂前川，飞流直下三千尺，疑是银河落九天。</view>
					<view class="u-order-time">2019-12-06 22:30</view>
				</view>
			</template>
		</u-time-line-item>
	</u-time-line>
</template>

<style lang="scss" scoped>
	.u-node {
		width: 44rpx;
		height: 44rpx;
		border-radius: 100rpx;
		display: flex;
		justify-content: center;
		align-items: center;
		background: #d0d0d0;
	}
	
	.u-order-title {
		color: #333333;
		font-weight: bold;
		font-size: 32rpx;
	}
	
	.u-order-desc {
		color: rgb(150, 150, 150);
		font-size: 28rpx;
		margin-bottom: 6rpx;
	}
	
	.u-order-time {
		color: rgb(200, 200, 200);
		font-size: 26rpx;
	}
</style>
```

## 注意事项

如果自定义了左边的图标等内容，有可能左边的图标无法和右边的内容平齐，可以调整`time-line-item`组件的`node-top`参数来达到想要的效果

```html
<u-time-line-item node-top="2">
	<template v-slot:node>
		<u-icon name="pushpin-fill" color="#ddd" :size="24"></u-icon>
	</template>
	<template v-slot:content>
		......
	</template>
</u-time-line-item>
```

## API

## TiemLimeItem Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| bg-color | 左边节点的背景颜色，一般通过slot内容自定义背景颜色即可 | String | #ffffff | - |
| node-top | 节点左边图标绝对定位的top值，单位rpx | String | Number | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/toast.md'
---
# Toast 消息提示&#x20;

此组件表现形式类似uni的`uni.showToast`API，但也有不同的地方，具体表现在：

* uView Pro的`toast`有5种主题可选
* 可以配置toast结束后，跳转相应URL
* 目前没有加载中的状态，请用uni的`uni.showLoading`，这个需求uni已经做得很好

:::warning 注意：
由于uni中无法通过js创建元素，所以需要在页面中调用`<toast />`组件，再通过`ref`开启
:::

## 基本使用

以下为一个模拟登录成功后，弹出toast提示，并在一定时间(默认2000ms)后，自动跳转页面到个人中心页(也可以配置跳转的参数)的示例

```html
<template>
	<view>
		<u-toast ref="uToastRef" />
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const uToastRef = ref()

function showToast() {
	// 通过ref调用uToast组件的show方法
	uToastRef.value?.show({
		title: '登录成功',
		type: 'success',
		url: '/pages/user/index'
	})
}
</script>
```

## 配置toast主题

一共有6种主题可选，如下：

* default-灰黑色，最普通的场景，此为默认主题，可以不用填`type`参数
* error-红色，代表错误
* success-绿色，代表成功
* warning-黄色，代表警告
* info-灰色，比default浅一点
* primary-蓝色，uView的主色调

除了`default`状态，其他5种主题，都是默认带有一个左边的图标，可以通过配置`icon`参数为`none`来取消

```js
uToastRef.value?.show({
	title: '操作成功',
	// 如果不传此type参数，默认为default，也可以手动写上 type: 'default'
	// type: 'success', 
	// 如果不需要图标，请设置为false
	// icon: false
})
```

## toast结束跳转URL

* 如果配置了`url`参数，在toast结束的时候，就会用`uni.navigateTo`(默认)或者`uni.switchTab`(需另外设置`isTab`为`true`)
* 如果配置了`params`参数，就会在跳转时自动在URL后面拼接上这些参数，具体用法如下：

```js
uToastRef.value?.show({
	title: '操作成功',
	url: '/pages/user/index',
	params: {
		id: 1,
		menu: 3
	}
})
```

## API

## Props

| 参数      | 说明        | 类型     |  默认值  |  可选值   |
|-----------|-----------|----------|----------|---------|
| z-index | toast展示时的`z-index`值  | String | Number | 10090 | - |

## Params

这些参数为通过`ref`调用`<toast/>`组件内部的`show`方法时，需要传递参数

| 参数      | 说明        | 类型     |  默认值  |  可选值   |
|-----------|-----------|----------|----------|---------|
| title | 显示的文本  | String | - | - |
| type | 主题类型，不填默认为`default` | String  | default | primary / success / error / warning / info |
| duration | toast的持续时间，单位ms | Nubmer  | 2000 | - |
| url | toast结束跳转的url，不填不跳转，优先级高于`back`参数 | String  | - | - |
| icon | 是否显示显示`type`对应的图标，为`false`不显示图标 | Boolean  | true | false |
| position | toast出现的位置 | String  | center | top / bottom |
| callback | toast结束后执行的回调方法 | Function  | - | - |
| isTab | toast结束后，跳转tab页面时需要配置为`true` | Boolean  | false | true |
| back | toast结束后，是否返回上一页，优先级低于`url`参数 | Boolean  | false | true |

## Methods

方法是通过`ref`调用的，参见上方说明
注意：所有有关`ref`的调用，都不能在页面的`onLoad`生命周期调用，因为此时组件尚未创建完毕，会报错，应该在`onReady`生命周期调用。

|方法名|说明|参数|版本|
|:-|:-|:-|:-|
| show | 显示toast，如需一进入页面就显示toast，请在`onReady`生命周期调用 | 见上方说明 |  -  |

---

---
url: 'https://uviewpro.cn/zh/components/topTips.md'
---
# TopTips 顶部提示&#x20;

该组件一般用于页面顶部向下滑出一个提示，尔后自动收起的场景。

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

该组件通过`ref`调用，使用简单，只需`title`参数设置显示的内容即可

注意：不要在onLoad中调用，应在onReady生命周期调用，因为onLoad生命周期组件尚未创建完成

```html
<template>
	<u-top-tips ref="uTipsRef"></u-top-tips>
</template>

<script setup lang="ts">
import { ref, onReady } from 'vue'

// 定义u-top-tips组件的引用
const uTipsRef = ref()

// 在onReady生命周期中调用
onReady(() => {
	if (uTipsRef.value) {
		uTipsRef.value.show({
			title: '铁马冰河入梦来',
			type: 'success',
			duration: '2300'
		})
	}
})
</script>
```

## 自定义导航栏使用本组件的问题

**注意：** 只有使用了自定义导航栏才需要注意如下事项，否则无需在意，不用处理。

由于本组件是预先将组件隐藏于导航栏底部，调用时显示，内部已兼容处理H5，APP，小程序等的系统导航栏高度问题。\
但是如果您是使用了自定义导航栏的话，组件内部不知道您的自定义导航栏高度是多少，可能会显示有误，所以您需要传入一个`navbar-height`参数(**单位为px**)。\
需要注意的是，这个`navbar-height`参数是您自定义导航栏的整个高度，比如在APP和各家小程序上，是“导航栏”+“状态栏”的高度，H5中，“状态栏”无法自定义，高度为0。

:::tip 温馨提示
uView 有推出[Navbar 自定义导航栏](/zh/components/navbar.html)组件，此组件有一个`height`参数(**单位px**，默认44)，这个高度是不包含状态栏的高度的，
所以您使用uView的自定义导航栏组件的话，您还需要通过"uni.getSystemInfoSync().statusBarHeight"(字节跳动小程序不支持)去获得状态栏的高度，
加上你需要的导航栏高度(也即uView的`navbar`组件的`height`)，即为需要传入`u-top-tips`组件的`navbar-height`参数值。
:::

使用uView自定导航栏可进行如下处理，如果是其他的UI框架的导航栏或者自己做的导航栏组件，请以此类推，也能不需要下面的处理。

```html
<template>
	<view class="wrap">
		<u-navbar title="文章列表"></u-navbar>
		<u-top-tips ref="uTipsRef" :navbar-height="statusBarHeight + navbarHeight"></u-top-tips>
		<u-button @click="showTips">弹出Tips</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义u-top-tips组件的引用
const uTipsRef = ref()

// 状态栏高度，H5中，此值为0，因为H5不可操作状态栏
const statusBarHeight = uni.getSystemInfoSync().statusBarHeight
// 导航栏内容区域高度，不包括状态栏高度在内
const navbarHeight = ref<number>(44)

// 定义showTips方法
const showTips = () => {
	if (uTipsRef.value) {
		uTipsRef.value.show({
			title: '雨打梨花深闭门，忘了青春，误了青春'
		})
	}
}
</script>

<style lang="scss" scoped>
.wrap {
	padding: 40rpx;
}
</style>
```

## 主题设置

可以通过配置`type`参数设置显示的背景颜色：

* `type`值可选的有`primary`(默认)、`success`、`info`、`warning`、`error`

## 显示时间设置

* `duration`值设置显示的时间，单位ms：

## API

## Methods

需要注意的是，这里的参数是通过`ref`调用的，调用方法如上方"基本使用"中所示

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| title | 要显示的内容  | String | - | - |
| type | 主题选择  | String | primary | success / info / warning / error |
| duration | 显示的时间，单位ms |  String | Number | - |

## Props

需要注意到是，这里的参数是需要通过`props`调用的，只有**使用了自定义导航栏**才需要配置，见上方说明。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| navbar-height | 导航栏高度(包含状态栏高度在内)，单位PX  | String | Number | - | - |
| z-index | `z-index`值 | String | Number | 975 | - |

---

---
url: 'https://uviewpro.cn/zh/tools/trim.md'
---
# trim 去除空格

### trim(str, pos)

该方法可以去除空格，分别可以去除所有空格，两端空格，左边空格，右边空格，默认为去除两端空格

* `str` \<String> 字符串
* `pos` \<String> 去除那些位置的空格，可选为：`both`-默认值，去除两端空格，`left`-去除左边空格，`right`-去除右边空格，`all`-去除包括中间和两端的所有空格

```js
console.log(uni.$u.trim('abc    b ', 'all')); // 去除所有空格
console.log(uni.$u.trim(' abc '));	// 去除两端空格
```

---

---
url: 'https://uviewpro.cn/zh/tools/http.md'
---
# uni-app 轻量级 Http 请求库&#x20;

支持 TypeScript、Vue3、组合式 API，插件化、全局配置、请求/响应拦截器、toast/loading 灵活控制，开箱即用，适合中小型项目。目前不适用于其他的请求形式，比如上传，下载等。

## 平台兼容性

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

:::tip 提示
put/delete 在某些小程序平台的限制：

* 1.delete 请求，不支持支付宝和头条小程序(HX2.6.15)
* 2.put 请求，不支持支付宝小程序(HX2.6.15)
  :::

## 特性亮点

* 支持 get/post/put/delete 四种常用请求
* 插件化注册，支持全局配置和拦截器
* toast、loading 可全局/单次请求灵活配置
* 拦截器支持 token 注入、统一错误处理、登录失效跳转等
* TypeScript 类型友好，支持组合式 API
* 可通过 `$u.http.get/post` 方式调用（需 import { $u } from 'uview-pro'）
* 适配 H5、App、各主流小程序平台

## 基本用法

### 组合式 API

```ts
import { http } from 'uview-pro'

// GET
http.get('/api/user', { id: 1 }).then(res => {
  /* ... */
})

// POST
http.post('/api/login', { username: 'xx', password: 'xx' }).then(res => {
  /* ... */
})

// PUT/DELETE
http.put('/api/user/1', { name: 'new' })
http.delete('/api/user/1')
```

### await/async

```ts
const res = await http.post('/api/login', { username: 'xx' })
```

### 自定义 header

```ts
http.get(
  '/api/user',
  {},
  {
    header: { Authorization: 'Bearer token' }
  }
)
```

## 全局与动态配置

### 全局配置

```ts
import { http } from 'uview-pro'

http.setConfig({
  baseUrl: 'https://api.example.com',
  meta: {
    toast: true, // 全局开启错误toast，默认为false关闭
    loading: true, // 全局开启loading，默认为false关闭
    originalData: true // 是否在拦截器中返回服务端的原始数据，默认为true返回的是原始数据
  }
})
```

### 单次请求动态配置

```ts
http.post(
  '/api/login',
  { username: 'xx' },
  {
    meta: { toast: true, loading: true }
  }
)
```

## 最佳实践-推荐

### 1. 创建拦截器文件

```ts
import type { RequestConfig, RequestInterceptor, RequestMeta, RequestOptions } from 'uview-pro'
import { useUserStore } from '@/store'

// 全局请求配置
export const httpRequestConfig: RequestConfig = {
  baseUrl,
  header: {
    'content-type': 'application/json'
  },
  meta: {
    originalData: true,
    toast: true,
    loading: true
  }
}

// 全局请求/响应拦截器
export const httpInterceptor: RequestInterceptor = {
  request: (config: RequestOptions) => {
    const meta: RequestMeta = config.meta || {}
    if (meta.loading) {
      // 显示loading
    }
    const userStore = useUserStore()
    if (userStore.token) {
      config.header.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  response: (response: any) => {
    const meta: RequestMeta = response.config?.meta || {}
    if (meta.loading) {
      // 隐藏loading
    }

    // 根据业务处理错误、例如登录失效等处理接口返回错误码
    if (response.data.code !== 200) {
      if (meta.toast) {
        // 可以弹出错误toast
      }
      throw new Error('接口返回错误码，根据业务处理，可以弹出toast')
    }
    return response.data
  }
}
```

***

### 2. 注册插件（main.ts）

已经定义好全局请求配置和请求/响应拦截器，可以在main.ts 中注册：

```ts
import { createSSRApp } from 'vue'
import uViewPro, { httpPlugin } from 'uview-pro'
import { httpInterceptor, httpRequestConfig } from 'http.interceptor'

export function createApp() {
  const app = createSSRApp(App)

  // 注册uView-pro
  app.use(uViewPro)

  // 注册http插件
  app.use(httpPlugin, {
    interceptor: httpInterceptor,
    requestConfig: httpRequestConfig
  })

  return { app }
}
```

***

### 3. API 管理

建议将所有接口统一封装到 `api/index.ts`，便于维护和类型推断：

```ts
// api/index.ts
import { http } from 'uview-pro'

export const login = data => http.post('/api/login', data)
export const getUser = id => http.get('/api/user', { id })
```

页面中直接调用：

```ts
import { login, getUser } from '@/api'

const user = await getUser(1)
```

***

### 4. $u 工具库用法

> 需 import { $u } from 'uview-pro'
>
> $u.http.get/post/put/delete 参数与 http 保持一致

```ts
import { $u } from 'uview-pro'

$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })
$u.http.post('/api/login', { username: 'xx' }, { meta: { loading: true } })

// 或
uni.$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })
```

## 进阶用法

### 多实例/多拦截器

```ts
import { Request } from 'uview-pro'

const customHttp = new Request()
customHttp.setConfig({ baseUrl: 'https://other.api.com' })
customHttp.interceptor.request = config => {
  // ...自定义逻辑
  return config
}
export { customHttp }
```

### 扩展 meta 字段

你可以在 meta 中扩展自定义参数，在拦截器中读取：

```ts
http.get('/api/user', {}, { meta: { toast: true, customFlag: true } })
// 在拦截器中：config.meta?.customFlag
```

### 结合 hooks 封装

```ts
// hooks/useApi.ts
import { http } from 'uview-pro'
export function useApi() {
  return {
    login: data => http.post('/api/login', data),
    getUser: id => http.get('/api/user', { id })
  }
}
```

## 类型提示与 TS 支持

* 所有请求方法均有完整类型推断
* 支持泛型：`http.get<MyResType>(url)`
* 支持自定义 Request/Response 类型
* 推荐在 api 层定义类型，页面调用自动推断

## 常见问题 FAQ

### 1. 如何全局配置 baseUrl、header、meta？

> 使用 `http.setConfig({ ... })`，建议在 main.ts 或拦截器注册前调用。

### 2. 如何单次请求自定义 toast/loading？

> 通过 meta 字段：`http.post(url, data, { meta: { toast: true, loading: true } })`

### 3. 如何自定义拦截器？

> 参考 http.interceptor.ts，request/response 可灵活扩展。

### 4. 如何在组合式 API 中优雅使用？

> 直接 `import { http }`，无需 getCurrentInstance。

### 5. 如何处理多环境/多 baseUrl？

> 可通过 setConfig 动态切换，或 new Request() 多实例。

### 6. 如何捕获和处理错误？

> 建议统一在 response 拦截器处理，页面可用 try/catch 或 .catch。

### 7. $u.http.get/post 与 http 有什么区别？

> $u.http.get/post 适配 uview-pro 导出的 http，参数与 http 完全一致，底层同一实现。
> 即以下方式是同等的：

```js
import { $u, http } from 'uview-pro'

// 方式一
http.get('/api/user', { id: 1 }, { meta: { toast: true } })

// 方式二
$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })

// 方式三
uni.$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })
```

### 8. put/delete 在小程序平台有限制吗？

> put/delete 在支付宝、头条等部分平台有限制，详见最上方提示。

***

---

---
url: 'https://uviewpro.cn/zh/tools/request.md'
---
# uni-app 轻量级 Http 请求库&#x20;

支持 TypeScript、Vue3、组合式 API，插件化、全局配置、请求/响应拦截器、toast/loading 灵活控制，开箱即用，适合中小型项目。目前不适用于其他的请求形式，比如上传，下载等。

## 平台兼容性

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

:::tip 提示
put/delete 在某些小程序平台的限制：

* 1.delete请求，不支持支付宝和头条小程序(HX2.6.15)
* 2.put请求，不支持支付宝小程序(HX2.6.15)
  :::

***

## 特性亮点

* 支持 get/post/put/delete 四种常用请求
* 插件化注册，支持全局配置和拦截器
* toast、loading 可全局/单次请求灵活配置
* 拦截器支持 token 注入、统一错误处理、登录失效跳转等
* TypeScript 类型友好，支持组合式 API
* 可通过 `$u.http.get/post` 方式调用（需 import { $u } from 'uview-pro'）
* 适配 H5、App、各主流小程序平台

***

## 快速开始

### 1. 注册插件（main.ts）

如何定义全局请求配置和请求/响应拦截器，看下面：[#拦截器最佳实践](#拦截器最佳实践)

```ts
import { createSSRApp } from 'vue'
import uViewPro, { httpPlugin } from 'uview-pro'
import { httpInterceptor, httpRequestConfig } from 'http.interceptor'

export function createApp() {
  const app = createSSRApp(App)

  // 注册uView-pro
  app.use(uViewPro)

  // 注册http插件
  app.use(httpPlugin, {
    interceptor: httpInterceptor,
    requestConfig: httpRequestConfig,
  })

  return { app }
}
```

***

## 全局与动态配置

### 全局配置

```ts
import { http } from 'uview-pro'

http.setConfig({
  baseUrl: 'https://api.example.com',
  meta: {
    toast: true, // 全局开启错误toast，默认为false关闭
    loading: true, // 全局开启loading，默认为false关闭
    originalData: true, // 是否在拦截器中返回服务端的原始数据，默认为true返回的是原始数据
  },
})
```

### 单次请求动态配置

```ts
http.post('/api/login', { username: 'xx' }, {
  meta: { toast: true, loading: true }
})
```

***

## 基本用法

### 组合式 API

```ts
import { http } from 'uview-pro'

// GET
http.get('/api/user', { id: 1 }).then(res => { /* ... */ })

// POST
http.post('/api/login', { username: 'xx', password: 'xx' }).then(res => { /* ... */ })

// PUT/DELETE
http.put('/api/user/1', { name: 'new' })
http.delete('/api/user/1')
```

### await/async

```ts
const res = await http.post('/api/login', { username: 'xx' })
```

### 自定义 header

```ts
http.get('/api/user', {}, {
  header: { Authorization: 'Bearer token' }
})
```

***

## 拦截器最佳实践

### http.interceptor.ts 示例

```ts
import type { RequestConfig, RequestInterceptor, RequestMeta } from 'uview-pro'
import { useUserStore } from '@/store'

// 全局请求配置
export const httpRequestConfig: RequestConfig = {
    baseUrl,
    header: {
        'content-type': 'application/json'
    },
    meta: {
        originalData: true,
        toast: true,
        loading: true
    }
};

// 全局请求/响应拦截器
export const httpInterceptor: RequestInterceptor = {
  request: (config) => {
    const meta: RequestMeta = config.meta || {}
    if (meta.loading) {
      // 显示loading
    }
    const userStore = useUserStore()
    if (userStore.token) {
      config.header.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  response: (response) => {
    const meta: RequestMeta = response.config?.meta || {}
    if (meta.loading) {
      // 隐藏loading
    }

    // 根据业务处理错误、例如登录失效等处理接口返回错误码
    if (response.data.code !== 200) {
      if (meta.toast) {
        // 可以弹出错误toast
      }
      throw new Error('接口返回错误码，根据业务处理，可以弹出toast')
    }
    return response.data
  },
}
```

***

## $u 工具库用法

> 需 import { $u } from 'uview-pro'
>
> $u.http.get/post/put/delete 参数与 http 保持一致

```ts
import { $u } from 'uview-pro'

$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })
$u.http.post('/api/login', { username: 'xx' }, { meta: { loading: true } })

// 或
uni.$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })
```

***

## API 管理推荐

建议将所有接口统一封装到 `api/index.ts`，便于维护和类型推断：

```ts
// api/index.ts
import { http } from 'uview-pro'

export const login = (data) => http.post('/api/login', data)
export const getUser = (id) => http.get('/api/user', { id })
```

页面中直接调用：

```ts
import { login, getUser } from '@/api'

const user = await getUser(1)
```

***

## 进阶用法

### 多实例/多拦截器

```ts
import { Request } from 'uview-pro'

const customHttp = new Request()
customHttp.setConfig({ baseUrl: 'https://other.api.com' })
customHttp.interceptor.request = (config) => {
  // ...自定义逻辑
  return config
}
```

### 扩展 meta 字段

你可以在 meta 中扩展自定义参数，在拦截器中读取：

```ts
http.get('/api/user', {}, { meta: { toast: true, customFlag: true } })
// 在拦截器中：config.meta?.customFlag
```

### 结合 hooks 封装

```ts
// hooks/useApi.ts
import { http } from 'uview-pro'
export function useApi() {
  return {
    login: (data) => http.post('/api/login', data),
    getUser: (id) => http.get('/api/user', { id }),
  }
}
```

***

## 类型提示与 TS 支持

* 所有请求方法均有完整类型推断
* 支持泛型：`http.get<MyResType>(url)`
* 支持自定义 Request/Response 类型
* 推荐在 api 层定义类型，页面调用自动推断

***

## 常见问题 FAQ

### 1. 如何全局配置 baseUrl、header、meta？

> 使用 `http.setConfig({ ... })`，建议在 main.ts 或拦截器注册前调用。

### 2. 如何单次请求自定义 toast/loading？

> 通过 meta 字段：`http.post(url, data, { meta: { toast: true, loading: true } })`

### 3. 如何自定义拦截器？

> 参考 http.interceptor.ts，request/response 可灵活扩展。

### 4. 如何在组合式 API 中优雅使用？

> 直接 `import { http }`，无需 getCurrentInstance。

### 5. 如何处理多环境/多 baseUrl？

> 可通过 setConfig 动态切换，或 new Request() 多实例。

### 6. 如何捕获和处理错误？

> 建议统一在 response 拦截器处理，页面可用 try/catch 或 .catch。

### 7. $u.http.get/post 与 http 有什么区别？

> $u.http.get/post 适配 uview-pro 导出的 http，参数与 http 完全一致，底层同一实现。
> 即以下方式是同等的：

```js
import { $u, http } from 'uview-pro'

// 方式一
http.get('/api/user', { id: 1 }, { meta: { toast: true } })

// 方式二
$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })

// 方式三
uni.$u.http.get('/api/user', { id: 1 }, { meta: { toast: true } })

```

### 8. put/delete 在小程序平台有限制吗？

> put/delete 在支付宝、头条等部分平台有限制，详见最上方提示。

***

---

---
url: 'https://uviewpro.cn/zh/components/uniModulesSetting.md'
---
# uni\_modules 安装方式配置

uView Pro 提供了多种安装方式，本文将介绍如何使用 uni\_modules 方式进行配置。

## 准备工作

在进行配置之前，请确保您已经根据[安装](/zh/components/install.html)中的步骤对 uView Pro 进行了下载安装，如果没有，请先下载安装。

## 配置步骤

### 1. 引入 uView 主库

在项目根目录中的`main.ts`中，引入并使用 uView Pro 的工具库，注意这两行要放在`import Vue`之后。

```js
// main.ts
import { createSSRApp } from "vue";
import uViewPro from "@/uni_modules/uview-pro";

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro);
  // 其他配置
  return {
    app,
  };
}
```

### 2. 在引入 uView Pro 的全局 SCSS 主题文件

在项目根目录的`uni.scss`中引入此文件。

```css
/* uni.scss */
@import "@/uni_modules/uview-pro/theme.scss";
```

### 3. 引入 uView Pro 基础样式

:::danger 注意！
在`App.vue`中**首行**的位置引入，注意给 style 标签加入 lang="scss"属性
:::

```css
<style lang="scss">
	/* 注意要写在第一行，同时给style标签加入lang="scss"属性 */
	@import "@/uni_modules/uview-pro/index.scss";
</style>
```

## 3. 配置自动引入组件

### 基于 easycom 配置自动引入组件方案 1

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
    }
  },
  "pages": [
    // ...
  ]
}
```

:::tip 注意

* 1.修改 `easycom` 规则后需重启 HX 或重新编译项目。
* 2.请确保 `pages.json` 中只有一个 easycom 字段，否则请自行合并多个规则。
* 3.一定要放在 `custom` 内，否则无效。
  :::

### 基于 vite 配置自动引入组件方案 2

如果不熟悉 `easycom`，也可以通过 [@uni-helper/vite-plugin-uni-components](https://github.com/uni-helper/vite-plugin-uni-components) 实现组件的自动引入。

:::tip 提醒

* 推荐使用 `@uni-helper/vite-plugin-uni-components@0.2.1` 及以上版本，因为在 0.2.1 版本开始其内置了 `uView Pro` 的`resolver`。
* 如果使用此方案时控制台打印很多 `Sourcemap for  points to missing source files​` ，可以尝试将 `Vite` 版本升级至 `4.5.x` 以上版本。

:::

::: code-group

```bash [npm]
npm i @uni-helper/vite-plugin-uni-components -D
```

```bash [yarn]
yarn add @uni-helper/vite-plugin-uni-components -D
```

```bash [pnpm]
pnpm add @uni-helper/vite-plugin-uni-components -D
```

:::

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

import Components from '@uni-helper/vite-plugin-uni-components'
import { uViewProResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'

export default defineConfig({
  plugins: [
    // make sure put it before `Uni()`
    Components({
      resolvers: [uViewProResolver()]
    }),
    uni()
  ]
})
```

如果你使用 `pnpm` ，请在根目录下创建一个 `.npmrc` 文件，参见 [Issue](https://github.com/antfu/unplugin-vue-components/issues/389)。

```text
// .npmrc
public-hoist-pattern[]=@vue*
// or
// shamefully-hoist = true
```

---

---
url: 'https://uviewpro.cn/zh/components/read.md'
---


---

---
url: 'https://uviewpro.cn/zh/components/upload.md'
---
# Upload 上传&#x20;

该组件用于上传图片场景

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

* 可以通过设置`file-list`参数(数组，元素为对象)，显示预置的图片。其中元素的`url`属性为图片路径
* 设置`action`参数为后端服务器地址，注意H5在浏览器可能会有跨域限制，让后端允许域即可

```html
<template>
    <u-upload :action="action" :file-list="fileList" ></u-upload>
</template>

<script setup lang="ts">
// 演示地址，请勿直接使用
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const fileList = ref([
    {
        url: 'http://pics.sc.chinaz.com/files/pic/pic9/201912/hpic1886.jpg',
    }
])
</script>
```

## 手动上传

组件默认为自动上传，可以设置`auto-upload`为`false`，然后通过`ref`调用组件的`upload`方法，手动上传图片

```html
<!-- 手动上传 -->
<template>
    <view>
        <u-upload ref="uUploadRef" :action="action" :auto-upload="false" ></u-upload>
        <u-button @click="submit">提交</u-button>
    </view>
</template>

<script setup lang="ts">
// 非真实地址
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function submit() {
    uUploadRef.value?.upload()
}
</script>
```

## 获取上传的图片列表

图片选择或者上传成功后，会保存在组件内部的`lists`数组中，数组元素为对象，有如下属性：

* url: 图片地址
* error：组件内部使用，不应根据此值判断上传是否成功，而应根据`progress`属性
* progress：如果值为100，表示图片上传成功
* response：上传成功后，服务器返回的数据，这是最有用的了

为了获得上传的文件列表，可以在提交表单时，通过`ref`获取组件内部的`lists`文件数组，历遍元素筛选出`progress`为100的文件

```html
<!-- 获取上传的图片列表 -->
<template>
    <view>
        <u-upload ref="uUploadRef" :action="action" :auto-upload="true" ></u-upload>
        <u-button @click="submit">提交</u-button>
    </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function submit() {
    let files = []
    // 通过filter，筛选出上传进度为100的文件(因为某些上传失败的文件，进度值不为100，这个是可选的操作)
    files = uUploadRef.value?.lists.filter((val: any) => {
        return val.progress == 100
    })
    // 如果您不需要进行太多的处理，直接如下即可
    // files = uUploadRef.value?.lists
    console.log(files)
}
</script>
```

## 报错提示

在以下几种情况，组件会默认通过toast提示用户信息，可以把`show-tips`设置为`false`取消默认的提示，这时可以通过API
中的各种事件，进行自定义的个性化提示

* 超出允许的最大上传数量
* 图片大小超出最大允许大小
* 上传图片出错
* 移除图片

以下示例为屏蔽组件内部的提示，在移除图片时，监听`onRemove`事件，手动提示的情况

```html
<!-- 屏蔽组件内部的提示，在移除图片时，监听onRemove事件，手动提示的情况 -->
<template>
    <u-upload ref="uUploadRef" :action="action" :show-tips="false" @on-remove="onRemove"></u-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const action = ref('http://www.example.com/upload')
const uUploadRef = ref()

function onRemove(index: number, lists: any[]) {
    console.log('图片已被移除')
}
</script>
```

## 限制图片数量和大小

* 通过`max-count`可以设置最多可以选择的图片的数量
* 通过`max-size`设置单张图片最大的大小，单位为B(byte)，默认不限制

下方示例为单张最大为5M，最多选择6张的情况：

```html
<u-upload :max-size="5 * 1024 * 1024" max-count="6"></u-upload>
```

## 上传前的钩子

某些时候，**每个文件**上传前可能需要动态修改文件名，修改额外参数等，就会需要用到一个叫`before-upload`的钩子(参数注意不要加括号)，也即回调方法，此方法会返回两个参数：

* `index`——即当前上传文件在上传列表中的索引
* `lists`——当前所有的文件列表

此回调可以返回一个`promise`、`true`，或者`false`，下面分别阐述三者的处理情况：

* `false`——如果返回`false`，将会跳过当前文件，继续上传下一张图片(如果有)，并且再次执行`before-upload`钩子
* `true`——如果返回`true`，会随即上传当前文件，上传成功后，继续上传下一张图片(如果有)，并且再次执行`before-upload`钩子
* `promise`——如果返回的是一个`promise`，如果进入`then`回调，就会和返回`true`的情况一样，如果进入`catch`回调，就会和返回`false`的情况一样

下面举例说明：

### 1. 普通返回

```html
<!-- before-upload 普通返回 -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
function beforeUpload(index: number, list: any[]) {
    // 只上传偶数索引的文件
    if(index % 2 == 0) return true;
    else return false;
}
</script>
```

### 2. 请求之后再返回

```html
<!-- before-upload 请求之后再返回 -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
async function beforeUpload(index: number, list: any[]) {
    // await等待一个请求，请求回来后再返回true，继续上传文件
    let data = await uni.$u.post('url');
    return true; // 或者根据逻辑返回false
}
</script>
```

### 3. 返回一个Promise

```html
<!-- before-upload 返回一个Promise -->
<template>
    <u-upload :before-upload="beforeUpload"></u-upload>
</template>

<script setup lang="ts">
function beforeUpload(index: number, list: any[]) {
    // 返回一个promise
    return new Promise((resolve, reject) => {
        uni.$u.post('url').then(res => {
            // resolve()之后，将会进入promise的组件内部的then回调，相当于返回true
            resolve();
        }).catch(err => {
            // reject()之后，将会进入promise的组件内部的catch回调，相当于返回false
            reject();
        })
    })
}
</script>
```

## 移除前的钩子

某些时候，文件被移除前可能需要进行判断是否可以被移除，就会需要用到一个叫`before-remove`的钩子(参数注意不要加括号)，也即回调方法，此方法会返回两个参数：

* `index`——即当前上传文件在上传列表中的索引
* `lists`——当前所有的文件列表

此回调可以返回一个`promise`、`true`，或者`false`，下面分别阐述三者的处理情况：

* `false`——如果返回`false`，终止移除操作
* `true`——如果返回`true`，执行移除操作
* `promise`——如果返回的是一个`promise`，如果进入`then`回调，就会和返回`true`的情况一样，如果进入`catch`回调，就会和返回`false`的情况一样

此处不举例说明，参考`before-upload`的示例即可。

## 自定义相关说明

1. 组件内部样式\
   组件默认选取图片会展示预览缩略图，包括默认的选取图片的按钮，他们的宽高都是`200rpx`，`border-radius`值为`10rpx`，
   另外预览图片的盒子有一个默认的边框，值为`border: 1px solid rgb(235, 236, 238)`。如果用户需要自定义上传按钮，可以参考这些值。

2. 自定义上传按钮\
   通过传递名为`addBtn`的`slot`，同时配置`custom-btn`为`true`，可以自定义想要的上传按钮。

如下所示：

```html
<u-upload :custom-btn="true">
	<template #addBtn>
		<view class="slot-btn" hover-class="slot-btn__hover" hover-stay-time="150">
			<u-icon name="photo" size="60" color="#2979ff"></u-icon>
		</view>
	</template>
</u-upload>

<style>
.slot-btn {
	width: 329rpx;
	height: 140rpx;
	display: flex;
	justify-content: center;
	align-items: center;
	background: rgb(244, 245, 246);
	border-radius: 10rpx;
}

.slot-btn__hover {
	background-color: rgb(235, 236, 238);
}
</style>
```

3. 自定义预览列表
   首先需要设置`show-upload-list`为`false`来去除组件内部的默认预览列表，其次需要通过`ref`获取组件，进而
   操作组件内部的变量和方法，下面为一些组件内部的方法和变量说明：

* `lists`(变量)，可以通过此值，构建自定义的预览列表，该变量内部如下：

```js
lists = [
	{
		url: 'xxx.png', // 预览图片的地址
		error: false, // 上传失败，此值为true
		progress: 100, // 0-100之间的值
	},
	......
]
```

* `deleteItem(index)`(方法)，可以用此方法在自定义列表中通过`ref`删除某一张图片

以下为完整的自定义图片预览列表示例：

```html
<!-- 自定义图片预览列表 -->
<template>
    <view class="wrap">
        <view class="pre-box" v-if="!showUploadList">
            <view class="pre-item" v-for="(item, index) in lists" :key="index">
                <image class="pre-item-image" :src="item.url" mode="aspectFill"></image>
            </view>
        </view>
        <u-upload :custom-btn="true" ref="uUploadRef" :show-upload-list="showUploadList" :action="action">
            <template #addBtn>
                <view class="slot-btn" hover-class="slot-btn__hover" hover-stay-time="150">
                    <u-icon name="photo" size="60" color="#c0c4cc"></u-icon>
                </view>
            </template>
        </u-upload>
    </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const action = ref('http://www.example.com') // 演示地址
const showUploadList = ref(false)
const uUploadRef = ref()
const lists = ref<any[]>([])

// 只有onMounted生命周期才能调用refs操作组件
onMounted(() => {
    // 得到整个组件对象，内部图片列表变量为"lists"
    lists.value = uUploadRef.value?.lists || []
})
</script>

<style lang="scss">
    .wrap {
        padding: 24rpx;
    }
    
    .slot-btn {
        width: 341rpx;
        height: 140rpx;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgb(244, 245, 246);
        border-radius: 10rpx;
    }

    .slot-btn__hover {
        background-color: rgb(235, 236, 238);
    }

    .pre-box {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .pre-item {
        flex: 0 0 48.5%;
        border-radius: 10rpx;
        height: 140rpx;
        overflow: hidden;
        position: relative;
        margin-bottom: 20rpx;
    }

    .pre-item-image {
        width: 100%;
        height: 140rpx;
    }
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| action | 服务器上传地址  | String | - | - |
| max-count | 最大选择图片的数量 | String | Number | 99 | - |
| width | 图片预览区域和添加图片按钮的宽度，单位rpx，不能是百分比，或者`auto` | String | Number | 200 | - |
| height | 图片预览区域和添加图片按钮的高度，单位rpx，不能是百分比，或者`auto` | String | Number | 200 | - |
| custom-btn | 如果需要自定义选择图片的按钮，设置为`true` | Boolean | false | true |
| show-progress | 是否显示进度条 | Boolean  | true | false |
| disabled | 是否启用(显示/隐藏)组件 | Boolean  | false | true |
| image-mode | 预览图片等显示模式，可选值为uni的image的`mode`属性值 | String  | aspectFill | - |
| header | 上传携带的头信息，对象形式 | Object | {} | - |
| form-data | 上传额外携带的参数 | Object | {} | - |
| name | 上传文件的字段名，供后端获取使用 | String  | file | - |
| size-type | original 原图，compressed 压缩图，默认二者都有，H5无效 | Array\<String>  | \['original', 'compressed'] | - |
| source-type | 选择图片的来源，album-从相册选图，camera-使用相机，默认二者都有 | Array\<String>  | \['album', 'camera'] | - |
| preview-full-image | 是否可以通过`uni.previewImage`预览已选择的图片 | Boolean  | true | false |
| multiple | 是否开启图片多选，部分安卓机型不支持  | Boolean  | true | false |
| deletable | 是否显示删除图片的按钮 | Boolean  | true | false |
| max-size | 选择单个文件的最大大小，单位B(byte)，默认不限制 | String | Number  | Number.MAX\_VALUE | - |
| file-list | 默认显示的图片列表，数组元素为对象，必须提供`url`属性 | Array\<Object>  | - | - |
| upload-text | 选择图片按钮的提示文字 | String  | 选择图片 | - |
| auto-upload | 选择完图片是否自动上传，见上方说明 | Boolean  | true | false |
| show-tips | 特殊情况下是否自动提示toast，见上方说明 | Boolean  | true | false |
| show-upload-list | 是否显示组件内部的图片预览 | Boolean  | true | false |
| del-icon | 右上角删除图标名称，只能为uView内置图标 | String  | close | - |
| del-bg-color | 右上角关闭按钮的背景颜色 | String  | #fa3534 | - |
| del-color | 右上角关闭按钮图标的颜色 | String  | #ffffff | - |
| to-json | 如果上传后服务端返回的值为`json`字符串的话，是否自动转为`json` | Boolean | true  | false |
| before-upload | 每个文件上传前触发的钩子回调函数，见上方说明，注意不要加括号 | Function | - | - |
| limitType | 允许的图片后缀 | Array | \['png', 'jpg', 'jpeg', 'webp', 'gif'] | - |
| index  | 在各个回调事件中的最后一个参数返回，用于区别是哪一个组件的事件 | String | Number  | - | - |

## Methods

此方法如要通过ref手动调用

| 名称          | 说明            |
|-------------  |---------------- |
| upload | 调用此方法，手动上传图片  |
| clear | 调用此方法，清空内部文件列表  |
| reUpload | 调用此方法，重新上传内部上传失败或者尚未上传的图片  |
| remove(index) | 手动移除列表的某一个图片，`index`为`lists`数组的索引  |

## Slot

|名称|说明|
|:-|:-|
| addBtn | 自定义的选择图片按钮 |

## Events

回调参数中的`lists`参数，为目前组件内的所有图片数组，`index`为当前操作的图片的索引，`name`为通过`props`传递的`index`参数：

|事件名|说明|回调参数|
|:-|:-|:-|
| on-oversize | 图片大小超出最大允许大小 | (file, lists, name), name为通过`props`传递的`index`参数 |
| on-preview | 全屏预览图片时触发 | (url, lists, name)，url为当前选中的图片地址，index为通过`props`传递的`index`参数 |
| on-remove | 移除图片时触发 | (index, lists, name)，name为通过`props`传递的`index`参数 |
| on-success | 图片上传成功时触发 | (data, index, lists, name)，data为服务器返回的数据，name为通过`props`传递的`index`参数 |
| on-change | 图片上传后，无论成功或者失败都会触发 | (res, index, lists, name)，res为服务器返回的信息，name为通过`props`传递的`index`参数 |
| on-error | 图片上传失败时触发 | (res, index, lists, name)，res为服务器返回的信息，name为通过`props`传递的`index`参数 |
| on-progress | 图片上传过程中的进度变化过程触发 | (res, index, lists, name)，res为服务器返回的信息，具体参数请打印查看，name为通过`props`传递的`index`参数 |
| on-uploaded | 所有图片上传完毕触发 | (lists, name)，可以通过此事件，将lists参数获取，提交给后端使用，name为通过`props`传递的`index`参数 |
| on-choose-complete | 每次选择图片后触发，只是让外部可以得知每次选择后，内部的文件列表 | (lists, name)，内部当前的文件列表，name为通过`props`传递的`index`参数 |
| on-list-change | 当内部文件列表被加入文件、移除文件，或手动调用`clear`方法时触发 | (lists, name)，内部文件变化之后的列表，name为通过`props`传递的`index`参数 |
| on-choose-fail | 选择文件出错时触发，比如选择文件时取消了操作，只在微信和APP有效 | (error)，错误信息 |

---

---
url: 'https://uviewpro.cn/zh.md'
---


---

---
url: 'https://uviewpro.cn/zh/resource/harmony.md'
---
# uView Pro 鸿蒙应用正式上线 🎉

## 体验跨平台 UI 组件库在 HarmonyOS 上的完整能力

uView Pro 鸿蒙端应用已正式登陆华为应用市场，为您提供完整的组件展示、业务场景演示和开发体验。

## 📱 应用信息

**应用名称：** uViewPro（跨平台 UI 组件库）

**应用市场：** 华为应用市场（AppGallery）

**下载链接：** <https://appgallery.huawei.com/app/detail?id=cn.anyup.uviewpro>

## 📲 下载方式

### 方式一：扫描二维码下载

![扫描二维码下载 uView Pro 鸿蒙应用](/images/qr_harmony.png)

### 方式二：应用市场下载

直接访问华为应用市场搜索 **uViewPro** 或点击下方链接：

👉 [前往华为应用市场下载](https://appgallery.huawei.com/app/detail?id=cn.anyup.uviewpro)

## ⚠️ 系统要求

**重要提示：** 此应用仅在 **HarmonyOS 5.0 及以上版本** 设备的应用市场中提供。

请确保您的设备系统版本满足要求后再进行下载。

## ✨ 核心功能

uView Pro 鸿蒙应用提供完整的业务场景演示平台，包含：

* **组件库展示** - 丰富的 UI 组件，覆盖日常开发所需
* **模板示例** - 实用的页面模板，快速搭建应用
* **场景案例** - 真实业务场景演示，了解组件实际应用
* **一键复制下载** - 便捷的代码获取方式，提升开发效率

帮助开发者快速上手并体验组件的实际应用价值。

## 📸 应用预览

![uView Pro 鸿蒙应用界面预览](/images/harmony_preview.png)

## 🎯 关于 uView Pro

uView Pro 是一个功能强大的跨平台 UI 组件库，致力于为开发者提供高质量、易用的组件解决方案。现在，您可以在鸿蒙设备上直接体验 uView Pro 的完整功能，感受组件在实际应用中的表现。

***

**立即下载体验，开启您的鸿蒙开发之旅！** 🚀

---

---
url: 'https://uviewpro.cn/zh/components/vuexDetail.md'
---
# uView简化Vuex写法的基本原理

`vuex`传统写法简单，但是也很繁琐：

1. 我们需要在`vuex`中定义`state`和`mutations`
2. 我们需要在每个用到`vuex`变量的地方，都引入`mapState`，同时还要解构到`computed`中去
3. 修改`vuex`变量的时候，还需要通过`commit`提交
4. 由于`vuex`变量是保存在运行内存中的，刷新浏览器`vuex`变量会消失，还需要通过其他手段实现变量的存续

* 针对上面的第1点，我们写了一个统一的`mutations`，用于更新所有的`state`变量，这样可以免去每个变量都要写一个对应的`mutations`步骤，同时在
  这个统一的`mutations`中，根据配置判断是否在变量更新的时候，把它存进本地`Local Storage`，这样H5刷新或者APP下次启动，就会自动把这些变量赋值给
  `state`

具体实现如下(当然，这可能不是最优的写法)

```js
// 根目录的/store/index.js

$uStore(state, payload) {
	// 判断是否多层级调用，state中为对象存在的情况，诸如user.info.score = 1
	let nameArr = payload.name.split('.');
	let saveKey = '';
	let len = nameArr.length;
	if(nameArr.length >= 2) {
		let obj = state[nameArr[0]];
		for(let i = 1; i < len - 1; i ++) {
			obj = obj[nameArr[i]];
		}
		obj[nameArr[len - 1]] = payload.value;
		saveKey = nameArr[0];
	} else {
		// 单层级变量，在state就是一个普通变量的情况
		state[payload.name] = payload.value;
		saveKey = payload.name;
	}
	saveLifeData(saveKey, state[saveKey])
}
```

* 针对上面第二点，我们通过`Vue.mixin`全局混入的形式，可以很好的解决。`mixin`会把内容注入到每一个页面，所以我们在其中写了`mapState`到`computed`，
  每个页面自然地就获得了从`vuex`的`state`中注入的全局变量，这里我们需要在uni-app目根目录新建一个`store`文件夹(如果没有的话)，
  在其中新建一个`$u.mixin.js`文件，这个文件无需您手动引入和`Vue.mixin`处理，uView会自动处理，只为让您少写两行代码。

```js
// $u.mixin.js的部分实现

import { mapState } from 'vuex'
import store from "@/store"

// 尝试将用户在根目录中的store/index.js的vuex的state变量，全部加载到全局变量中
let $uStoreKey = [];
try{
	$uStoreKey = store.state ? Object.keys(store.state) : [];
}catch(e){}

module.exports = {
	computed: {
		// 将vuex的state中的所有变量，解构到全局混入的mixin中
		...mapState($uStoreKey)
	}
}
```

* 针对上面的第3点，因为我们通过统一的`mutations`的去更新`state`，自然就需要一个统一方法去触发`mutations`，用以替代原来的`commit`方法，
  具体是将此方法顺带写入到`$u.mixin.js`，并挂载到`this.$u`中，命名为`vuex`，见如下：

```js
module.exports = {
	created() {
		// 将vuex方法挂在到$u中
		// 使用方法为：如果要修改vuex的state中的user.name变量为"史诗" => uni.$u.vuex('user.name', '史诗')
		// 如果要修改vuex的state的version变量为1.0.1 => uni.$u.vuex('version', '1.0.1')
		uni.$u.vuex = (name, value) => {
			this.$store.commit('$uStore', {
				name,value
			})
		}
	}
}
```

当我们要修改某一个`state`值的时候，就用`uni.$u.vuex('name', value)`的形式，通过其他办法，也可以实现`this.name = value`的简写，但是这种方式
不支持对象的修改，同时也会造成其他的问题，这里不做过多讨论。

* 针对第4点，其实已经在第1点中解决了。

上面的做法，只是抛砖引玉的做了一个思路的解析，如果您有更好的思路，也可以和我们分享。

说明：确保您是新项目的情况下，或者您对这个实现方法很清楚，才使用这个方法。

---

---
url: 'https://uviewpro.cn/zh/components/verificationCode.md'
---
# VerificationCode 验证码倒计时&#x20;

考虑到用户实际发送验证码的场景，可能是一个按钮，也可能是一段文字，提示语各有不同，所以本组件
不提供界面显示，只提供提示语，由用户将提示语嵌入到具体的场景

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

通过ref获取组件对象，再执行后面的操作，见下方示例。

1. 通过`seconds`设置需要倒计的秒数(默认`60`)
2. 通过ref调用组件内部的`start`方法，开始倒计时
3. 通过监听`change`事件(从开始到结束之间，每秒触发一次)获得提示的文字，可能值如"获取验证码|12秒后重新获取|重新获取"，可以自定义

注意：用户可能在倒计时的过程中点击获取验证码的按钮，组件内部提供了通过ref获取的`canGetCode`变量，在倒计时
过程中，该值为`false`，如果为`false`应该给予提示并不要再次向后端请求验证码，如果为`true`，则为获取验证码
之前，或者倒计结束之后，可以再次向后端请求验证码。

以下为完整示例，见如下：

```html
<template>
	<view class="wrap">
		<u-toast ref="uToast"></u-toast>
		<u-verification-code :seconds="seconds" @end="end" @start="start" ref="uCodeRef" 
		@change="codeChange"></u-verification-code>
		<u-button @tap="getCode">{{tips}}</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const tips = ref('')
const seconds = ref(10)
const uCodeRef = ref()

function codeChange(text: string) {
  tips.value = text
}

function getCode() {
  if (uCodeRef.value?.canGetCode) {
    // 模拟向后端请求验证码
    uni.showLoading({
      title: '正在获取验证码'
    })
    setTimeout(() => {
      uni.hideLoading()
      // 这里此提示会被start方法中的提示覆盖
      uni.$u.toast('验证码已发送')
      // 通知验证码组件内部开始倒计时
      uCodeRef.value?.start()
    }, 2000)
  } else {
    uni.$u.toast('倒计时结束后再发送')
  }
}

function end() {
  uni.$u.toast('倒计时结束')
}

function start() {
  uni.$u.toast('倒计时开始')
}
</script>

<style lang="scss" scoped>
	.wrap {
		padding: 24rpx;
	}
</style>
```

## 自定义提示语

组件内部有内置的提示语，如获取验证码前的提示语为"获取验证码"，用户可以通过参数配置自定义的提示：

* 获取前，参数为`start-text`，默认值为"获取验证码"
* 倒计时期间，参数为`change-text`，默认为"X秒重新获取"，这里的"x"(大小写均可)，将会被倒计的秒数替代
* 倒计时结束，参数为`end-text`，默认值为"重新获取"

## 保持倒计时

一般情况下，在H5刷新浏览器，或者各端返回再进入时，倒计时会消失，导致用户可以再次尝试获取验证码，虽然后端还会对此进行进一步的判断。\
对于这种情况，uView给出了一个`keep-running`参数(默认为`false`)，为`true`的时候，即使刷新浏览器，或者返回上一个页面，
倒计时依然会继续(如果还在倒计时间内的话)。

**注意：** 如果您的一个页面或者多个页面同时使用了多个此组件，为了防止多个组件之间，保存在本地的多个继续倒计时的变量之间互相干扰，可以配置
各个组件的`unique-key`为一个不重复的字符串，以作区分：

```html
/* A.vue */
<u-verification-code unique-key="page-a"></u-verification-code>

/* B.vue */
<u-verification-code unique-key="page-b"></u-verification-code>
```

## API

## Props

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| seconds | 倒计时所需的秒数  | Number | String | 60 | - |
| start-text | 开始前的提示语，见上方说明  | String | 获取验证码 | - |
| change-text | 倒计时期间的提示语，必须带有字母"x"，见上方说明 | String  | X秒重新获取 | - |
| end-text | 倒计结束的提示语，见上方说明 | String  | 重新获取 | - |
| keep-running | 是否在H5刷新或各端返回再进入时继续倒计时 | Boolean  | false | true |
| unique-key | 多个组件之间继续倒计时的区分`key`，见上方说明 | String  | - | - |

## Methods

需要通过ref获取验证码组件才能调用，见上方"基本使用"说明

| 名称          | 说明            |
|-------------  |---------------- |
| start | 开始倒计时  |
| reset | 结束当前正在进行中的倒计时，设置组件为可以重新获取验证码的状态  |

## Event

|事件名|说明|回调参数|版本|
|:-|:-|:-|:-|
| change | 倒计时期间，每秒触发一次 | text: 当前剩余多少秒的状态，见上方说明 | - |
| start | 开始倒计时触发 | - | - |
| end | 结束倒计时触发 | - | - |

---

---
url: 'https://uviewpro.cn/zh/components/waterfall.md'
---
# Waterfall 瀑布流&#x20;

这是一个瀑布流形式的组件，内容分为左右两列，结合uView的`懒加载`组件效果更佳。\
相较于某些只是奇偶数左右分别，或者没有利用vue作用域插槽的做法，uView Pro的瀑布流实现了真正的
组件化，搭配[LazyLoad 懒加载](/zh/components/lazyLoad.html)和[Loadmore 加载更多](/zh/components/loadMore.html)组件，让您开箱即用，眼前一亮。

:::warning 注意

1. 在微信小程序中，需要hx2.8.11才支持在懒加载中结合其他组件
2. 新增清空列表和移除某条数据的组件方法，原`flow-list`参数，需要改为`v-model`接收传值
3. 由于hx的问题，支付宝小程序需要hx2.8.2版本及以上才支持本组件
   :::

## 平台差异说明

|App|H5|微信小程序|支付宝小程序|百度小程序|头条小程序|QQ小程序|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|√|√|√|√|√|√|√|

## 基本使用

本组件利用了vue的作用域插槽([详见vue文档](https://cn.vuejs.org/v2/guide/components-slots.html#%E4%BD%9C%E7%94%A8%E5%9F%9F%E6%8F%92%E6%A7%BD))特性，
将传入`waterfall`内部的数据，通过`slot`(作用域插槽)让用户能在父组件中引用和配置对应的数据，这样做的
原因是可以让用户自定义列表`item`的结构和样式，达到真正的组件化。

需要注意的是，组件内部导出的数据，需要使用`template`元素接收，同时通过`v-slot`指定左右两列的`slot`，如
`v-slot:left="list"`，这里的`list`变量名为用户自定义的(意味着您可以起名叫`data`都是没问题的)，它为一个对象，它内部分别有`leftList`和`rightList`，用于
渲染左右两列的数据，见如下完整示例：

## 核心代码

```html
<u-waterfall v-model="flowList">
	<template v-slot:left="{leftList}">
		<view v-for="(item, index) in leftList" :key="index">
			<!-- 这里编写您的内容，item为您传递给v-model的数组元素 -->
		</view>
	</template>
	<template v-slot:right="{rightList}">
		<view v-for="(item, index) in rightList" :key="index">
			<!-- 这里编写您的内容，item为您传递给v-model的数组元素 -->
		</view>
	</template>
</u-waterfall>
```

## 移除或清空数据

移除或者清空，都需要通过`ref`调用组件内部的方法。

1. 移除数据

组件内部方法名为`remove`，需要传入"id"值，这个"id"键值的名称配置参数为`idKey`(默认`id`)，如下：

假设您的数据为:

```js
let arr = [
	{idx: 1, name: 'lisa'},
	{idx: 2, name: 'mary'}
]
```

那么您应该配置`idKey`为`idx`。

2. 清空数据

通过`ref`手动调用组件内部的`clear`方法，可以清空左右两列的数据。

说明：具体实现方法，请见下方的示例代码

## 完整应用示例

```html
<template>
	<view class="wrap">
		<u-button @click="clear">清空列表</u-button>
		<u-waterfall v-model="flowList" ref="uWaterfallRef">
			<template v-slot:left="{leftList}">
				<view class="demo-warter" v-for="(item, index) in leftList" :key="index">
					<!-- 警告：微信小程序中需要hx2.8.11版本才支持在template中结合其他组件，比如下方的lazy-load组件 -->
					<u-lazy-load threshold="-450" border-radius="10" :image="item.image" :index="index"></u-lazy-load>
					<view class="demo-title">
						{{item.title}}
					</view>
					<view class="demo-price">
						{{item.price}}元
					</view>
					<view class="demo-tag">
						<view class="demo-tag-owner">
							自营
						</view>
						<view class="demo-tag-text">
							放心购
						</view>
					</view>
					<view class="demo-shop">
						{{item.shop}}
					</view>
					<u-icon name="close-circle-fill" color="#fa3534" size="34" class="u-close" @click="remove(item.id)"></u-icon>
				</view>
			</template>
			<template v-slot:right="{rightList}">
				<view class="demo-warter" v-for="(item, index) in rightList" :key="index">
					<u-lazy-load threshold="-450" border-radius="10" :image="item.image" :index="index"></u-lazy-load>
					<view class="demo-title">
						{{item.title}}
					</view>
					<view class="demo-price">
						{{item.price}}元
					</view>
					<view class="demo-tag">
						<view class="demo-tag-owner">
							自营
						</view>
						<view class="demo-tag-text">
							放心购
						</view>
					</view>
					<view class="demo-shop">
						{{item.shop}}
					</view>
					<u-icon name="close-circle-fill" color="#fa3534" size="34" class="u-close" @click="remove(item.id)"></u-icon>
				</view>
			</template>
		</u-waterfall>
		<u-loadmore bg-color="rgb(240, 240, 240)" :status="loadStatus" @loadmore="addRandomData"></u-loadmore>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'

const loadStatus = ref('loadmore')
const flowList = ref<any[]>([])
const uWaterfallRef = ref()
const list = [
  {
    price: 35,
    title: '北国风光，千里冰封，万里雪飘',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic.sc.chinaz.com/Files/pic/pic9/202002/zzpic23327_s.jpg',
  },
  {
    price: 75,
    title: '望长城内外，惟余莽莽',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic.sc.chinaz.com/Files/pic/pic9/202002/zzpic23325_s.jpg',
  },
  {
    price: 385,
    title: '大河上下，顿失滔滔',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic2.sc.chinaz.com/Files/pic/pic9/202002/hpic2119_s.jpg',
  },
  {
    price: 784,
    title: '欲与天公试比高',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic2.sc.chinaz.com/Files/pic/pic9/202002/zzpic23369_s.jpg',
  },
  {
    price: 7891,
    title: '须晴日，看红装素裹，分外妖娆',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic2.sc.chinaz.com/Files/pic/pic9/202002/hpic2130_s.jpg',
  },
  {
    price: 2341,
    shop: '李白杜甫白居易旗舰店',
    title: '江山如此多娇，引无数英雄竞折腰',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23346_s.jpg',
  },
  {
    price: 661,
    shop: '李白杜甫白居易旗舰店',
    title: '惜秦皇汉武，略输文采',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23344_s.jpg',
  },
  {
    price: 1654,
    title: '唐宗宋祖，稍逊风骚',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23343_s.jpg',
  },
  {
    price: 1678,
    title: '一代天骄，成吉思汗',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23343_s.jpg',
  },
  {
    price: 924,
    title: '只识弯弓射大雕',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23343_s.jpg',
  },
  {
    price: 8243,
    title: '俱往矣，数风流人物，还看今朝',
    shop: '李白杜甫白居易旗舰店',
    image: 'http://pic1.sc.chinaz.com/Files/pic/pic9/202002/zzpic23343_s.jpg',
  },
]

function addRandomData() {
  for(let i = 0; i < 10; i++) {
    let index = uni.$u.random(0, list.length - 1)
    // 先转成字符串再转成对象，避免数组对象引用导致数据混乱
    let item = JSON.parse(JSON.stringify(list[index]))
    item.id = uni.$u.guid()
    flowList.value.push(item)
  }
}

function remove(id: string) {
  uWaterfallRef.value?.remove(id)
}

function clear() {
  uWaterfallRef.value?.clear()
}

onLoad(() => {
  addRandomData()
})

onReachBottom(() => {
  loadStatus.value = 'loading'
  setTimeout(() => {
    addRandomData()
    loadStatus.value = 'loadmore'
  }, 1000)
})
</script>

<style>
	/* page不能写带scope的style标签中，否则无效 */
	page {
		background-color: rgb(240, 240, 240);
	}
</style>

<style lang="scss" scoped>
	.demo-warter {
		border-radius: 8px;
		margin: 5px;
		background-color: #ffffff;
		padding: 8px;
		position: relative;
	}
	
	.u-close {
		position: absolute;
		top: 32rpx;
		right: 32rpx;
	}
	
	.demo-image {
		width: 100%;
		border-radius: 4px;
	}
	
	.demo-title {
		font-size: 30rpx;
		margin-top: 5px;
		color: $u-main-color;
	}
	
	.demo-tag {
		display: flex;
		margin-top: 5px;
	}
	
	.demo-tag-owner {
		background-color: $u-type-error;
		color: #FFFFFF;
		display: flex;
		align-items: center;
		padding: 4rpx 14rpx;
		border-radius: 50rpx;
		font-size: 20rpx;
		line-height: 1;
	}
	
	.demo-tag-text {
		border: 1px solid $u-type-primary;
		color: $u-type-primary;
		margin-left: 10px;
		border-radius: 50rpx;
		line-height: 1;
		padding: 4rpx 14rpx;
		display: flex;
		align-items: center;
		border-radius: 50rpx;
		font-size: 20rpx;
	}
	
	.demo-price {
		font-size: 30rpx;
		color: $u-type-error;
		margin-top: 5px;
	}
	
	.demo-shop {
		font-size: 22rpx;
		color: $u-tips-color;
		margin-top: 5px;
	}
</style>
```

## 注意事项

1. 上方的示例中，结合了uView的[lazyload懒加载](/zh/components/lazyLoad.html)和[loadmore加载更多](/zh/components/loadMore.html)组件，具体用法，请见文档。
2. 需要通过`v-model`传递参数，将数据传递给组件，组件内部将每次新增的数据，通过动态查询左右列的高度
   添加到高度低的一列。
3. 组件有一个`add-time`参数，用于将单条数据添加到队列的时间间隔，因为图片加载是需要时间的，所以瀑布流左右列
   的高度会不定时改变，`add-time`值越大，对程序效果越好，但是对用户来说，越大值可能就是以能感受的速度一个一个添加
   到队列尾部的，所以这是一个双面性的结果。
4. 由于图片加载完成的时机是不确定的，导致图片加载完成时，队列的高度会发生改变，而且这个时机是无法确定的，
   所以每次添加数据的时候，单次请求的所有数据中最后一个数据不一定能准确添加高度更低的队列一侧，但是可以保证下一次请求数据的第一条
   能准确添加到队列高度低的一侧。

## API

## IndexBar Props

注意：通过`v-model`双向绑定传递参数，因为组件内部需要修改父组件的值。

| 参数          | 说明            | 类型            | 默认值             |  可选值   |
|-------------  |---------------- |---------------|------------------ |-------- |
| add-time | 单条数据添加到队列的时间间隔，单位ms，见上方注意事项说明  | String | Number | 200 | - |
| idKey | 数据的唯一值的键名，见上方说明  | String | id | - |

## Methods

这些为组件内部的方法，需要通过`ref`调用

| 参数          | 说明            |
|-------------  |---------------- |
| clear | 清空列表数据 |
| remove(id) | `id`为唯一的"id"值，见上方说明  |

---

---
url: 'https://uviewpro.cn/zh/components/downloadSetting.md'
---
# 下载安装方式配置

## 关于 SCSS

## 关于 SCSS

uView Pro 依赖 SCSS，您必须要安装此插件，否则无法正常运行。

* 如果您的项目是由`HBuilder X`创建的，相信已经安装 scss 插件，如果没有，请在 HX 菜单的 工具->插件安装中找到"scss/sass 编译"插件进行安装，
  如不生效，重启 HX 即可
* 如果您的项目是由 vue-cli 创建的，请通过以下命令安装对 sass(scss)的支持，如果已安装，请略过。

```bash
# 安装sass
npm i sass -D

# 安装sass-loader
npm i sass-loader -D
```

:::tip 注意
sass、sass-loader 版本过高或过低，导致编译异常，因此推荐统一并锁定依赖版本：

```json
"sass": "1.63.2",
"sass-loader": "10.4.1"
```

:::

## 准备工作

在进行配置之前，请确保您已经根据[安装](install.html)中的步骤对 uView Pro 进行了下载安装，如果没有，请先下载安装。

## 1. 引入 uView Pro 主库

在 `main.ts` 中引入并注册 uView Pro：

```js
// main.ts
import { createSSRApp } from 'vue'
// uni_modules 方式
import uViewPro from '@/uni_modules/uview-pro'

export function createApp() {
  const app = createSSRApp(App)
  app.use(uViewPro)
  return {
    app
  }
}
```

## 2. 引入全局样式

在 `uni.scss` 中引入主题样式：

```scss
// uni_modules 方式
@import '@/uni_modules/uview-pro/theme.scss';
```

在 `App.vue` 首行引入基础样式：

```scss
<style lang="scss">
  // uni_modules 方式
  @import "@/uni_modules/uview-pro/index.scss";
</style>
```

## 3. 配置自动引入组件

### 基于 easycom 配置自动引入组件方案 1

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
      // uni_modules 方式
      "^u-(.*)": "@/uni_modules/uview-pro/components/u-$1/u-$1.vue"
    }
  },
  "pages": [
    // ...
  ]
}
```

:::tip 注意

* 1.修改 `easycom` 规则后需重启 HX 或重新编译项目。
* 2.请确保 `pages.json` 中只有一个 easycom 字段，否则请自行合并多个规则。
* 3.一定要放在 `custom` 内，否则无效。
  :::

### 基于 vite 配置自动引入组件方案 2

如果不熟悉 `easycom`，也可以通过 [@uni-helper/vite-plugin-uni-components](https://github.com/uni-helper/vite-plugin-uni-components) 实现组件的自动引入。

:::tip 提醒

* 推荐使用 `@uni-helper/vite-plugin-uni-components@0.2.1` 及以上版本，因为在 0.2.1 版本开始其内置了 `uView Pro` 的`resolver`。
* 如果使用此方案时控制台打印很多 `Sourcemap for  points to missing source files​` ，可以尝试将 `Vite` 版本升级至 `4.5.x` 以上版本。

:::

::: code-group

```bash [npm]
npm i @uni-helper/vite-plugin-uni-components -D
```

```bash [yarn]
yarn add @uni-helper/vite-plugin-uni-components -D
```

```bash [pnpm]
pnpm add @uni-helper/vite-plugin-uni-components -D
```

:::

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

import Components from '@uni-helper/vite-plugin-uni-components'
import { uViewProResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'

export default defineConfig({
  plugins: [
    // make sure put it before `Uni()`
    Components({
      resolvers: [uViewProResolver()]
    }),
    uni()
  ]
})
```

如果你使用 `pnpm` ，请在根目录下创建一个 `.npmrc` 文件，参见 [Issue](https://github.com/antfu/unplugin-vue-components/issues/389)。

```text
// .npmrc
public-hoist-pattern[]=@vue*
// or
// shamefully-hoist = true
```

## 4. Volar 类型提示支持

如需在 CLI 项目中获得 Volar 的全局类型提示，请在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    // uni_modules 方式
    "types": ["@/uni_modules/uview-pro/types"]
  }
}
```

> HBuilderX 项目暂不支持 tsconfig.json 的 types 配置，CLI 项目推荐配置以获得最佳 TS 体验。

## 5. 组件使用

配置完成后，无需 import 和 components 注册，可直接在 SFC 中使用 uView Pro 组件：

```vue
<template>
  <u-button type="primary">按钮</u-button>
</template>
```

---

---
url: 'https://uviewpro.cn/zh/components/chatGroup.md'
---
# 交流反馈

### 点击群号跳转 QQ 窗口：[群号：811732166](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027\&k=98nSVDldWEbDdq4lxiP4aL7uATfMSlI6\&authKey=G2yQJ5MQiKzMldaxBsIfKt17NuJuUw8Fr6zdKLggc6NZXgw4BVbqkU2U3EE994yd\&noverify=0\&group_code=811732166)

---

---
url: 'https://uviewpro.cn/zh/resource/about.md'
---
# 交流反馈

uView Pro 采用[MIT](https://baike.baidu.com/item/MIT/10772952)许可证的开源项目，使用完全免费。欢迎加 QQ 群交流反馈，一起学习，共同进步。

## 作者

我当前是一名前端开发工程师，热衷于利用新技术和工具创造优质的产品体验。对开源充满热情，并经常维护和贡献一些项目。同时也喜欢通过撰写技术博客来分享我的知识和经验，希望能帮助到更多的人。

我经常在以下平台进行创作：

* 掘金：[点击链接直达掘金>>>](https://juejin.cn/user/4230576472589976/posts)
* CSDN：[点击链接直达CSDN>>>](https://blog.csdn.net/qq_24956515?type=blog)
* 微信公众号：[点击链接直达微信公众号>>>](https://mp.weixin.qq.com/s/kHQ9Db0QUvpxDh1nhJEP2g)

## 研发组

uView Pro 的理念是"挣脱束缚，向往自由"，目标是做 uni-app 生态的标杆，推动 uni-app 生态和互联网的发展。\
uView Pro 免费开源，无需授权，欢迎商用。uView Pro 的发展希望得到各个小伙伴的支持，我们一起为构建一个更加优秀的 UI 框架而努力。

## 文档

uView Pro 的文档，力求不留死角，把所有可能需要注意的地方，都详细列出。uView Pro 的文档经得起推敲，受得住考验。

## 展望未来

uView Pro 的目标是做成 uniapp Vue3 生态的标杆，自由且免费开源。\
对此，uView Pro 有清晰且明确的计划安排，uView Pro 将会全面兼容 Vue3 TypeScript，适配暗黑模式，整合 unicloud，加入更多组件和模板等。\
但是，一个人的力量是不够的：

1. **为了开源，理想和自由**，您可以加入 uView Pro 的研发工作组，我们一起并肩奋战。
2. 如果您是个积极活跃的人，那么也欢迎您加入 uView Pro 的 QQ 群或微信群成为管理员。

所有加入 uView Pro 贡献的同学，都会在官网声明，并且有自己的个人专属页。

请加作者 微信(注明加入 uView Pro 开发组)：anyupxing

## 赞助商

uView 官方拥有众多用户，且文档详尽，经得起推敲，受得住考验，官方网站每天有超过 1 万 IP 访问量，如果您认为这些有助于您公司的业务推广，可以成为 uView Pro的赞助商，
我们会在适当的位置展示您的推广内容。

赞助请联系 微信(注明赞助)：anyupxing

## 捐赠

---

---
url: 'https://uviewpro.cn/zh/guide/intro.md'
---
# 介绍

## uView Pro 的由来

uView Pro 是在 uView 1.8.8 官方组件库基础上，采用 Vue3 全新语法彻底重构的 uni-app 生态框架。不同于市面上的其他 uView 框架等兼容 Vue3 的方案，uView Pro 并非简单兼容，而是对每一个组件和工具进行源码级重构，充分发挥 Vue3 的响应式和组合式优势，API 设计更现代，性能更优越。

uView Pro 继承了 uView 1.x 简洁高效的设计理念，并在此基础上全面升级，支持更丰富的业务场景和更灵活的扩展能力。

## 多平台支持

uView Pro 已覆盖 Android、iOS、鸿蒙以及微信/头条/支付宝等主流小程序平台，真正实现“一套代码，多端运行”，并通过统一的适配层屏蔽平台差异，让开发者专注业务而非兼容问题。

同时内置主题系统、暗黑模式与国际化（i18n）支持，便于快速切换视觉风格与语言，满足不同项目与多场景的需求。

## 框架优势

* 🚀 **彻底重构**：基于 Vue3 语法和特性，源码级重构所有组件和工具，非兼容层方案。
* ⚡ **高性能**：充分利用 Vue3 响应式和组合式 API，组件性能和可维护性大幅提升。
* 🖥️ **多端适配**：支持 Android、iOS、微信小程序，持续兼容更多平台。
* 🌍 **国际化（i18n）支持**：内置多语言切换，便于多语言项目快速集成与部署。
* ✨ **易用性强**：API 设计现代，文档详尽，开发体验优于传统兼容方案。
* 🌐 **生态完善**：内置 80+ 高质量组件和丰富工具库，覆盖主流业务场景。
* 🎨 **多主题定制**：通过主题生成工具三分钟实现多套主题定制。
* 🌙 **暗黑模式**：支持一键暗黑模式。

::: tip uView Pro 的目标是做成 uniapp Vue3 生态的标杆，自由且免费开源。
uView Pro 相关开源地址如下：

> * GitHub：<https://github.com/anyup/uview-pro>
> * Gitee：<https://gitee.com/anyup/uview-pro>
> * Npm：<https://www.npmjs.com/package/uview-pro>
> * 插件市场：<https://ext.dcloud.net.cn/plugin?id=24633>
> * 官网：<https://uviewpro.cn/>
>   :::

## 与其它框架的区别

uView Pro 与 uview-plus、uv-ui 等框架的最大区别在于：

* 其它框架多为在原有 Vue2 组件基础上做兼容层，部分 API 或特性无法充分发挥 Vue3 优势。
* uView Pro 则是基于 Vue3 彻底重构，所有组件和工具均为原生 Vue3 实现，性能和体验更优。

## 版权信息

uView Pro 遵循 [MIT](https://baike.baidu.com/item/MIT/10772952) 开源协议，您可免费用于任何合法项目。

注意：禁止用于非法领域（如赌博、暴力等），如因此产生纠纷，uView Pro 不承担任何责任。

## 鸣谢

再次感谢 `uView UI` 官方开发团队，感谢所有为 `uView UI` 的贡献者，以及所有为 `uView Pro` 的贡献者。

* [uView Pro Github](https://github.com/anyup/uview-pro)
* [uView Pro Gitee](https://gitee.com/anyup/uview-pro)
* [uView UI 1.0](https://github.com/umicro/uView)
* [uView UI 2.0](https://github.com/umicro/uView2.0)

## 捐赠

---

---
url: 'https://uviewpro.cn/zh/layout/intro.md'
---
# 介绍




布局为uView Pro框架的一部分，是uView Pro平时积累的常见页面布局，可能是页面的一部分，可也能是整个
页面，主要功能不是逻辑的交互，而是样式的实现，所以我们把它们收集成一个板块，而不是当成组件呈现。

需要使用这些布局的用户，可以直接复制到需要的页面，修改相关的结构，逻辑或者样式即可。

:::warning 注意
这些布局都依赖uView Pro框架，请确保在使用uView Pro的情况下使用相关的功能，否则，需要自行调试修改。
:::

---

---
url: 'https://uviewpro.cn/zh/tools/intro.md'
---
# 介绍

此函数方法，为 `uView Pro` 框架提供的一部分功能，它的实现，需要通过 `function` 调用，而不是组件的形式。
工具库中的所有方法，均挂载在`$u`对象下，调用方法如下：

* 如果是在 `script` 中，需要通过`uni.$u.xxx`形式调用，如调用去除空格的`trim`方法：

```js
console.log(uni.$u.trim(' abc '));	// 去除两端空格
```

或导入 `$u` 工具函数库，调用方法如下：

```js
import { $u } from 'uview-pro'

console.log($u.trim(' abc '));	// 去除两端空格
```

* 如果是在元素中，也需要导入，如：

```html
<template>
	<view>
		去除所有空格：{{$u.trim(str, 'all')}}
	</view>
</template>

<script setup lang="ts">
	import { $u } from 'uview-pro'
</script>
```

---

---
url: 'https://uviewpro.cn/zh/layout/coupon.md'
---
# 优惠券




此部件为一些常见优惠券样式，大家可以根据自己的需求，修改布局的结构，样式等。

---

---
url: 'https://uviewpro.cn/zh/tools/fastUse.md'
---
# 便捷工具

此专题内容为一些方便用户快速，便捷使用的小工具，可能是uView的一些方法的简易版，或者对uni的一些方法进行二次封装，方便用户
快速使用。

### toast(title, duration = 1500)

* `title` \<String> toast的消息内容
* `duration` \<Number> toast出现到消失的时间，单位ms，默认1500ms

此方法为uniapp的`uni.showToast`的二次封装，方便用户使用，参数只能配置`title`和`duration`

```js
uni.$u.toast('Hello uView!');
```

### os()

此属性用于返回平台的名称，为小写的`ios`或`android`

**注意：** 以方法形式调用

```js
console.log(uni.$u.os())
```

### sys()

此属性用于获取设备的信息，相当于uni.getSystemInfoSync()的效果

**注意：** 以方法形式调用，因为属性方式调用，结果可能会不准确

```js
console.log(uni.$u.sys())
```

---

---
url: 'https://uviewpro.cn/zh/components/common.md'
---
# 内置样式

## 说明

uView Pro 组件功能的实现，并不依赖全局样式，内置的一些类名，只是提供一些基础且常用的样式，仅此而已。\
注意：请根据[快速上手](/zh/components/quickstart.html)中的说明，引入 uView Pro 提供的 scss 文件。

:::warning 温馨提示
由于 uView Pro 的内置样式均是写在 scss 文件中的，您在使用的时候，请确保要给页面的`style`标签加上`lang="scss"`属性，否则可能会报错。

:::

## 文字省略

`u-line-1`,`u-line-2`,`u-line-3`,`u-line-4`,`u-line-5`五个类名在文字超出内容盒子时，分别只显示一行、两行、三行、四行、五行+省略号。

```html
<view class="u-line-1">
  是日也，天朗气清，惠风和畅，仰观宇宙之大，俯察品类之盛，所以游目骋怀，足以极视听之娱，信可乐也
</view>
```

## 定位

uView Pro 内置了关于相对和绝对定位的两个类，分别为`u-relative`(`u-rela`)和`u-absolute`(`u-abso`)：

```css
.u-relative,
.u-rela {
  position: relative;
}

.u-absolute,
.u-abso {
  position: absolute;
}
```

## 字体大小

### **1. 数值形式**

uView Pro 为了方便用户写字体，通过 SCSS 生成了一套样式类，专门用于定位字体的大小。对于字体，不同用户可能有喜欢`px`，也有喜欢`rpx`单位的，
一般来说，在 uni-app 上，`rpx`单位最终表现出来的大小数值为`px`的两倍左右，也就是说，`24rpx`和`12px`的字体大小是差不多的。\
uView Pro 为此提供了一个类`u-font-x`，这个`x`为 10-40 之间(包含 10 和 40)，当`x >= 10 && x < 20`时，表现为`px`性质，当`x >= 20 && x <= 40`时，表现为`rpx`性质。

用法如下：

* 当`x >= 10 && x < 20`时，表现为`px`性质

```html
<view class="u-font-13"></view>
```

这个`.u-font-13`在 uView 的内部样式定义为：

```css
.u-font-13 {
  font-size: 13px;
}
```

* 当`x >= 20 && x <= 40`时，表现为`rpx`性质

```html
<view class="u-font-26"></view>
```

这个`.u-font-26`在 uView Pro 的内部样式定义为：

```css
.u-font-26 {
  font-size: 26rpx;
}
```

### **2. 断点形式**

为了更加形象和方便记忆，uView 另外提供了一套断点的字体大小，分别以`xs`、`sm`、`md`、`lg`、`xl`作为后缀，如下：

```css
.u-font-xs {
  font-size: 22rpx;
}

.u-font-sm {
  font-size: 26rpx;
}

.u-font-md {
  font-size: 28rpx;
}

.u-font-lg {
  font-size: 30rpx;
}

.u-font-xl {
  font-size: 34rpx;
}
```

## 文字对齐

uView Pro 为文字对齐定义了 3 个类，分别如下：

```css
/* 文字左对齐 */
.u-text-left {
  text-align: left;
}

/* 文字居中对齐 */
.u-text-center {
  text-align: center;
}

/* 文字右对齐 */
.u-text-right {
  text-align: right;
}
```

## 重置按钮样式

我们知道，uni-app 和微信小程序的`button`按钮是自带样式的，比如边框，内边距，行高等。在某些特殊场景，我们可能会需要清除这些样式，仅仅只留下按钮文本，就像
单纯的`view`元素一样，不带预置样式，场景：\
在微信小程序中，我们知道`button`设置`open-type`参数为`getUserInfo`(或者分享场景)，点击按钮可以弹出让用户授权的系统弹窗，有时候我们可能需要按钮形式展现，但也有时候我们仅仅需要
"点击登录/授权/分享"几个字，同时具备获取相应的功能，就需要清除按钮的样式了，只需要给`button`加上`u-reset-button`类名即可。

```html
<button class="u-reset-button">点击登录</button>
```

提示：

1. 此种场景，不建议使用 uView Pro 的`u-button`组件，使用原生的`button`即可
2. 有时候，我们可能弹出询问用户是否想授权，可以用`u-modal`组件，此组件有一个`confirm-button`的`slot`用于替换`确定`按钮，用户点击确定，即可授权。

````html
/* 请在微信开发工具中运行此代码 */ ```vue
<template>
  <view>
    <u-modal v-model="show" content="点击确定进行授权">
      <template #confirm-button>
        <button
          open-type="getUserInfo"
          class="u-reset-button"
          @getuserinfo="getUserInfo"
        >
          确定
        </button>
      </template>
    </u-modal>
    <u-button @click="show = true">打开modal</u-button>
  </view>
</template>

<script setup lang="ts">
  import { ref } from "vue";

  const show = ref(true);

  function getUserInfo(res: any) {
    console.log(res);
  }
</script>
````

## 内外边距

uView 定义了一套内外边距的类名，调用简单，方便用户使用，类似`u-padding-x`、`u-margin-left-x`等，这里的`x`取值规则如下：

* 1-80(可以等于 80)之间的偶数(双数)
* 能被 5 除尽的 1-80 之间的数，如 5，10，15，35 等

类名的取值有如下：

**注意：** uView 同时也给了一套简写的方法，二者是等价的。

* u-padding-x == u-p-x
* u-padding-left-x == u-p-l-x
* u-padding-top-x == u-p-t-x
* u-padding-right-x == u-p-r-x
* u-padding-bottom-x == u-p-b-x
* u-margin-x == u-m-x
* u-margin-left-x == u-m-l-x
* u-margin-top-x == u-m-t-x
* u-margin-right-x == u-m-r-x
* u-margin-bottom-x == u-m-b-x

如果我们想定义`26rpx`的**左外边距**：

```html
<view class="u-margin-left-26"></view>
```

这个`.u-margin-left-26`在 uView 的内部样式定义为：

```css
.u-margin-left-26 {
  margin-left: 26rpx;
}
```

如果我们想要`35rpx`的内边距：

```html
<view class="u-padding-35"></view>
```

这个`.u-padding-35`在 uView 的内部样式定义为：

```css
.u-padding-35 {
  padding: 35rpx;
}
```

## flex 布局

在看这个部分的时候，请确保您对`flex`是了解的，否则可以参考[阮一峰的 flex 教程](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)\
由于我们经常要使用`flex`布局，而其中的大部分样式又都是重复的，总是少不了如下的几句：

```css
/* 父盒子 */
display: flex;
flex-wrap: wrap;
flex-direction: row;
align-items: center;

/* 子元素 */
flex: 1;
```

基于以上，uView 定义了一个最常用的总集合类，名为`u-flex`，其内部值如下：

### **1. 总超集**

```css
.u-flex {
  display: flex;
  flex-direction: row;
  align-items: center;
}
```

### **2. 子元素是否换行**

```css
/* 换行 */
.u-flex-wrap {
  flex-wrap: wrap;
}

/* 不换行 */
.u-flex-nowrap {
  flex-wrap: nowrap;
}
```

:::tip 提示
当我们写这些跟`flex`相关的类名时，总应该把`u-flex`写在`class`多个类名的左边，因为`u-flex`是一个集合类，如果你不想要其中的某个属性，如`align-items: center`
，可以通过右边的类名覆盖它。
:::

覆盖`u-flex`中的`align-items: center`(对齐)，改为顶部对齐`u-col-top`：

```html
<view class="u-flex u-col-top"> ...... </view>
```

最终内部表现如下(其它以此类推)：

```css
.u-flex {
  display: flex;
  flex-direction: row;
  align-items: center;
}

/* 由于align-items: flex-start在后面，故覆盖了"u-flex"的align-items: center */
.u-col-top {
  align-items: flex-start;
}
```

### **3. 子元素在上下左右的对齐方式**

这里类名的命名依据为，`col`为`column`(列，竖向)的缩写，`row`为行的意思(横向)，所以就有垂直方向上的诸如`u-col-center`表
垂直居中对齐，`u-row-left`代表水平左对齐。\
此类名控制的是子元素，是需要写在父元素盒子上的：

```css
/* 垂直居中 */
.u-col-center {
  align-items: center;
}

/* 顶部对齐 */
.u-col-top {
  align-items: flex-start;
}

/* 底部对齐 */
.u-col-bottom {
  align-items: flex-end;
}

/* 左边对齐 */
.u-row-left {
  justify-content: flex-start;
}

/* 水平居中 */
.u-row-center {
  justify-content: center;
}

/* 右边对齐 */
.u-row-right {
  justify-content: flex-end;
}

/* 水平两端对齐，项目之间的间隔都相等 */
.u-row-between {
  justify-content: space-between;
}

/* 水平每个项目两侧的间隔相等，所以项目之间的间隔比项目与父元素两边的间隔大一倍 */
.u-row-around {
  justify-content: space-around;
}
```

### **4. 子元素空间分布**

此类名是写在子元素的`class`中的，主要用于决定子元素占据的父元素的空间大小，类名为`u-flex-x`，`x`的取值为`x >= 1 && x <= 12`：

```css
.u-flex-1 {
  flex: 1;
}

.u-flex-2 {
  flex: 2;
}

.u-flex-3 {
  flex: 3;
}

/* ...... */

.u-flex-12 {
  flex: 12;
}
```

## 边框

uni-app，iOS 和少数设备使用`1rpx`是能够得到类似`0.5px`的半像素宽度的，但是某些情况下是不兼容的，
故 uView 提供了一套兼容的 css 类名，方便用户使用。\
`u-border`表示给元素添加四周的边框，`u-border-top`为上边框，`u-border-right`为右边框，
`u-border-bottom`为下边框，`u-border-left`为左边框。\
说明：如果想调整边框与内容的距离，修改元素的内边距即可。

```html
<view class="u-border-bottom">
  夫人之相与，俯仰一世，或取诸怀抱，悟言一室之内；或因寄所托，放浪形骸之外
</view>
```

## 文字颜色

uView 提供了四个关于文字的颜色，具体详见文档的[Color 色彩](/zh/components/color.html)部分，分别是：

* `main-color`主要颜色，可以用于标题等需要重颜色的场景
* `content-color`内容颜色，可以用于一般性内容的场景
* `tips-color`提示颜色，可以用于浅颜色的提示语的场景
* `light-color`为比`tips-color`更浅的颜色，可以和`tips-color`搭配使用

举个例子：\
我们平时看到的 APP 的新闻列表，标题颜色可以用`$u-main-color`，简介部分颜色可以用`$u-content-color`，底部的发布时间文字等可以用`$u-tips-color`。

### **1. 类名方案**

这个方案，直接通过类名调用，有这几个对应类名：`u-main-color`、`u-content-color`、`u-tips-color`、`u-light-color`。

```html
<view class="u-main-color"> ...... </view>
```

### **2. SCSS 变量名方案**

uView 提供了四个关于文字颜色的 scss 变量名，具体详见文档的[Color 色彩](/zh/components/color.html)部分，分别是：

* `$u-main-color`
* `$u-content-color`
* `$u-tips-color`
* `$u-light-color`

```html
<!-- 请确保在style标签声明了"lang="scss"" -->
<style lang="scss" scoped>
  .box {
    color: $u-main-color;
  }

  .count {
    border-color: $u-light-color;
  }
</style>
```

## 主题色

uView 提供五个关于主题的 scss 颜色变量，如有需要，可合理使用。具体详见文档的[Color 色彩](/zh/components/color.html)部分，分别是：

* `$u-type-primary`为蓝色，uView 的主色彩，代表热情，友好，积极，向上之意。
* `$u-type-warning`为黄色，代表警告之意。
* `$u-type-success`为绿色，代表成功之意。
* `$u-type-error`为红色，代表错误之意。
* `$u-type-info`为灰色，代表一般信息之意。

```html
<style lang="scss" scoped>
  .item {
    color: $u-type-primary;
  }
</style>
```

---

---
url: 'https://uviewpro.cn/zh/components/upgrade/04x.md'
---
# 升级指南

0.4.1 版本开始，uView Pro 引入了多主题系统、暗黑模式和改进的主题配置工具。本指南帮助你从 0.3.x 升级到 0.4.x。

## 概述

| 功能 | 0.3.x | 0.4.x |
|------|-------|-------|
| 主题配置 | 单主题，手动编辑变量 | 多主题，可视化智能配置工具 |
| 暗黑模式 | 不支持 | 原生支持，自动/手动切换 |
| 色值生成 | 手动管理 | 智能生成暗黑色值 |
| 导出格式 | SCSS + TS 变量 | SCSS + TS 数组 |
| 配置工具 | [旧版配置工具](/zh/guide/theme.html) | [新版配置工具](/zh/guide/themeGenerate.html) |

## 核心变更

### 1. 主题配置方式

**0.3.x**：直接修改 SCSS 变量文件

```scss
// old-theme.scss
$u-type-primary: #2979ff;
$u-type-success: #19be6b;
// ... 手动配置每一个变量
```

**0.4.x**：使用【[主题配置工具](/zh/guide/themeGenerate.html)】生成主题文件

* 打开工具页面，填写颜色和元信息
* 支持可视化色值选择，即时预览效果
* 可配置单个或多个主题
* 导出为 `uview-pro.theme.ts`（推荐）或 SCSS

### 2. 主题文件结构

**0.3.x**：

```scss
$u-type-primary: #2979ff;
$u-type-primary-dark: #2b85e4;
// 所有色值都是静态定义
```

**0.4.x**：

```ts
// src/uview-pro.theme.ts
export default [
  {
    name: 'default',
    label: '默认主题',
    description: '清爽蓝色主题',
    color: {
      primary: '#2979ff',
      success: '#19be6b',
      error: '#fa3534',
      warning: '#ff9900',
      info: '#909399',
      mainColor: '#303133',
      contentColor: '#606266',
      tipsColor: '#909399',
      lightColor: '#c0c4cc',
      borderColor: '#e4e7ed',
      dividerColor: '#e4e7ed',
      bgColor: '#f3f4f6',
      bgWhite: '#ffffff',
      bgGrayLight: '#f1f1f1',
      bgGrayDark: '#2f343c',
      bgBlack: '#000000',
      maskColor: 'rgba(0, 0, 0, 0.4)',
      shadowColor: 'rgba(0, 0, 0, 0.1)'
    },
    darkColor: {
      // 暗黑色值（可选，未填的会由系统智能生成）
      primary: '#5b9ff5'
      // ... 其他可选的暗黑色覆盖
    }
  },
  // 可以包含多个主题...
];
```

### 3. 注册方式变更

**0.3.x**：在 SCSS 中直接导入变量文件

```scss
@import 'path/to/old-theme.scss';
```

**0.4.x**：

1. **在 `unis.scss` 中导入基础主题系统**
   ```scss
   @import 'uview-pro/theme.scss';
   ```

2. **在 `main.ts` 中注册主题**
   ```ts
   import { createSSRApp } from 'vue';
   import App from './App.vue';
   import theme from '@/uview-pro.theme';  // 导入自定义主题
   import uViewPro from '@/uni_modules/uview-pro';

   export function createApp() {
     const app = createSSRApp(App);
     app.use(uViewPro, { theme });  // 传入自定义主题列表
     return { app };
   }
   ```

### 4. 暗黑模式支持

**0.3.x**：无原生支持

**0.4.x**：

* **自动跟随系统**：设置 `darkMode: 'auto'`
* **手动切换**：`setDarkMode('light' | 'dark' | 'auto')`
* **快速切换**：`toggleDarkMode()` 在 light/dark 间切换
* **检查状态**：`isInDarkMode()` 返回布尔值

### 5. 智能暗黑色生成

**0.4.x** 的核心创新：

* 你只需提供**亮色色板** (`color`)，系统自动为缺失的 `darkColor` 生成合理的暗色值
* 如果你需要手动调整某个暗色，只在 `darkColor` 中填写该项，其余仍由系统生成
* 生成算法基于色值混合，确保暗黑模式下的可读性和美观性

例如：

```ts
{
  color: {
    primary: '#2979ff',
    bgColor: '#f3f4f6',
    // ... 其他亮色
  },
  darkColor: {
    // 留空，系统自动生成以下内容：
    // primary: '#5b9ff5'（基于 #2979ff 混合生成的暗色）
    // bgColor: '#1a1a1a'（基于 #f3f4f6 反转生成）
    
    // 如果你想手动覆盖某个暗色：
    primary: '#6ba1ff',  // 自定义的暗色 primary
    // bgColor 仍会由系统生成
  }
}
```

## 升级步骤

### 第 1 步：生成新主题文件

1. 访问【[主题配置工具](/zh/guide/themeGenerate.html)】
2. 配置你的主题色和其他色值（可参考 0.3.x 的旧值作为起点）
3. 打开"启用暗黑色值"并检查生成的暗色是否满意（可逐项调整）
4. 点击"下载主题文件(TS 格式导出)"，得到 `uview-pro.theme.ts`
5. 将文件复制到项目的 `src/uview-pro.theme.ts`

### 第 2 步：更新主题注册代码

编辑 `main.ts` 或你的应用入口文件：

```ts
// Before (0.3.x)
import uViewPro from '@/uni_modules/uview-pro';
app.use(uViewPro);

// After (0.4.x)
import theme from '@/uview-pro.theme';
import uViewPro from '@/uni_modules/uview-pro';
app.use(uViewPro, { theme });
```

### 第 3 步：更新 SCSS 导入

在 `unis.scss` 中：

```scss
// Before (0.3.x)
// @import 'path/to/your-old-theme.scss';

// After (0.4.x)
@import 'uview-pro/theme.scss';  // 导入系统主题基础
// 自定义的色值会通过 main.ts 的 theme 选项注入，无需再导入
```

### 第 4 步：配置多主题/暗黑模式支持

如果你的项目需要暗黑模式，在全局根组件（如 `App.vue`）中包裹 `u-config-provider`：

```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
import { computed } from 'vue';

const { darkMode, themes, currentTheme } = useTheme();

const themeName = computed(() => currentTheme.value?.name);
</script>

<template>
  <u-config-provider :dark-mode="darkMode" :current-theme="themeName" :themes="themes">
    <!-- 你的应用内容 -->
    <KuRootView />
  </u-config-provider>
</template>
```

## 样式使用变更

### SCSS/CSS 中使用

变量命名规则保持一致（兼容 0.3.x）：

```scss
.title {
  color: $u-type-primary;  // 主题色
}
.card {
  background-color: $u-bg-white;  // 背景色
  border-color: $u-border-color;  // 边框色
}
```

### Vue 模板或 JS 中使用

**0.3.x**（无原生支持）：

```js
// 需要手动管理颜色值
const primaryColor = '#2979ff';
```

**0.4.x**（推荐方式）：

```ts
import { $u } from 'uview-pro';

// 方式 1：直接取值
const color = $u.color.primary;

// 方式 2：使用 useTheme
import { useTheme } from 'uview-pro';
const { cssVars } = useTheme();
// cssVars 包含所有当前主题的 CSS 变量，会自动响应主题/暗黑切换
```

行内样式示例：

```vue
<template>
  <!-- 使用 CSS 变量（推荐，自动响应切换） -->
  <view :style="{ color: 'var(--u-type-primary)' }">文本</view>
  
  <!-- 使用 $u.color（需要监听响应） -->
  <view :style="{ color: $u.color.primary }">文本</view>
</template>
```

## 多主题管理

**0.4.x** 新增多主题支持：

```ts
// src/uview-pro.theme.ts
export default [
  {
    name: 'blue',
    label: '蓝色主题',
    color: { primary: '#2979ff', /* ... */ },
    darkColor: { /* ... */ }
  },
  {
    name: 'purple',
    label: '紫色主题',
    color: { primary: '#7c3aed', /* ... */ },
    darkColor: { /* ... */ }
  },
  // 更多主题...
];
```

在应用中切换主题：

```ts
import { useTheme } from 'uview-pro';
const { setTheme, themes } = useTheme();

// 显示所有可用主题并支持切换
themes.value.forEach(t => {
  console.log(t.name, t.label);
});

// 切换到指定主题
setTheme('purple');
```

## 常见问题

**Q: 0.3.x 的 SCSS 文件能继续用吗？**\
A: 不建议混用。建议完全迁移到新的主题系统，使用【主题配置工具】生成统一的 `uview-pro.theme.ts`。
B: 0.3.x 的 SCSS 文件仍然可用，但必须要迁移到新的主题系统。

**Q: 我只想用亮色，不需要暗黑模式？**\
A: 可以。只需提供 `color` 字段，不填 `darkColor` 即可；或设置 `darkMode: 'light'` 固定禁用暗黑。

**Q: 如何在运行时动态加载主题？**\
A: 调用 `useTheme().initTheme(customThemeList)` 在运行时初始化或更新主题列表。

**Q: 暗黑色是如何生成的？**\
A: 系统采用色值混合算法，将亮色与预定义的暗色基准混合（ratio=0.6），生成视觉层级合理的暗色。你可以在配置工具中手动调整任何暗色值。

**Q: CSS 变量名有变化吗？**\
A: 无。仍使用 `$u-type-primary`、`$u-bg-color` 等，保持向后兼容。新增了 CSS 变量形式（`--u-type-primary` 等）供 JS 读取。

## 总结

| 步骤 | 说明 |
|------|------|
| 1️⃣ 使用工具 | 访问主题配置工具，配置新主题并导出 `uview-pro.theme.ts` |
| 2️⃣ 更新注册 | 修改 `main.ts`，传入自定义主题 |
| 3️⃣ 更新导入 | 在 `unis.scss` 导入 `uview-pro/theme.scss` |
| 4️⃣ 可选配置 | 若需要暗黑模式，在主题生成工具中启用暗黑色值 |
| 5️⃣ 测试验证 | 确保色值正确应用，暗黑切换正常工作 |

升级完成后，你将获得：

* ✅ 更灵活的多主题支持
* ✅ 开箱即用的暗黑模式
* ✅ 自动化的色值生成和管理
* ✅ 可视化的主题配置体验

有任何问题，请参考【[多主题与暗黑模式完整指南](/zh/guide/customTheme.html)】。

---

---
url: 'https://uviewpro.cn/zh/guide/i18n.md'
---
# 国际化（i18n）支持 &#x20;

uView Pro 所有内置组件均支持多语言，支持全局与组件级配置、响应式切换与持久化语言偏好。

**核心特性**

* **内置语言**: 默认包含 `zh-CN` 与 `en-US`。
* **配置灵活**: 支持在应用入口全局配置或组件内覆盖局部语言包。
* **响应式切换**: 切换语言时组件文案自动更新。
* **持久化**: 用户选择会被保存以便下次恢复。
* **扩展友好**: 可按需添加或覆盖语言包，支持按需加载。

:::warning 特别注意

组件库发布到 npm 的是未编译的 Vue 和 TypeScript 代码。由于 Vite 会预构建依赖到 `node_modules/.vite`，而国际化基于 `reactive` 实现数据共享，开发阶段可能导致页面使用预构建产物中的数据，而组件库使用内部数据，造成数据不同步。

非 `uni_modules` 模式下，需在 `vite.config.ts` 中添加配置排除预构建：

```ts
import { defineConfig } from 'vite'

export default defineConfig({
    ...
    optimizeDeps: {
        exclude: process.env.UNI_PLATFORM === 'h5' && process.env.NODE_ENV === 'development' ? ['uview-pro'] : []
    }
    ...
})
```

`uni_modules` 模式无需额外处理。

:::

## 快速上手

方式一：全局注册（main.ts）：

```ts
app.use(uViewPro, { locale: 'zh-CN' })

// 或
import { zhCN, enUS } from 'uview-pro/locale';

app.use(uViewPro, {
  locale: { locales: [zhCN, enUS], defaultLocale: 'zh-CN' }
})
```

方式二：使用 `u-config-provider` 或 `useLocale()` 在组件级提供 `locales` 和 `currentLocale`。

```vue
<template>
  <u-config-provider
    :locales="locales"
    :current-locale="currentLocale"
  >
    <!-- 你的应用内容 -->
    <u-modal v-model="show" :content="content"></u-modal> 
    <u-button @click="open"> 打开模态框 </u-button>
  </u-config-provider>
</template>

<script setup lang="ts">
import { useLocale } from 'uview-pro'

const { currentLocale, locales } = useLocale()
const show = ref<boolean>(false)
const content = ref<string>('东临碣石，以观沧海')

const open = () => {
    show.value = true
}
</script>
```

* 编程式切换语言：

```ts
import { useLocale } from 'uview-pro';

const { setLocale } = useLocale()
setLocale('en-US')
```

## 覆盖默认语言包

* 局部覆盖：在 `locale.locales` 中传入部分字段，uView Pro 将与内置文案合并（深度覆盖）。

```typescript
// main.ts
app.use(uViewPro, {
  theme: themes,
  locale: {
    locales: [{
      name: 'zh-CN',
      modal: {
        confirmText: '好的',  // 自定义确认按钮文案
        cancelText: '算了'   // 自定义取消按钮文案
      },
      upload: {
        uploadText: '选择文件'  // 自定义上传文案
      }
    }],
    defaultLocale: 'zh-CN'
  }
})
```

## 添加新语言包

* 新增语言：创建语言文件（示例 `src/locales/fr-FR.ts`，包含 `name` 字段及组件文案），并在入口注册。所有字段见下方“[语言包字段说明](#语言包字段说明)”章节。

假设我们要为应用添加法语支持：

```typescript
// 首先创建法语语言包文件
// src/locales/fr-FR.ts
export default {
  name: 'fr-FR', // 必须要有
  actionSheet: {
    cancelText: 'Annuler'
  },
  modal: {
    title: 'Avertissement',
    content: 'Contenu',
    confirmText: 'Confirmer',
    cancelText: 'Annuler'
  },
  calendar: {
    startText: 'Début',
    endText: 'Fin',
    confirmText: 'Confirmer',
    toolTip: 'Sélectionner une date',
    // ... 其他法语翻译
  },
  upload: {
    uploadText: 'Sélectionner une image',
    retry: 'Réessayer',
    overSize: 'Le fichier dépasse la taille autorisée',
    // ... 更多法语文案
  },
  // ... 继续添加其他组件的法语翻译
}
```

::: tip 注意

1. 必须将 `name` 字段作为语言包的唯一标识。
2. 新的语言包中必须包含所有字段，否则未存在的字段将会显示异常。

:::

在入口注册时引入并添加该语言包：

```typescript
// main.ts
import { createApp } from 'vue'
import uViewPro from 'uview-pro'
import frFR from './locales/fr-FR'

const app = createApp(App)

app.use(uViewPro, {
  theme: themes,
  locale: {
    locales: [frFR], // 添加法语语言包
    defaultLocale: 'fr-FR' // 设置默认语言为法语，为语言包中的name字段
  }
})
```

## 国际化 Hook 使用

* Hook 使用：

```ts
import { useLocale } from 'uview-pro';

const { t } = useLocale('modal')
const text = t('confirmText') // 等价于 t('modal.confirmText')

// 等价于
const { t } = useLocale();
const text = t('modal.confirmText');
```

* 动态参数替换：`t('welcome', { name: '张三' })` → "欢迎您，张三！"

## 与 vue-i18n 集成

[vue-i18n 官方文档](https://vue-i18n.intlify.dev/)

方案：使用 `vue-i18n` 管理业务文案，uView Pro 管理组件文案。

启动顺序建议先 `app.use(i18n)`，再 `app.use(uViewPro, { locale: { defaultLocale: ... } })`，切换时同步两端语言即可。

### 1. 注册 vue-i18n 和 uView Pro

首先你应该在项目中配置vue-i18n：

```typescript
// src/locales/index.ts
import { createI18n } from 'vue-i18n';

import zhCN from './langs/zh-CN.json'; // 简体中文
import enUS from './langs/en-US.json'; // 英文

const messages = {
  'zh-Hans': zhCN,
  en: enUS,
};

// 自动检测用户语言
const getDefaultLocale = () => {
  try {
    const lang = uni.getLocale?.() || 'zh-Hans';
    return lang.startsWith('zh') ? 'zh-Hans' : 'en';
  } catch {
    return 'zh-Hans';
  }
};

const i18n = createI18n({
  locale: getDefaultLocale(),
  fallbackLocale: 'zh-Hans',
  messages,
  allowComposition: true,
  legacy: false,
  globalInjection: true
});

export default i18n;
```

然后在main.ts中集成vue-i18n和uView Pro：

```typescript
// main.ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import i18n from './locales';
import uViewPro from 'uview-pro';

const app = createSSRApp(App);

// 先使用vue-i18n
app.use(i18n);

// 再使用uView Pro，并配置国际化
app.use(uViewPro, {
  locale: {
    // 设置 'zh-CN' 为默认语言
    defaultLocale: 'zh-CN'
  }
});
```

### 2. 语言切换

将 `vue-i18n` 的 `locale` 与 uView Pro 的 `setLocale()` 进行映射（如 `zh-Hans` ↔ `zh-CN`）。

```ts
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useLocale } from 'uview-pro';

const { t, locale } = useI18n();
const { setLocale } = useLocale();

type LocaleKey = 'zh-Hans' | 'en';

const handleLocaleChange = (value: LocaleKey) => {
  // 设置vue-i18n语言
  locale.value = value;

  // 设置系统语言
  uni.setLocale(value);

  // 设置uView Pro语言
  const uViewLocale = value === 'zh-Hans' ? 'zh-CN' : 'en-US';
  setLocale(uViewLocale);
};

// 切换到英文
handleLocaleChange('en');
// 切换到中文
handleLocaleChange('zh-Hans');
```

## 常见 API 摘要

* `useLocale()` → 返回 `{ t, setLocale, currentLocale, locales }`。
* `t(key, params?)` → 获取翻译字符串并支持参数替换。
* `setLocale(name)` → 切换语言（例如 `zh-CN` / `en-US`）。

uView Pro 的 i18n 旨在提供实用、可扩展且易集成的组件文案国际化能力。项目中建议用 `vue-i18n` 管理业务文案，uView Pro 管理组件文案，切换时同步即可。

## 语言包字段说明

uview Pro 默认支持 2 个语言包（中文、英文），更多语言包请自行添加，下述为所有字段：

::: code-group

```ts [zh-CN]
export default {
    name: 'zh-CN',
    uActionSheet: {
        cancelText: '取消'
    },
    uUpload: {
        uploadText: '选择图片',
        retry: '点击重试',
        overSize: '超出允许的文件大小',
        overMaxCount: '超出最大允许的文件个数',
        reUpload: '重新上传',
        uploadFailed: '上传失败，请重试',
        modalTitle: '提示',
        deleteConfirm: '您确定要删除此项吗？',
        terminatedRemove: '已终止移除',
        removeSuccess: '移除成功',
        previewFailed: '预览图片失败',
        notAllowedExt: '不允许选择{ext}格式的文件',
        noAction: '请配置上传地址'
    },
    uVerificationCode: {
        startText: '获取验证码',
        changeText: 'X秒重新获取',
        endText: '重新获取'
    },
    uSection: {
        subTitle: '更多'
    },
    uSelect: {
        cancelText: '取消',
        confirmText: '确认'
    },
    uSearch: {
        placeholder: '请输入关键字',
        actionText: '搜索'
    },
    uNoNetwork: {
        tips: '哎呀，网络信号丢失',
        checkNetwork: '请检查网络，或前往',
        setting: '设置',
        retry: '重试',
        noConnection: '无网络连接',
        connected: '网络已连接'
    },
    uReadMore: {
        closeText: '展开阅读全文',
        openText: '收起'
    },
    uPagination: {
        prevText: '上一页',
        nextText: '下一页'
    },
    uPicker: {
        cancelText: '取消',
        confirmText: '确认'
    },
    uModal: {
        title: '提示',
        content: '内容',
        confirmText: '确认',
        cancelText: '取消'
    },
    uLoadmore: {
        loadmore: '加载更多',
        loading: '正在加载...',
        nomore: '没有更多了'
    },
    uLink: {
        mpTips: '链接已复制，请在浏览器打开'
    },
    uKeyboard: {
        cancelText: '取消',
        confirmText: '确认',
        number: '数字键盘',
        idCard: '身份证键盘',
        plate: '车牌号键盘'
    },
    uInput: {
        placeholder: '请输入内容'
    },
    uCalendar: {
        startText: '开始',
        endText: '结束',
        toolTip: '选择日期',
        outOfRange: '日期超出范围啦~',
        year: '年',
        month: '月',
        sun: '日',
        mon: '一',
        tue: '二',
        wed: '三',
        thu: '四',
        fri: '五',
        sat: '六',
        confirmText: '确定',
        to: '至'
    },
    uEmpty: {
        car: '购物车为空',
        page: '页面不存在',
        search: '没有搜索结果',
        address: '没有收货地址',
        wifi: '没有WiFi',
        order: '订单为空',
        coupon: '没有优惠券',
        favor: '暂无收藏',
        permission: '无权限',
        history: '无历史记录',
        news: '无新闻列表',
        message: '消息列表为空',
        list: '列表为空',
        data: '数据为空'
    },
    uCountDown: {
        day: '天',
        hour: '时',
        minute: '分',
        second: '秒'
    },
    uFullScreen: {
        title: '发现新版本',
        upgrade: '升级'
    }
};
```

```ts [en-US]
export default {
    name: 'en-US',
    uActionSheet: {
        cancelText: 'Cancel'
    },
    uUpload: {
        uploadText: 'Select Image',
        retry: 'Retry',
        overSize: 'File size exceeds allowed limit',
        overMaxCount: 'Exceeds maximum allowed number of files',
        reUpload: 'Re-upload',
        uploadFailed: 'Upload failed, please try again',
        modalTitle: 'Notice',
        deleteConfirm: 'Are you sure you want to delete this item?',
        terminatedRemove: 'Removal cancelled',
        removeSuccess: 'Removed successfully',
        previewFailed: 'Failed to preview image',
        notAllowedExt: 'Files with {ext} format are not allowed',
        noAction: 'Please configure upload address'
    },
    uVerificationCode: {
        startText: 'Get Code',
        changeText: 'Retry in Xs',
        endText: 'Retry'
    },
    uSection: {
        subTitle: 'More'
    },
    uSelect: {
        cancelText: 'Cancel',
        confirmText: 'Confirm'
    },
    uSearch: {
        placeholder: 'Please enter keywords',
        actionText: 'Search'
    },
    uNoNetwork: {
        tips: 'Ooops, network disconnected',
        checkNetwork: 'Please check network or go to',
        setting: 'Settings',
        retry: 'Retry',
        noConnection: 'No network connection',
        connected: 'Network connected'
    },
    uReadMore: {
        closeText: 'Read More',
        openText: 'Collapse'
    },
    uPagination: {
        prevText: 'Prev',
        nextText: 'Next'
    },
    uPicker: {
        cancelText: 'Cancel',
        confirmText: 'Confirm'
    },
    uModal: {
        title: 'Notice',
        content: 'Content',
        confirmText: 'Confirm',
        cancelText: 'Cancel'
    },
    uLoadmore: {
        loadmore: 'Load more',
        loading: 'Loading...',
        nomore: 'No more'
    },
    uLink: {
        mpTips: 'Link copied, please open it in browser'
    },
    uKeyboard: {
        cancelText: 'Cancel',
        confirmText: 'Confirm',
        number: 'Number Keyboard',
        idCard: 'ID Card Keyboard',
        plate: 'Plate Keyboard'
    },
    uInput: {
        placeholder: 'Please enter'
    },
    uCalendar: {
        startText: 'Start',
        endText: 'End',
        toolTip: 'Select date',
        outOfRange: 'Date out of range',
        year: '',
        month: '',
        sun: 'Sun',
        mon: 'Mon',
        tue: 'Tue',
        wed: 'Wed',
        thu: 'Thu',
        fri: 'Fri',
        sat: 'Sat',
        confirmText: 'Confirm',
        to: ' to '
    },
    uEmpty: {
        car: 'Shopping cart is empty',
        page: 'Page not found',
        search: 'No search results',
        address: 'No shipping address',
        wifi: 'No WiFi',
        order: 'No orders',
        coupon: 'No coupons',
        favor: 'No favorites',
        permission: 'No permission',
        history: 'No history',
        news: 'No news',
        message: 'No messages',
        list: 'No list',
        data: 'No data'
    },
    uCountDown: {
        day: 'days',
        hour: 'hours',
        minute: 'minutes',
        second: 'Second'
    },
    uFullScreen: {
        title: 'New Version Available',
        upgrade: 'Upgrade'
    }
};
```

:::

---

---
url: 'https://uviewpro.cn/zh/layout/menu.md'
---
# 垂直分类




uView为用户制作了两个类型的分类页面，分别是左右联动，左右分开的场景。\
这两个页面，为布局而非组件形式，可以根据自己的需求修改页面的结构，逻辑，样式。

## 左右联动

该场景左右可以联动，右边所有的内容在一个大盒子中，点击左边的分类，右边会上下滚动。滑动右边的内容，左边
的分类也会对应激活。

## 左右分开

该场景左右是分开的，左边一个分类对应右边一个盒子，只有通过左边的tab分类，才能改变右边的内容。

---

---
url: 'https://uviewpro.cn/zh/layout/citySelect.md'
---
# 城市选择




这个界面功能，为城市选择示例，此仅为参考模板，如果演示达不到您想要的效果，请自行修改即可。

---

---
url: 'https://uviewpro.cn/zh/guide/customTheme.md'
---
# 多主题与暗黑模式&#x20;

:::tip 说明
本文适用于 uView Pro 版本 0.4.1 及以上，支持单主题、多主题、暗黑模式等。
:::

本文面向 uView Pro 组件库使用者，帮助你在 Uni-app 项目中完整启用 uView Pro 的多主题与暗黑模式能力，重点围绕 `useTheme` 的 API 和最佳实践展开。

## 核心能力

* **一次性初始化**：在应用入口通过 `initTheme` 注入自定义主题，支持多套配置并自动生成暗黑色板。
* **响应式主题状态**：`useTheme` 暴露 `currentTheme`、`themes`、`darkMode`、`cssVars` 等 ref，可直接用于模板。
* **暗黑模式策略**：支持 `auto` 跟随系统、`light`、`dark` 三种模式，且可在运行时主动切换。
* **颜色获取**：CSS 场景使用 `$u-*` SCSS 变量，内联样式使用 `$u.color.xxx` 或 `useTheme().cssVars` / `useColor()` 返回值，确保实时响应。

## 生成主题

通过【[`主题配置工具ThemeGenerate`](/zh/guide/themeGenerate.html)】生成主题文件 `uview-pro.theme.ts`

* 生成后复制到 `src/uview-pro.theme.ts`，默认导出一个数组，每个元素描述一套主题：

```ts
export default [
  {
    name: 'midnight-black',
    label: '午夜黑',
    color: {
      primary: '#ff7a18',
      // ... 亮色色板
    },
    darkColor: {
      primaryLight: '#ffb066'
      // 留空的暗色会由系统智能生成
    }
  },
  // 其他主题...
];
```

* 只提供 `color` 也可以，缺失的 `darkColor` 会自动按规则补齐；若部分暗色需要自定义，只需在 `darkColor` 中填写对应键，其余仍会自动生成。

## 注册主题

### 基础使用

在 `unis.scss`中引入`uview-pro/theme.scss`

```scss
@import 'uview-pro/theme.scss';
```

在 `main.ts` 中注册 uView Pro

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import themes from '@/uview-pro.theme';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, { theme: themes }); // 只需传入一次
  return { app };
}
```

* `install` 内部会调用 `useTheme().initTheme`，无需手动再次初始化，确保主题数据全局唯一。

### 使用系统单主题

如果你是使用系统单主题，且需要修改主题色，可以进行如下配置：

:::tip 注意
仅使用系统单主题不可自定义暗黑色值的主题色
:::

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, {
      theme: {
          primary: '#000000',
          // ...
      }
  });
  return { app };
}
```

### 自定义单/多主题

如果你是多主题并在初始化时设置默认主题和暗黑模式，可以进行如下配置：

:::tip 注意
版本支持
:::

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import themes from '@/uview-pro.theme';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, {
      theme: {
          themes: themes,
          defaultTheme: 'purple', // 默认主题名称
          defaultDarkMode: 'auto' // 默认暗黑模式：auto、light、dark
      }
  });
  return { app };
}
```

## 监听主题切换

> 需要配合虚拟根组件([uni-ku-root](https://github.com/uni-ku/root)) 来做全局共享

如果你不想使用`uni-ku-root`虚拟根组件，也可以自己定义一个全局根组件，但是必须要使用 `u-config-provider` 组件来包裹内部所有页面！

### 安装

::: code-group

```bash [npm]
npm i -D @uni-ku/root
```

```bash [yarn]
yarn add -D @uni-ku/root
```

```bash [pnpm]
pnpm add -D @uni-ku/root
```

:::

### 引入

* CLI项目: 直接编辑 根目录下的 vite.config.(js|ts)
* HBuilderX项目: 需要在根目录下 创建 vite.config.(js|ts)

```ts
// vite.config.(js|ts)

import { defineConfig } from 'vite'
import UniKuRoot from '@uni-ku/root'
import Uni from '@dcloudio/vite-plugin-uni'

export default defineConfig({
  plugins: [
    // ...plugins
    UniKuRoot(),
    Uni()
  ]
})
```

:::tip
若存在改变 pages.json 的插件，需要将 UniKuRoot 放置其后
:::

### 使用

1. 创建根组件并处理全局配置组件

* CLI项目: 在 **src** 目录下创建下 App.ku.vue
* HBuilderX项目: 在 **根** 目录下创建 App.ku.vue

:::tip
在 App.ku.vue 中标签 `<KuRootView />` 代表指定视图存放位置
:::

在全局根组件包裹 `u-config-provider`

```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
import { computed } from 'vue';

const { darkMode, themes, currentTheme } = useTheme();

const themeName = computed(() => currentTheme.value?.name);
</script>

<template>
  <u-config-provider :dark-mode="darkMode" :current-theme="themeName" :themes="themes">
    <KuRootView />
  </u-config-provider>
</template>
```

* `u-config-provider` 负责把 CSS 变量注入到页面，同时监听主题/模式切换事件，具体 API 见 [u-config-provider 文档](/zh/components/configProvider.html)。

## 在项目中使用

> 以上配置完成后需重新编译项目即可生效使用

在 scss 中使用：

```html
<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
    /* 或使用 css 变量 */
    color: var(--u-type-primary);
	}
</style>

```

在 vue/ts 中使用：

```js
import { ref, onMounted } from 'vue';
import {$u} from 'uview-pro'
const color = ref('');

onMounted(() => {
  color.value = uni.$u.color['primary'];
  // 或
  color.value = $u.color['primary'];
});
```

## `useTheme` API

```ts
const {
  currentTheme, // Ref<Theme | null>
  themes,       // Ref<Theme[]>
  darkMode,     // Ref<'light' | 'dark' | 'auto'>
  cssVars,      // Ref<Record<string, string>>
  setTheme,
  getCurrentTheme,
  getAvailableThemes,
  initTheme,
  getDarkMode,
  setDarkMode,
  isInDarkMode,
  toggleDarkMode
} = useTheme();
```

* **currentTheme / themes**：直接在模板中使用，例如 `currentTheme?.name`、`themes.map(...)`。
* **cssVars**：包含诸如 `--u-type-primary`, `--u-bg-color` 等变量，可配合 `v-bind` 绑定到行内样式。
* **setTheme(name)**：切换到指定主题，内部会持久化到 `Storage`，下次启动自动恢复。
* **initTheme(list, defaultName?)**：大多数场景无需手动调用；只有当你在运行时动态获取主题列表时，需要显式调用一次。
* **getDarkMode / setDarkMode**：读写当前暗黑策略；`setDarkMode('auto')` 会立即跟随系统主题。
* **toggleDarkMode()**：在 `light` 与 `dark` 间快速切换，常用于快捷开关。
* **isInDarkMode()**：返回布尔值，表示当前是否处于暗黑渲染状态（`auto` 时会考虑系统设置）。

## 响应式颜色

* **SCSS / CSS**：继续使用 `$u-xxx` 变量，例如

```scss
.card {
  background-color: $u-bg-white;
  border-color: $u-border-color;
}
```

* **模板行内样式**：使用 `$u.color.xxx` 或 `useTheme().cssVars`

```vue
<view :style="{ color: $u.color.primary }">按钮</view>
<view :style="{ backgroundColor: `rgba(var(--u-type-primary-rgb), 0.15)` }" />
<view :style="{ backgroundColor: `var(--u-type-primary)` }" />
```

* **组合式 API**：`useColor()`（可选）提供 `getColor(name)`，在脚本逻辑中获取实时颜色值。

## 构建主题切换 UI 示例

```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
const { themes, currentTheme, setTheme, darkMode, setDarkMode, toggleDarkMode } = useTheme();
</script>

<template>
  <picker :range="themes" range-key="label" @change="e => setTheme(themes[e.detail.value].name)">
    <view>当前主题：{{ currentTheme?.label }}</view>
  </picker>
  <u-switch :checked="darkMode === 'dark'" @change="toggleDarkMode" />
  <u-button @click="setDarkMode('auto')">跟随系统</u-button>
</template>
```

## 系统暗黑模式与持久化

* 首次进入应用时，如果 `darkMode` 设置为 `auto`，库会读取 `uni.getSystemInfoSync().theme` 并立即同步。
* 随后通过 `uni.onThemeChange`/`window.matchMedia` 监听系统变化，保持与系统一致。
* 主题、暗黑模式均存储在本地 Storage，实现跨页面、重启仍然生效。

## 常见问题

* **Q: 为什么动态写入 style 的颜色没有更新？**\
  A: 确保使用 `$u.color.xxx` 或 `useTheme().cssVars`，而不是硬编码十六进制。
* **Q: 只传入了一个主题对象是否可行？**\
  A: 可以。传递 `options.theme` 时会与默认主题合并，仍具备暗黑模式。
* **Q: 如何为特定主题手动定制暗黑色？**\
  A: 在 `darkColor` 中写入需要覆盖的键（例如 `primaryLight`），其余键仍由系统生成，保证一致性。

完成以上步骤即可获得统一、响应式、可扩展的主题与暗黑体验。若需更复杂的用例，可结合 `useTheme` 返回的 `cssVars` 做自定义动画或渐变效果。

---

---
url: 'https://uviewpro.cn/zh/guide/themeGenerate.md'
---
# 多主题配置工具&#x20;

:::tip 说明
自 uView Pro 0.4.1 版本开始，uView Pro 提供了多套主题和暗黑模式配置工具，帮助用户快速配置主题。
:::

uView Pro 目前可以自定义多套主题，包括主题色，字体颜色，边框颜色，背景颜色等，所有组件内部的样式，都基于同一套主题，比如您修改了`primary`主题色，所有用到了`primary`颜色的组件都会受影响。

基于以下主题配置工具可以配置多套主题！

## 配置教程

1. 在打开的颜色拾取器中输入或者选择颜色，再点"确定"按钮即可；
2. 颜色配置完后，在页面底部填写主题元信息（name/label/description）后，点击导出；
3. 如果是导出多主题，可以配置好一套主题后**添加到导出队列**，再次配置其他主题，最终都**添加到导出队列**中，再点击导出；
4. 最终导出会得到一个名为 `uview-pro.theme.ts` 的文件。

## 配置工具

::: tip 提示
该工具支持单主题、多主题配置，支持智能生成颜色值、暗黑色值，随机主题颜色等。配置完成后点击导出，即可得到主题配置文件。
:::

---

---
url: 'https://uviewpro.cn/zh/components/safeAreaInset.md'
---
# 安全区适配

## 底部安全区&#x20;

这个适配，主要是针对 IPhone X 等一些底部带指示条的机型，指示条的操作区域与页面底部存在重合，容易导致用户误操作，因此我们需要针对这些机型进行底部安全区适配。\
uView Pro 是 uni-app 态的 UI 框架 uni-app 专门针对底部安全区域的解决方案，具体如下(也可见 uni 官方说明[全面屏、刘海屏适配（iphoneX 适配）及安全区设置](https://ask.dcloud.net.cn/article/35564))：

* 在 APP 上(以下只对 APP 生效)，可以通过项目根目录的`mainfest.json`文件`app-plus`节点下配置`safearea`的`bottom`属性为`none`，以此来关闭 IPhone X 等机型的底部安全区域。

配置后需要重新编译，并重启调试基座才会生效，具体如下：

```json
"app-plus": {
	"safearea": {
		"bottom": {
			"offset": "none"
		}
	}
}
```

如果`offset`设置为`auto`，那么在 IPhone X 的底部安全区，APP 上就会生成一个原生的元素进行占位，此时也就无需解决安全区指示条引起的问题。

* 在非 APP 端，诸如小程序，或者微信浏览器(其他浏览器，如 UC 等手机浏览器，底部有浏览器工具条，不存在安全区指示条引起的问题)，底部是没有安全区占位的。

像这种情况，就要使用 css 去解决，一般是通过给元素添加底部内边距的形式，如下：

```html
<style>
  .list {
    padding-bottom: 0;
    padding-bottom: constant(safe-area-inset-bottom);
    padding-bottom: env(safe-area-inset-bottom);
  }
</style>
```

鉴于以上问题，uView Pro 提供了一个组件`u-safe-bottom`，如果有需要，您可以在任何地方引用它，它会自动判断在并且在 IPhone X 等机型的时候，给元素加上一个适当
底部内边距，在 APP 上，即使您保留了原生安全区占位(`offset`设置为`auto`)，也不会导致底部出现双倍的空白区域，也即 APP 上`offset`设置为`auto`时。

```html
<template>
  <view>
    ......
    <u-safe-bottom></u-safe-bottom>
  </view>
</template>
```

## 顶部安全区&#x20;

由于我们在做页面布局时经常会使用顶部位置，uView Pro 提供了一个组件`u-status-bar`，如`u-popup`从顶部弹出时，可以考虑使用此组件。

```html
<template>
  <view>
    <u-status-bar></u-status-bar>
    ......
  </view>
</template>
```

## 关于 uView Pro 某些组件`safe-area-inset`参数的说明

在 uView Pro 中，一些组件如`u-popup`、`u-keyboard`组件等，提供了一个`safeAreaInsetBottom`参数(布尔类型)，如果设置为`true`，就会在组件内部对安全区进行适配，
从而避免安全区指示条引起的问题，以下为 uView Pro 的`u-keyboard`组件在`微信浏览器`中分别设置`safeAreaInsetBottom`参数
为`false`和`true`的表现：

---

---
url: 'https://uviewpro.cn/zh/components/install.md'
---
# 安装

:::tip 说明

1. 由于 uView Pro 使用`easycom`模式，让您无需引入组件即可直接使用，但是此功能需要 Hbuilder X 2.5.5 及以上版本才支持，详见[配置 easycom 组件模式](/zh/components/quickstart.html#_3-配置easycom组件模式)。
   `easycom`打包的时候是**按需引入**的，您可以放心引入 uView Pro 的整个组件库，发布打包时会自动剔除您没有使用的组件(注意：调试时仍然是全部引入的)

2. 请确保您下载的[Hbuilder X](https://www.dcloud.io/hbuilderx.html)为`APP开发版`，而非`标准版`，并且在"工具-插件安装"中安装了"scss/sass 编译"插件

:::

:::tip 注意
sass、sass-loader 版本过高或过低，导致编译异常，因此推荐统一并锁定依赖版本：

```json
"sass": "1.63.2",
"sass-loader": "10.4.1"
```

:::

## 方式一：npm 安装

使用 npm 的方式安装，能更方便进行升级。

**注意：** 项目名称不能有**中文**字符。

如果您的项目是HX创建的，根目录又没有package.json文件的话，请先执行如下命令：

```bash
npm init -y
```

执行安装命令：
::: code-group

```bash [npm]
npm i uview-pro
```

```bash [yarn]
yarn add uview-pro
```

```bash [pnpm]
pnpm add uview-pro
```

:::

## 方式二：下载安装

通过 HBuilderX 插件市场或手动下载，将 uView Pro 放入 `uni_modules` 目录。

[插件市场：https://ext.dcloud.net.cn/plugin?id=24633](https://ext.dcloud.net.cn/plugin?id=24633)

使用下载的方式安装，能更方便阅读源码，但是每次升级都需要重新下载并覆盖 `uview-pro` 文件夹。

* 在 uni-app 插件市场右上角选择 `下载并导入HBuilder X`，会直接导入到项目 `src` 目录的 `uni_modules` 目录中。
* 如果您的项目是由 HBuilder X 创建的标准 uni-app 项目，将下载后的`uview-pro`文件夹，复制到项目`uni_modules`目录。
* 如果您的项目是由[vue-cli](https://uniapp.dcloud.io/quickstart?id=_2-%e9%80%9a%e8%bf%87vue-cli%e5%91%bd%e4%bb%a4%e8%a1%8c)模式创建的，请将下载后的`uview-pro`文件夹放到项目的`src`的 `uni_modules`文件夹中即可。

## 版本查询

* 通过源码查看的形式

可以查阅 uView Pro 的配置文件得知当前版本号，具体位置为 "/uview-pro/package.json" 中的 "version" 字段。

## 示例项目

此方式为整个 uView Pro 演示项目，里面有 uView Pro 核心，组件演示，模板等，建议用户可以下载
此项目运行用于查看 UI 演示效果，复制模板案例，通过里面的示例，可以快速掌握某一个组件的用法。

* 途径一：在 uni-app 插件市场右上角选择`使用 HBuilderX 导入示例项目`或者`下载示例项目ZIP`，然后在 HBuilder X 中运行即可。

  * 插件市场：<https://ext.dcloud.net.cn/plugin?id=24633>

* 途径二：通过 Github 或 Gitee 下载 uView Pro 示例项目，在 VSCode 中运行即可。
  * Github：<https://github.com/anyup/uview-pro>
  * Gitee：<https://gitee.com/anyup/uview-pro>

```bash

pnpm install

pnpm run dev:h5
```

:::tip 注意
演示项目不适用于直接开发中，它只是演示用的，可以直接运行并查看效果。\
如果在微信开发工具真机预览时，提示分包太大运行的问题，请在`HBuilder X`进行设置：菜单栏 运行 -> 运行到小程序模拟器，在下拉菜单中**勾选**"运行时是否压缩代码"
:::

---

---
url: 'https://uviewpro.cn/zh/guide/faq.md'
---
# 常见问题与解决方案

:::tip 说明
综合社区反馈与官方文档，系统梳理了使用 uView Pro 组件库开发 uni-app 应用时的常见问题、解决方案及最佳实践，帮助大家高效避坑、提升项目质量。

本文会持续更新一些常见问题及解决方案
:::

## 目录

* [1.组件无法正常显示/样式错乱](#_1-组件无法正常显示-样式错乱)
* [2.npm 与 uni\_modules 安装混用导致依赖冲突](#_2-npm-与-uni-modules-安装混用导致依赖冲突)
* [3.Volar/TypeScript 类型提示缺失](#_3-volar-typescript-类型提示缺失)
* [4.组件属性报错无提示](#_4-组件属性报错无提示)
* [5.工具函数类型提示与 tree-shaking](#_5-工具函数类型提示与-tree-shaking)
* [6.HBuilderX/WebStorm 项目类型提示支持不足](#_6-hbuilderx-webstorm-项目类型提示支持不足)
* [7.组件未识别/打包异常/运行报错](#_7-组件未识别-打包异常-运行报错)
* [8.主题定制与全局样式冲突](#_8-主题定制与全局样式冲突)
* [9.与其他组件库（如 uview-plus 等）引入冲突](#_9-与其他组件库-如-uview-plus-等-引入冲突)
* [10.使用 Sass 时语法不对引起的 bug](#_10-使用-sass-时语法不对引起的-bug)
* [11.ref 和组件同名报错问题](#_11-ref-和组件同名报错问题)
* [12.UnoCss 解析规则与组件库冲突问题](#_12-unocss-解析规则与组件库冲突问题)

## 1.组件无法正常显示/样式错乱

**原因分析**：

* 未正确引入 uView Pro 组件库或样式
* easycom 配置缺失或路径错误
* 组件名拼写错误

**解决方案**：

* 按官方文档配置 easycom，推荐使用自动引入：

```json
    // pages.json
    "easycom": {
      "autoscan": true,
      "custom": {
        "^u-(.*)": "@/uni_modules/uview-pro/components/u-$1/u-$1.vue"
      }
```

* 确认 `main.ts` 已全局引入 uView Pro
* 检查组件名、路径拼写，建议复制粘贴官方示例
* 如样式异常，检查 `uview-pro/theme.scss` 是否全局引入，检查`uview-pro/index.scss` 是否引入
* 检查 easycom 配置是否正确

## 2.npm 与 uni\_modules 安装混用导致依赖冲突

**原因分析**：

* 同时存在 npm 安装和 uni\_modules 方式，依赖重复
* 依赖版本不一致，导致打包异常

**解决方案**：

* 推荐二选一：**npm 安装（CLI 项目）** 或 **uni\_modules 安装（HBuilderX 项目）**
* 清理无用依赖，保持依赖唯一性
* 升级至最新版本，避免历史 bug

**最佳实践**：

* CLI 项目优先使用 npm 安装，便于版本管理与类型提示
* HBuilderX 项目优先使用 uni\_modules，兼容性更好

## 3.Volar/TypeScript 类型提示缺失

**原因分析**：

* tsconfig.json 未正确配置 types/typeRoots
* VSCode 未安装 Volar 或未禁用 Vetur
* uView Pro 版本过旧

**解决方案**：

* CLI 项目在 tsconfig.json 添加：
  ```json
  {
    "compilerOptions": {
      "types": ["uview-pro/types"]
    }
  }
  ```
* uni\_modules 方式一般无需配置，如无提示可补充 typeRoots
* 确认 VSCode 仅启用 Volar 插件
* 升级 uView Pro 至最新版
* 重启 VSCode

**效果示例**：

* 组件标签、属性、事件、插槽等均有智能补全与类型校验

## 4.组件属性报错无提示

**原因分析**：

* 组件名、属性名拼写错误
* 未正确配置类型声明
* 依赖未升级

**解决方案**：

* 检查拼写，参考官方文档
* 按类型声明配置 tsconfig.json
* 升级依赖

**最佳实践**：

* 推荐 `<script setup lang="ts">` 书写，享受最完整类型推断
* 善用 IDE 跳转、补全、错误提示

## 5.工具函数类型提示与 tree-shaking

**问题表现**：

* 工具函数类型提示缺失
* 打包体积大

**解决方案**：

* 推荐按需导入工具函数，自动 tree-shaking
  ```ts
  import { deepClone } from 'uview-pro'
  const copy = deepClone(obj) // 类型自动推断
  ```
* 也可通过 $u 或 uni.$u 访问

**最佳实践**：

* 按需导入优先，减少打包体积
* 充分利用类型提示提升开发效率

## 6.HBuilderX/WebStorm 项目类型提示支持不足

**问题表现**：

* HBuilderX/WebStorm 项目下类型提示不全或无效

**解决方案**：

* HBuilderX 暂不支持 tsconfig.json types 配置，建议 CLI 项目开发获得最佳 TS 体验
* 如需类型提示，尝试手动补充 typeRoots
* 建议使用 VSCode IDE

## 7.组件未识别/打包异常/运行报错

**原因分析**：

* 组件未注册、路径错误、依赖冲突
* 低版本 uni-app/依赖包

**解决方案**：

* 检查组件注册与路径
* 升级 uni-app 及相关依赖
* 清理 node\_modules/uni\_modules 重新安装

## 8.主题定制与全局样式冲突

**问题表现**：

* 主题色、全局样式被覆盖或冲突

**解决方案**：

* 按官方文档引入并覆盖 theme.scss
* 避免全局样式污染，合理使用作用域
* 主题变量建议统一管理

## 9.与其他组件库（如 uview-plus 等）引入冲突

**问题表现**：

* 组件样式错乱、功能异常、控制台报错
* 组件名、全局样式、工具函数等冲突

**原因分析**：

* 同时引入多个同名或类似命名空间的组件库（如 uview-plus、uView2.x、colorui 等）
* easycom 规则、全局样式、工具函数命名冲突

**解决方案**：

* 尽量避免同一项目中同时引入多个同类组件库，尤其是命名空间重叠的库
* 如需迁移，建议逐步替换为 uView Pro，清理旧依赖和 easycom 配置
* 检查 easycom custom 规则，确保只指向 uView Pro 目录
* 检查全局样式、工具函数命名，避免覆盖
* 如必须共存，建议手动引入组件并区分命名，避免自动扫描

**最佳实践**：

* 项目初期统一组件库选型，避免后期大规模迁移
* 团队协作时明确依赖规范，定期代码审查

## 10.使用 Sass 时语法不对引起的 bug

**问题表现**：

* 编译报错、样式丢失、部分组件样式异常
* 控制台提示 Sass 语法错误或不兼容

**原因分析**：

* Sass 语法与 loader 版本不兼容（如新版 Sass 不再支持 @import、部分语法变更）
* sass、sass-loader 版本过高或过低，导致编译异常
* 未锁定依赖版本，团队成员环境不一致

**解决方案**：

* 推荐统一并锁定依赖版本：

  ```json
  "sass": "1.63.2",
  "sass-loader": "10.4.1"
  ```

* 如遇到语法报错，优先检查 loader 版本与官方文档

* 团队协作时，建议在 package.json 中锁定依赖，避免自动升级

* 删除 node\_modules 并重新安装依赖，确保环境一致

**最佳实践**：

* 定期关注 uView Pro 官方和 Sass 官方的兼容性公告
* 统一团队开发环境，避免“我的能编译你的不能”问题

## 11.ref 和组件同名报错问题

**问题表现**：

* 在 `<template>` 中为组件设置 `ref` 属性时，`ref` 名称与组件名相同，导致运行时报错。

**解决方案**：

* 避免将 `ref` 命名为与组件名完全一致，建议加前缀或后缀区分，如 `ref="uButtonRef"` 而非 `ref="uButton"`。
* 统一团队命名规范，ref 命名建议采用小驼峰或加前缀（如 `uButtonRef`、`uInputRef`）。
* 如遇到类型提示异常，可手动声明类型或调整 ref 名称。

**最佳实践**：

* ref 命名应语义化且避免与组件名、变量名冲突。
* 在 `<script setup lang="ts">` 下，推荐使用类型断言提升类型安全。

**示例**：

```vue
<template>
  <u-button ref="uButtonRef">按钮</u-button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const uButtonRef = ref()
</script>
```

相关 issue：[#22](https://github.com/anyup/uView-Pro/issues/22)

## 12.UnoCss 解析规则与组件库冲突问题

**问题表现**：

* 样式丢失、部分组件样式异常
* h5 平台和小程序平台显示不一致
* 例如：u-icon 组件的 size 属性会被 unocss 解析成 css 属性，导致样式错误

**原因分析**：

* unocss 解析规则与组件库冲突

**解决方案**：

修改 unocss 的 presetAttributify，将其禁用

```ts
import { presetUni } from '@uni-helper/unocss-preset-uni'

import { defineConfig } from 'unocss'

export default defineConfig({
  presets: [
    presetUni({
      attributify: false
    })
  ]
})
```

或修改 unocss 的 presetAttributify，添加有问题的属性配置，进行忽略

```ts
import { presetUni } from '@uni-helper/unocss-preset-uni'

import { defineConfig } from 'unocss'

export default defineConfig({
  presets: [
    presetUni({
      attributify: {
        // 忽略 size 属性会被 unocss 解析成 css 属性，导致样式错误
        ignoreAttributes: ['size']
      }
    })
  ]
})
```

## 最佳实践总结

1. **规范依赖管理**：npm/uni\_modules 二选一，保持依赖唯一性。
2. **优先使用 CLI + npm + Volar + TS**，获得最佳开发体验。
3. **全局配置 easycom 与样式**，组件即用即引。
4. **充分利用类型提示与 IDE 能力**，减少低级错误。
5. **按需导入工具函数，优化打包体积。**
6. **定期升级依赖，关注官方 changelog 与 issue。**
7. **遇到问题多查文档/issue，善用社区资源。**
8. **团队协作时统一配置与代码规范，提升协作效率。**

## 常见问题排查清单

* \[ ] 组件/样式未生效？→ 检查 easycom、样式引入、依赖版本
* \[ ] 类型提示无效？→ 检查 tsconfig.json、Volar 插件、依赖版本
* \[ ] 组件/工具函数报错？→ 检查拼写、注册、依赖冲突
* \[ ] 打包异常？→ 清理 node\_modules/uni\_modules，重新安装
* \[ ] 主题/全局样式冲突？→ 检查 theme.scss 引入与变量覆盖

## 总结

uView Pro 作为 uni-app 生态的新星组件库，凭借完善的 TS 类型支持、丰富的组件体系和活跃的社区生态，极大提升了多端开发效率。只要遵循本文最佳实践与排查清单，大部分常见问题都能高效解决。

**官方资源**：

* [uView Pro 官方文档](https://uviewpro.cn)
* [GitHub 开源仓库](https://github.com/anyup/uview-pro)
* [Gitee 镜像](https://gitee.com/anyup/uview-pro)
* [插件市场](https://ext.dcloud.net.cn/plugin?id=24633)
* [官方 Issue 区](https://github.com/anyup/uview-pro/issues)
* [社区交流反馈区](https://uviewpro.cn/zh/cooperation/about.html)

如有更多问题，欢迎在官方 issue 区留言或加入交流群反馈！

> 本文根据实际项目补充，内容持续更新，欢迎 Star、Fork、PR、Issue 支持与反馈。

---

---
url: 'https://uviewpro.cn/zh/layout/wxCenter.md'
---
# 微信个人中心




此为模仿微信个人中心首页模板，仅作为参考学习使用，如果如达不到自己的需求，可自行修改。

---

---
url: 'https://uviewpro.cn/zh/components/quickstart.md'
---
# 快速上手

## 如何使用

通过 npm 和下载方式的配置之后，在某个页面可以直接使用组件，无需通过`import`引入组件。

```html
<template>
  <u-action-sheet :list="list" v-model="show"></u-action-sheet>
</template>

<script setup lang="ts">
  import { ref } from "vue";

  interface ListItem {
    text: string;
    color?: string;
    fontSize?: number;
  }

  const list = ref<ListItem[]>([
    { text: "点赞", color: "blue", fontSize: 28 },
    { text: "分享" },
    { text: "评论" },
  ]);

  const show = ref(true);
</script>
```

## 关于 $u

uView Pro 将`$u`对象同时挂载到了`uni`对象上，这意味着您可以在外部的`ts`文件中，通过`uni.$u.xxx`的形式去调用 uView 提供的一些工具方法。

或则您在使用 `$u` 时，先导入再使用：

```html
<script setup lang="ts">
  import { $u } from "uview-pro";

  function func() {
    $u.toast("hello world");
  }
</script>
```

## 如何不使用 easycom 而单独引用某一个组件

某些情况下，您可能不想通过 easycom 引用组件(虽然我们极力推荐您使用 easycom)，那么您可以使用`import`这个常规的引入方式，如下：

```html
<template>
  <my-action-sheet :list="list" v-model="show"></my-action-sheet>
</template>

<script setup lang="ts">
  // 你如果自定义引入的名称，template 中使用组件名称也需要对应
  import myActionSheet from "@/uni_modules/uview-pro/components/u-action-sheet/u-action-sheet.vue";
  import { ref } from "vue";

  interface ListItem {
    text: string;
    color?: string;
    fontSize?: number;
  }

  const list = ref<ListItem[]>([
    { text: "点赞", color: "blue", fontSize: 28 },
    { text: "分享" },
    { text: "评论" },
  ]);

  const show = ref(true);
</script>
```

---

---
url: 'https://uviewpro.cn/zh/reward/sponsor.md'
---
# 成为 uView Pro 赞助商

uView Pro 拥有活跃的开发者社区、完善的文档与高频访问量。您的赞助将帮助我们持续迭代、丰富组件与模板，并在社区中获得长期曝光。

## 为什么赞助

* **高曝光**：官网与文档日均 1 万+ IP，面向前端与跨平台开发者。
* **精准人群**：聚焦 uni-app / Vue / 跨平台开发者及技术决策人。
* **品牌背书**：作为开源支持者，提升品牌技术形象与影响力。

## 我们能提供什么

* 官网/文档合适位置的品牌露出（Logo、链接或简要文案）。
* 在社区动态、版本日志中致谢（视具体合作形式确定）。
* 与产品或技术主题相关的联合推广机会（可选）。

## 合作方式

* 赞助形式灵活，可按季度/年度或专项活动定制。
* 可与我们沟通您的预算、目标与希望的曝光形式，我们将提供匹配方案。

## 联系方式

* 微信（备注“赞助商”）：**anyupxing**
* 邮件：**491302297@qq.com**

期待与您一起，为开源生态与开发者社区贡献力量。谢谢支持！🚀

---

---
url: 'https://uviewpro.cn/zh/reward/donation.md'
---
# 捐赠开源

---

---
url: 'https://uviewpro.cn/zh/layout/submitBar.md'
---
# 提交订单栏




该布局一般用于商品详情页底部引导用户快速购买商品的场景，开发者可以根据自己的需求修改布局结构和样式，
该组件依赖于uView Pro框架，请在安装uView Pro的情况下使用。

---

---
url: 'https://uviewpro.cn/zh/layout/address.md'
---
# 收货地址

此功能包含两个页面，分为展示用户收货地址列表和添加收货地址。相关功能和数据均为本地模拟数据和格式，不一定
和用户实际环境相同，请自行修改对应的js实现逻辑，不要拘泥于模板的示例。

---

---
url: 'https://uviewpro.cn/zh/components/feature.md'
---
# 注意事项

由于 uni-app 支持多端开发，而各端，特别是各小程序平台，没有统一的标准，加重了开发者和企业的成本，幸好 uni-app 使用 Vue 标准，对各端进行了写法的统一，
推动了生态的发展，但是由于某些小程序平台自身的原因，仍然会出现某些兼容性问题，我们会将制作 uView 过程中遇到，和平时收集的兼容性问题呈现在本专题，希望能
帮助到 uni-app 开发者。

## 支付宝小程序

:::tip 注意
uView Pro 需要开启了`component2`模式才支持支付宝小程序
:::

1. 支付宝在很早前，已升级为`component2`模式，此模式支持更多的功能和特性，uni-app 上，很多的特性，如`provide/inject`、`$slots`等，需要开启此模式才能支持，
   而此模式在 uni-app 新建项目中默认是关闭的，因而需要在项目根目录的`manifest.json`中开启，如没有`alipay`属性节点，新增即可：

```json
......
"mp-alipay" : {
	"component2": true
},
......
```

2. uView Pro 的`waterfall`瀑布流组件使用了`$scoped slot`特性，由于 hx 的问题，在 hx2.8.2 修正了此问题，所以瀑布流组件需要 hx2.8.2 及以上才支持支付宝小程序。

## Vue 特性在各平台支持度

1. 以下特性，uView 已对各小程序开发工具，H5 浏览器，APP(不含 NVUE)进行过实测，均获得支持，其中支付宝小程序需要开启`component2`模式。

| App | H5  | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ 小程序 |
| :-: | :-: | :--------: | :----------: | :--------: | :--------: | :-------: |
|  √  |  √  |     √      |      √       |     √      |     √      |     √     |

* provide / inject
* $slots
* v-model / sync
* $parent / $children

## 设置页面背景颜色

一般情况下，我们给页面的`page`节点或者给页面的最外层`view`设置背景颜色，二者分别有如下需要注意点：

### 1. 通过`page`节点设置

这个方式全端有效，但是需要注意的是，在微信小程序，或者某些安卓机型上，该节点如果写在带`scoped`属性的样式标签内是无效的，所以我们建议
您可以在页面多加一个不带 scoped 属性的样式标签，如下：

```css
/* 如果需要css的支持，还可以添加lang属性 */
<style lang="scss">
page {
	background-color: $u-bg-color;
}
</style>

/* 带scoed属性的其他样式 */
<style lang="scss" scoped>
.box {
	......
}
</style>
```

### 2. 通过页面外层`view`设置

相比`page`节点，`view`的高度默认为内容高度，所以如果页面内容不足一屏高度时，底部剩余部分依然为默认的白色，所以我们给需要这个`view`设置一个
最低高度，让它等于窗口高度：

```html
<template>
  <view class="wrap"> ...... </view>
</template>

<style scoped lang="scss">
  .wrap {
    background-color: $u-bg-color;
    min-height: 100vh;
  }
</style>
```

## 全局赋值设备信息的陷阱

我们都知道，可以通过`uni.getSystemInfoSync()`获取设备信息，但是每次用到时都写一遍是很繁琐的，所以很多同学们都会突发奇想，比如在`main.js`或者
在`App.vue`中将`uni.getSystemInfoSync()`的结果赋值给`Vue.prototype`，如下：

```js
// main.js
Vue.prototype.system = uni.getSystemInfoSync();
```

上面的写法没有问题，我们可以任意地方通过`this.system`得到设备的信息，但是这里有一个陷阱，写在`main.js`，意味着赋值代码只会被执行一次，且是 APP 启动的时候，
但是 uni-app 中，设备信息的`windowHeight`属性是不含 APP 的导航栏和 tabbar 高度在内的，当我们进入首页时，`windowHeight`不含 tabbar 高度在内，高度可能为
'700px'，但是进入内页后，没有 tabbar，这时的`windowHeight`高度依然为 700px(少掉了 tabbar 的 50px 高度)，显然是不正确的。\
上面说的只是对`windowHeight`属性有影响，其他的属性无碍，如果是需要获取高度，建议每次都执行`uni.getSystemInfoSync()`，或者通过 uView 提供的快捷工具
`uni.$u.sys()`方法获取即可。

## 小程序主包太大无法预览和发布

我们都知道微信小程序预览和发布的主包大小都不能超过`2M`，否则无法真机预览和上传发布，经常有同学反馈刚使用 uView，调试时候主包就超过了`2M`而无法真机预览，
我们在这里做一个说明，uView 是`按需引入`的，在发行时，HX 会自动剔除您没有使用组件，即使您使用了 uView 的全部组件，整个 uView 的大小也只有 500K 左右，但是有如下两点前提：

* **调试**\
  在调试阶段，为了调试的友好效果和编译速度等，HX 默认是没有对 JS 进行压缩和去除注释，也没有进行组件按需引入的，所以会导致 JS 文件都很大，我们需要在
  HBuilder X 进行如下操作，再重新编译即可：

```js
HBuilderX   运行->运行到小程序模拟器->勾选 运行时是否压缩代码
```

* **发布**\
  在 HX 中进行发布时，uView 的组件会按需引入(使用 uView 所有组件的情况下，占用空间 500k 左右)，如果主包依然超出`2M`，您需要从多个方面着手：

1. [小程序分包](https://uniapp.dcloud.io/collocation/pages?id=subpackages)
2. 将静态资源放到服务器进行引用
3. 取消"ES6 转 ES5"设置

## uni.scss 的优缺点

`uni.scss`为 uni-app 新建项目自带工程文件，使用的预处理器为`sass/scss`，由此可见，uni-app 官方推荐的是`scss`，同时我们 uView 也是`scss`的坚定推崇者，不建议在
uni-app 中使用`less`、`stylus`等。

`uni.scss`具有如下一些特点：

* 无需引入，uni-app 在编译时，会自动引入此文件
* 在此中定义的`scss`变量，可以全局使用，可以在此定义一些颜色，主题，尺寸等变量
* **`uni.scss`会编译到每个`scss`文件中**(请着重理解这一句话)

综上所述，我们可以得知，`uni.scss`主要是利用`scss`的特性，定义一些全局变量，供各个写了`lang=scss`的 style 标签引用，但是这引出了一个重要的问题：\
`uni.scss`中所写的一切内容，都会注入到每个声明了`scss`的文件中，这意味着，如果您的`uni.scss`如果有几百行，大小 10k 左右，那么这个 10k 都会被注入所有的
其他`scss`文件(页面)中，如果您的应用有 50 个页面，那么有可能因此导致整体的包体积多了 50 \* 10 = 500k 的大小，这可能会导致小程序包太大而无法预览和发布，
所以，我们建议您只将`scss`变量相关的内容放到`uni.scss`中。

## 样式覆盖兼容性

为了避免样式被用户覆盖，或者被污染，一般组件或者页面都会给`style`标签加上`scoped`属性，如下演示为一个组件的内部构造：

```html
/* item.vue */
<template>
  <view class="item"></view>
</template>

<style scoped>
  .item {
    border: 1px solid red;
  }
</style>
```

我们在页面中引入上方的`item`组件，并且想修改它的`border`边框为颜色(blue)，一般通过`:deep`或`/deep/`指令修改，如下写法：

```html
<template>
  <item></item>
</template>

<style scoped>
  :deep(.item) {
    border: 1px solid blue;
  }
</style>
```

上面的写法，在`App`和`H5`正常，但是在微信小程序无效，它要求`:deep`或`/deep/`前面必须还要有父元素的类名存在，如下：

```html
<template>
  <view class="wrap">
    <item></item>
  </view>
</template>

<style scoped>
  .wrap :deep(.item) {
    border: 1px solid blue;
  }
</style>
```

如果是在支付宝小程序中，写在组件上的类名和内联样式，都是无效的，如下：

```html
<template>
  /*
  在支付宝小程序，组件标签上的任何class和style都会被剔除，不会添加到组件内部的根元素中
  */
  <item style="border: 1px solid blue" class="item"></item>
</template>
```

---

---
url: 'https://uviewpro.cn/zh/guide/note.md'
---
# 注意事项

## uView Pro 对 nvue 的支持

什么是`nvue`？见[关于 nvue](/zh/guide/design.html#关于nvue)\
目前 uView 是`vue`版本，uView Pro 目前没有兼容 nvue，未来应该也不会兼容

## 技术点要求

1. uView Pro 依赖`SCSS`预处理器，所以您需要给 HBuilder X 安装 “sass/scss 编译” 插件，详见[快速上手](/zh/components/quickstart.html)
2. uView Pro 目前没有兼容 nvue，未来应该也不会兼容
3. uView Pro 基于 VSCode+Vue3 开发，旧版本可能会不兼容
4. uView 要求项目开启 uniapp 的 V3 版本，V3 有很大的优势，详见[V3 版本介绍](https://ask.dcloud.net.cn/article/36599)
5. HX2.5.5 稳定版正式引入`easycom`，建议开发者升级 HX 到 2.5.1 及以上的稳定版，详见[关于 easycom](/zh/components/quickstart.html#_3-配置easycom组件模式)

## 关于 VSCode

uView Pro 基于 VSCode + Vue3 开发，强烈建议使用 VSCode 系列的编辑器，因为 VSCode 的语法提示，代码补全，代码片段，AI 助手等，开发 Vue3 的项目，都是详尽的提示，可以保证你的代码不会出现任何问题。

## 关于 Hbuilder X

uniapp 依赖于 HX，uniapp 经过这两年发展(2018-2020)，势头强劲，茁壮成长。我们目睹了整个过程，陪着 uniapp 一起成长，感慨能有
一家良心企业能扎根技术，埋头苦干，把 APP，H5 还有各家小程序做到大一统，同时也愤慨各家大厂的小程序各自为营，仿佛倒退到多年前
各家[浏览器大战](https://baike.baidu.com/item/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%A4%A7%E6%88%98/8488119?fr=aladdin)的时代，让人唏嘘不已。

uView Pro 也可以使用 HX 作为编辑器：

* 开发者在开发线上项目的时候只使用 HX 的稳定版
* 初学者不要使用 HX 内测版，不然会碰到莫名其妙的问题，会挫败学习信心
* 每当 HX 更新大功能的时候，比如以往的自定义组件模式，近来的 V3 版本，还是目前的 uniCloud，或者以后可能关于 nuve 的大功能，线上项目请过一段时间再使用。
* 建议喜欢尝鲜并熟悉 uniapp 的用户，在电脑分别安装 HX 的稳定版和内测版，尝鲜使用内测版，开发使用稳定版，二者分别更新，互不干扰

## 编译调试

开发的时候，特别是写布局的时候，我们建议使用 chrome 或者 HX 内置的浏览器，需要说明的是，电脑浏览器的预览效果是不精细的，
写完之后，可以手机连上电脑同一局域网的 WiFi，在手机浏览器上再进行细微的调整。\
写完布局再写逻辑的时候，如果还需要兼容小程序和 APP，一定要每写完一个页面，就用 APP 基座和小程序真机进行调试，这能及早发现问题，否则会剪不断理还乱。

## 安全区适配(针对 APP)

在 iPhone X 等机型，底部带有指示条，如果配置了`safearea`则会在底部生成一个原生的白色区块，好处是不会导致
误触，缺点是颜色无法修改，有时候也影响美观。\
uView Pro 在各个可能会受到指示条影响的地方都做了特别处理，比如弹窗，键盘组件等，详见[底部安全区适配](/zh/components/safeAreaInset.html)

## 为什么 uView Pro 的源码中会有那么多的注释？

> uView Pro 和 uView 一样，尽量保持详尽的注释，方便广大开发者使用，也方便开发者维护和升级。

很多开源项目，发布的时候都会刻意去掉注释，这可能是为了干净整洁，也可能是为了减少体积，还可能是出品方认为用户不会，也没必要去阅读源码。\
相反，uView 不这么认为，我们会一直将注释保留在发行的版本中，这些注释不是为了给我们自己看的，而是为了给用户看的。\
我们希望用户在使用的过程中，能通过阅读源码，既能提升工作效率，还能学到知识。因为 uView 的理念是"挣脱束缚，向往自由"，我们也希望您在阅读
源码的过程中，如果发现问题，或者有更好的实现方式和想法，可以反馈给我们，进而构建一个更强健的 UI 框架。

---

---
url: 'https://uviewpro.cn/zh/guide/demo.md'
---
# 演示

uView Pro 会将各个版本的演示在此展示，目前演示的版本有 H5，安卓，微信小程序，其他版本的演示将会陆续添加。

## 使用方法

* H5 版本可以用微信或者手机浏览器扫描二维码即可
* 微信小程序只能通过微信扫码查看
* 安卓版本只能在安卓使用，可以用安卓浏览器或者 QQ 扫码进行安装(**微信中不能扫码安装**)，安装过程中您可能需要勾选相应的提示，允许安装来自非应用市场的 APP，或者您需要在`设置`中打开**允许安装来自未知来源的应用**

## 说明

文档中也有相应的演示示例，但它是通过`iframe`嵌入到网页的，所以可能会造成某些 uni-appAPI 在网页上(浏览器 F12 手机调试模式无问题)无法使用，造成组件有 BUG 的错觉。

**注意：** 建议您只在浏览文档时使用文档右侧的演示功能，电脑示例由于分辨率和 uni-app 用`rpx`单位的问题，显示可能会不够细致，请通过微信扫码小程序体验最佳的效果。

## 扫码

---

---
url: 'https://uviewpro.cn/zh/layout/login.md'
---
# 登录界面




这个界面功能，为模仿美团APP的登录界面，包括输入手机号，获取验证码填写(uView Pro的`MessageInput`组件)等共两个界面。\
如果开发者用到此模板，请自行修改相关的结构和样式等，以达到自己所需的效果。

---

---
url: 'https://uviewpro.cn/zh/guide/codeHint.md'
---
# 编辑器对 uView Pro 的代码提示

> 不建议使用 HBuilder X，建议使用 VSCode

uView Pro 是以 uView 1.8.8 为基础重构，所有组件的 API 均已同步，所以如果你是使用的 uView 1.x，你可以无缝切换到 uView Pro，它同样适配了 HX 的代码提示功能，让用户可以更简单，畅快的使用 uView Pro 的组件，这个提示功能有如下特色：

* 通过敲`<u`关键字(无需`<u-`后面的`-`)，HX 会通过弹出提示列出 uView 的所有组件
* 可以在提示中一键直达对应组件的官方文档
* 提示中有完整的参数类型、 说明，事件描述等提示
* 无需给 HX 安装插件和设置，即可拥有以上提示功能

> 后面会增加基于 uView Pro 的 VSCode 提示插件

## 触发提示

在"\*.vue"文件的模板编写区域，通过`<u`开头的关键字，就能 触发 uView 的组件候选列表：

* 如果想得到更准确的提示，可以完整敲出组件名称，如`<u-badge`就会弹出唯一的提示，此时回车即可键入。
* 如果对某一个组件的名称记忆不清，可凭借大概的字符输入，HX 会按模糊搜索的方式进行匹配可能的组件选项，比如`u-alert-tips`组件，我们可以敲`<u-altip`，
  `<u-tips`，或者`<u-aler`等等，都可识别出组件的提示，总的来说，以`<u`，开头，后面可以是组件的部分关键字，前中后部分都可，大家可自行尝试。

## 一键在浏览器打开组件对应文档

当我们在 HX 匹配到某个组件后，提示框的右边会弹出此组件所在的文档地址，通过鼠标点击，即可在浏览器快速打开对应的文档。

## 参数提示

当我们键入完整的组件结构后，通过`:`开头，即可列出组件的参数，右边有对应的类型和说明提示，还可以通过模糊的匹配的方式(敲出参数名称的部分字符)，快速找到某一个参数。

## 事件提示

某些组件有回调事件，通过`@`开头，即可列出对应的事件名称，右边有事件对应的说明，回车即可自动键入。

---

---
url: 'https://uviewpro.cn/zh/guide/theme.md'
---
# 自定义主题&#x20;

:::tip 说明
本文适用于 uView Pro 版本 0.4.1 以下，仅支持单主题配置等。
:::

uView Pro 目前可以自定主题色，字体颜色，边框颜色等，所有组件内部的样式，都基于同一套主题，比如您修改了`primary`主题色，所有用到了`primary`颜色
的组件都会受影响。

## 教程

1. 可以在打开的颜色拾取器中输入或者选择颜色，再点"确定"按钮即可。
2. 颜色配置完后，在页面底部下载文件，会得到一个名为`uview-pro.theme.scss`和`uview-pro.theme.ts`(可选)的文件。

## 配置 scss 变量

1. 将`uview-pro.theme.scss`文件复制到项目的公共目录(视情况而定)中，再在项目根目录的`uni.scss`中引入即可。
2. 删除`uni.scss`文件中原来引入的`@import 'uview-pro/theme.scss';`(旧的内置主题文件引入语句)。
3. 重新编译项目或者重启编辑器即可生效。

## 配置 ts 变量

1. 将`uview-pro.theme.ts`文件复制到项目的公共目录(视情况而定)中，再在项目根目录的`main.ts`中引入即可，如下：
2. 重新编译项目即可生效。

引入方式：

```ts
import { createSSRApp } from 'vue'
import App from './App.vue'
import theme from '@/common/uview-pro.theme'
import uViewPro from 'uview-pro'

export function createApp() {
  const app = createSSRApp(App)
  // 引入uView Pro 主库，及theme主题
  app.use(uViewPro, { theme })
  return {
    app
  }
}
```

## 如何使用

在 scss 中使用：

```html
<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
	}
</style>

```

在 ts 中使用：

```js
import { ref, onMounted } from 'vue';

const color = ref('');

onMounted(() => {
  color.value = uni.$u.color['primary'];
});
```

两者的主题即可同步！

---

---
url: 'https://uviewpro.cn/zh/guide/customStyle.md'
---
# 自定义样式&#x20;

uView Pro 默认提供了一套美观且统一的组件样式，但在实际项目开发中，往往需要根据业务需求进行个性化定制。参考[自定义主题](/zh/guide/theme.html)。

然而，如果仅是需要覆盖组件的默认样式，或增加样式，uView Pro 则支持两种主流的自定义样式方式，灵活满足各种场景。

:::tip 说明
自 uView Pro 0.3.0 版本开始，所有组件支持两种自定义样式方式。
:::

## 方式一：custom-class 样式穿透

所有组件均支持 `custom-class` 属性，可为组件根节点添加自定义 class，实现样式穿透和深度定制。推荐配合 `:deep()` 或 `/deep/` 实现作用域样式穿透。

**示例：**

```html
<view class="my-page">
  <u-button custom-class="my-btn"></u-button>
</view>
```

```scss
.my-page {
  :deep(.my-btn) {
    background-color: #2979ff;
    color: #fff;
    border-radius: 8px;
  }
}
```

* 可用于自定义背景、字体、边框、动画等任意样式。
* 支持多层嵌套和全局样式覆盖。

## 方式二：custom-style 内联样式

所有组件均支持 `custom-style` 属性，可直接传递内联样式字符串，快速实现样式定制。

**示例：**

```html
<u-button
  custom-style="background: linear-gradient(90deg,#2979ff,#00c6ff);color:#fff;border-radius:8px;"
></u-button>
```

* 适合简单样式调整和动态样式绑定。
* 支持与变量、计算属性结合。

## 进阶说明

* 两种方式可结合使用，优先级：`custom-style` > `custom-class` > 组件默认样式。
* 推荐在页面根节点加唯一 class，避免样式污染。
* 复杂场景建议使用 `custom-class`，便于维护和复用。
* 组件文档均有对应属性说明，详见各组件 API。

## 常见问题

* **为什么样式不生效？**
  * 检查 class 名称是否正确，是否在正确的作用域下。
  * 确认样式优先级，必要时使用 `!important`。
  * Vue3/uni-app 下建议用 `:deep()` 实现穿透。
* **如何批量定制所有组件样式？**
  * 可通过全局样式或主题变量统一覆盖，参考[自定义主题](/zh/guide/theme.html)。

---

---
url: 'https://uviewpro.cn/zh/layout/keyboardPay.md'
---
# 自定义键盘支付




此为结合了uView Pro的[MessageInput 验证码输入](/zh/components/messageInput.html)及[Keyboard 键盘](/zh/components/keyboard.html)组件的模板，
模仿支付的场景，用户可以根据思路，修改出自己想要的效果。

---

---
url: 'https://uviewpro.cn/zh/layout/order.md'
---
# 订单列表




该页面模板结合了uView Pro的[Tabs 标签](/zh/components/tabs.html)组件，可以左右滑动。如果页面没有内容，会提示没有相关内容。\
具体效果请查看示例，手机上查看效果会更好 ，用户可以根据自己的需求修改页面结构，逻辑，样式等。

---

---
url: 'https://uviewpro.cn/zh/guide/design.md'
---
# 设计理念

:::tip 说明
`uView Pro` 的设计理念来源于 `uView 1.x` 和实际项目，由于之前使用 uniapp 开发的项目大多都是 uniapp + Vue2 + uView 1.x，想开始新项目使用 Vue3 时，却没有找到顺手的 UI 组件库，所以萌生了重构 `uView UI 1.x` 的想法，在 Vue3 的基础上重构了 `uView 1.8.8`，这才诞生了 `uView Pro`。

`uView Pro` 的设计理念是：保持 `uView UI 1.x` 简洁的设计理念，使用 Vue3 的语法全面重构每一个组件，并保持现有 API，可以让你无缝切换！
:::

## 导航栏

uniapp 可以通过配置`pages.json`生成原生元素的导航栏，简要说明如下：

* 优点是可以快速渲染，配置便捷，还可以带入一部分原生内容(针对 App Store)
* 缺点是配置不够灵活，遮罩无法覆盖导航栏等

建议：

* 如果开发者使用 nuve，可以直接自定义导航栏，无需使用 uniapp 自带的
* 如果是普通的 vue 页面，直接使用 uniapp 自带导航栏。如果自带的不能满足，条件允许就用`subNVue`绘制，否则就用普通元素绘制

说明：uni 官方有关于导航栏的详细说明，请参见[自定义导航栏](https://uniapp.dcloud.io/collocation/pages?id=customnav)

## 关于 nvue

nvue 源自于 uniapp 引入的阿里 weex 开源原生渲染引擎，单 weex 来说，是不推荐使用的，因为它没有周边的生态和第三方的功能。\
uniapp 引入 weex 之后，一直在整合，但也没有对 weex 进行定制开发，在 APP 端某些需要性能相关的可以使用 nvue，以下是我们对 nvue 的一些见解：

* nvue 具有媲美`react native`的性能，uniapp 一直在打通 vue 和 nvue 的壁垒
* nvue 页面中还不能像写 vue 一样便利，比如对样式的限制，api 还不能和 vue 完全互通等

建议：uniapp 一直在强化 vue，重心不在 nvue，如果不是特别复杂的应用，可以直接使用 vue 开发，应用的首页(V3 版本)使用`nvue`，渲染的速度会有显著的提升，
如果有需要进一步了解，请参见[nvue 开发与 vue 开发的常见区别](https://uniapp.dcloud.io/use-weex?id=nvue开发与vue开发的常见区别)

## 关于单位

我们在 web 中，常用的是`px`，`rem`等单位，`rem`在 uniapp 中不推荐使用，我们分别做如下阐述：

web 中：
可以使用`px`，它属于静态单位，它的最终呈现尺寸不会和屏幕尺寸有关系

uniapp 中(vue 和 nvue)：\
`px`属于静态单位，uni 中还有`upx`和`rpx`单位，`upx`为 uniapp 成立之初的动态单位，后来各家小程序跟随微信小程序，都使用
`rpx`单位，使它成为了既定的事实标准，uniapp 也就提倡并官宣使用`rpx`单位，但是`upx`也一样能使用，和`rpx`效果相同。\
另外：uniapp，vh 和 vw 也完全可以使用的，一般我们需要让某个元素高度铺满整个屏幕时，可以设置高度为`100vh`。

weex 中：
这里说的是阿里的 weex，而不是 uniapp 改良后的 nvue 版本中的 weex，它的`px`单位和 uniapp 中的`rpx`或者`upx`是一样的，也属于
动态单位，它自创了个`wx`单位，和 web 中的`px`一样，属于静态单位。\
说明：uniapp 的 nvue 版本中，虽然也是引入 weex，但是改良后，没有了`wx`，`nvue`的`rpx`(`upx`)与`px`和 uniapp 的 vue 版本单位效果一致。

建议：开发中，只需谨记两个单位，`px`和`rpx`，一般情况下，我们推荐字体和宽高等，都使用`rpx`单位，如果真的需要固定尺寸，就是用`px`。
如果关于各单位和他们的由来历史，还需要进一步了解，可以参见[尺寸单位](https://uniapp.dcloud.io/frame?id=尺寸单位)

## 布局

为兼容多端运行，我们建议开发者使用`flex`，不要使用`float`布局。移动端使用`flex`是没有顾虑的，而`flex`布局，可以达到事半功倍的效果。\
如果不熟悉`flex`，可以参考[阮一峰的 flex 教程](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)

---

---
url: 'https://uviewpro.cn/zh/layout/comment.md'
---
# 评论




此布局包含2个页面，一个是评论列表页，另一个是点击"共xxx条回复"进去的评论详情页面，可以进行点赞。\
这两个页面，用的是本地模拟数据，不一定和用户真实的数据格式一致，请根据真实数据对页面结构，逻辑和样式进行修改。

---

---
url: 'https://uviewpro.cn/zh/resource/intro.md'
---
# 资源下载

我们会在这里为您提供一些跟 uView Pro 设计相关的资源和设计工具的下载，更多设计资源正在整理和完善中。

## 设计资源

这里我们提供组件的 Sketch 和 Axure 设计资源，您可以根据需要进行下载。

## 框架资源

这里我们提供了一些跟组件，或者框架相关的下载资源，您可以根据需求进行下载。

---

---
url: 'https://uviewpro.cn/zh/components/setting.md'
---
# 配置

uView Pro 支持 `npm` 和 `uni_modules` 两种主流安装方式，配置方式高度一致。无论采用哪种方式，均可通过 easycom 实现组件自动引入，极大提升开发效率。以下为统一的配置说明：

:::tip 提示
确保你已经安装了 uView Pro，详见安装文档：[uView Pro 安装](install.html)
:::

## 1. 引入 uView Pro 主库

在 `main.ts` 中引入并注册 uView Pro：

```js
// main.ts
import { createSSRApp } from 'vue'
// npm 方式
import uViewPro from 'uview-pro'
// uni_modules 方式
// import uViewPro from "@/uni_modules/uview-pro";

export function createApp() {
  const app = createSSRApp(App)
  app.use(uViewPro)
  return {
    app
  }
}
```

## 2. 引入全局样式

在 `uni.scss` 中引入主题样式：

```scss
/* uni.scss */
// npm 方式
@import 'uview-pro/theme.scss';
// uni_modules 方式
// @import "@/uni_modules/uview-pro/theme.scss";
```

在 `App.vue` 首行引入基础样式：

```scss
<style lang="scss">
  // npm 方式
  @import "uview-pro/index.scss";
  // uni_modules 方式
  // @import "@/uni_modules/uview-pro/index.scss";
</style>
```

## 3. 配置自动引入组件

### 基于 easycom 配置自动引入组件方案 1

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
      // npm 方式
      "^u-(.*)": "uview-pro/components/u-$1/u-$1.vue"
      // uni_modules 方式
      // "^u-(.*)": "@/uni_modules/uview-pro/components/u-$1/u-$1.vue"
    }
  },
  "pages": [
    // ...
  ]
}
```

:::tip 注意

* 1.修改 `easycom` 规则后需重启 HX 或重新编译项目。
* 2.请确保 `pages.json` 中只有一个 easycom 字段，否则请自行合并多个规则。
* 3.一定要放在 `custom` 内，否则无效。
  :::

### 基于 vite 配置自动引入组件方案 2

如果不熟悉 `easycom`，也可以通过 [@uni-helper/vite-plugin-uni-components](https://github.com/uni-helper/vite-plugin-uni-components) 实现组件的自动引入。

:::tip 提醒

* 必须使用 `@uni-helper/vite-plugin-uni-components@0.2.3` 及以上版本，因为在 0.2.3 版本开始其内置了 `uView Pro` 的 `resolver`，并支持了 `npm`、`uni_modules` 方式引入。
* 如果使用此方案时控制台打印很多 `Sourcemap for  points to missing source files​` ，可以尝试将 `Vite` 版本升级至 `4.5.x` 以上版本。

:::

::: code-group

```bash [npm]
npm i @uni-helper/vite-plugin-uni-components -D
```

```bash [yarn]
yarn add @uni-helper/vite-plugin-uni-components -D
```

```bash [pnpm]
pnpm add @uni-helper/vite-plugin-uni-components -D
```

:::

### npm 配置方式：

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

import Components from '@uni-helper/vite-plugin-uni-components'
import { uViewProResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'

export default defineConfig({
  plugins: [
    // make sure put it before `Uni()`
    Components({
      resolvers: [uViewProResolver()]
    }),
    uni()
  ]
})
```

### uni\_modules 配置方式：

::: tip 提醒
如果使用了 `@` 符，务必配置别名 `@` 到根目录！
:::

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

import Components from '@uni-helper/vite-plugin-uni-components'
import { uViewProResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'

export default defineConfig({
  plugins: [
    // make sure put it before `Uni()`
    Components({
      resolvers: [uViewProResolver('@/uni_modules/uview-pro')]
    }),
    uni()
  ]
})
```

如果你使用 `pnpm` ，请在根目录下创建一个 `.npmrc` 文件，参见 [Issue](https://github.com/antfu/unplugin-vue-components/issues/389)。

```text
// .npmrc
public-hoist-pattern[]=@vue*
// or
// shamefully-hoist = true
```

## 4. Volar 类型提示支持

如需在 CLI 项目中获得 Volar 的全局类型提示，请在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    // npm 方式
    "types": ["uview-pro/types"]
    // uni_modules 方式
    // "types": ["@/uni_modules/uview-pro/types"]
  }
}
```

> HBuilderX 项目暂不支持 tsconfig.json 的 types 配置，CLI 项目推荐配置以获得最佳 TS 体验。

## 5. 组件使用

配置完成后，无需 import 和 components 注册，可直接在 SFC 中使用 uView Pro 组件：

```vue
<template>
  <u-button type="primary">按钮</u-button>
</template>
```
