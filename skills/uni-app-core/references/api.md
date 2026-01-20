# Uni-App-Core - Api

**Pages:** 27

---

## uni.hideKeyboard() | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/key#offkeyboardheightchange.md

**Contents:**
- # uni.hideKeyboard()
  - # hideKeyboard 兼容性
- # uni.onKeyboardHeightChange(CALLBACK)
- # uni.offKeyboardHeightChange(CALLBACK)
- # uni.getSelectedTextRange(OBJECT)

隐藏已经显示的软键盘，如果软键盘没有显示则不做任何操作。

示例源码如下，请查看 pre > code 标签中的内容

onKeyboardHeightChange 传入的监听函数。不传此参数则移除所有监听函数。

示例源码如下，请查看 pre > code 标签中的内容

在input、textarea等focus之后，获取输入框的光标位置。注意：只有在focus的时候调用此接口才有效。目前仅支持 vue 页面，nvue 可以直接使用 weex 的 getSelectionRange 。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 2 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 3 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 4 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#getstorageinfosync.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#setstorage.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#setstoragesync.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#getfileinfo.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#getsavedfileinfo.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#clearstoragesync.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#removestorage.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#removestoragesync.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#animation.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#getstorage.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#event-channel.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#clearstorage.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.hideKeyboard() | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/key#getselectedtextrange.md

**Contents:**
- # uni.hideKeyboard()
  - # hideKeyboard 兼容性
- # uni.onKeyboardHeightChange(CALLBACK)
- # uni.offKeyboardHeightChange(CALLBACK)
- # uni.getSelectedTextRange(OBJECT)

隐藏已经显示的软键盘，如果软键盘没有显示则不做任何操作。

示例源码如下，请查看 pre > code 标签中的内容

onKeyboardHeightChange 传入的监听函数。不传此参数则移除所有监听函数。

示例源码如下，请查看 pre > code 标签中的内容

在input、textarea等focus之后，获取输入框的光标位置。注意：只有在focus的时候调用此接口才有效。目前仅支持 vue 页面，nvue 可以直接使用 weex 的 getSelectionRange 。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 2 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 3 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 4 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#opendocument.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.hideKeyboard() | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/key#hidekeyboard.md

**Contents:**
- # uni.hideKeyboard()
  - # hideKeyboard 兼容性
- # uni.onKeyboardHeightChange(CALLBACK)
- # uni.offKeyboardHeightChange(CALLBACK)
- # uni.getSelectedTextRange(OBJECT)

隐藏已经显示的软键盘，如果软键盘没有显示则不做任何操作。

示例源码如下，请查看 pre > code 标签中的内容

onKeyboardHeightChange 传入的监听函数。不传此参数则移除所有监听函数。

示例源码如下，请查看 pre > code 标签中的内容

在input、textarea等focus之后，获取输入框的光标位置。注意：只有在focus的时候调用此接口才有效。目前仅支持 vue 页面，nvue 可以直接使用 weex 的 getSelectionRange 。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 2 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 3 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 4 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#getsavedfilelist.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#navigateback.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#savefile.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#redirectto.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#getstoragesync.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#switchtab.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.hideKeyboard() | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/key#onkeyboardheightchange.md

**Contents:**
- # uni.hideKeyboard()
  - # hideKeyboard 兼容性
- # uni.onKeyboardHeightChange(CALLBACK)
- # uni.offKeyboardHeightChange(CALLBACK)
- # uni.getSelectedTextRange(OBJECT)

隐藏已经显示的软键盘，如果软键盘没有显示则不做任何操作。

示例源码如下，请查看 pre > code 标签中的内容

onKeyboardHeightChange 传入的监听函数。不传此参数则移除所有监听函数。

示例源码如下，请查看 pre > code 标签中的内容

在input、textarea等focus之后，获取输入框的光标位置。注意：只有在focus的时候调用此接口才有效。目前仅支持 vue 页面，nvue 可以直接使用 weex 的 getSelectionRange 。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 2 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 3 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

Example 4 (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#navigateto.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---

## uni.saveFile(OBJECT) @savefile | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/file/file#removesavedfile.md

**Contents:**
- # uni.saveFile(OBJECT)
  - # saveFile 兼容性
- # uni.getSavedFileList(OBJECT)
  - # getSavedFileList 兼容性
- # uni.getSavedFileInfo(OBJECT)
  - # getSavedFileInfo 兼容性
- # uni.removeSavedFile(OBJECT)
  - # removeSavedFile 兼容性
- # uni.getFileInfo(OBJECT)
  - # getFileInfo 兼容性

注意：saveFile 会把临时文件移动，因此调用成功后传入的 tempFilePath 将不可用

微信小程序已停止维护wx.saveFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getSavedFileList(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

获取本地文件的文件信息。此接口只能用于获取已保存到本地的文件。

微信小程序已停止维护wx.getSavedFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.removeSavedFile(Object object) 接口，建议使用FileSystemManager 对象中的方法。

示例源码如下，请查看 pre > code 标签中的内容

微信小程序已停止维护wx.getFileInfo(Object object) 接口，建议使用FileSystemManager 对象中的方法。

新开页面打开文档，支持格式：doc, xls, ppt, pdf, docx, xlsx, pptx。

示例源码如下，请查看 pre > code 标签中的内容

**Examples:**

Example 1 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 2 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 3 (gdscript):
```gdscript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

Example 4 (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
      }
    });
  }
});
```

---

## uni.setStorage(OBJECT) @setstorage | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/storage/storage#getstorageinfo.md

**Contents:**
- # uni.setStorage(OBJECT)
  - # setStorage 兼容性
- # uni.setStorageSync(KEY,DATA)
- # uni.getStorage(OBJECT)
  - # getStorage 兼容性
- # uni.getStorageSync(KEY)
  - # getStorageSync 兼容性
- # uni.getStorageInfo(OBJECT)
  - # getStorageInfo 兼容性
- # uni.getStorageInfoSync()

将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个异步接口。

示例源码如下，请查看 pre > code 标签中的内容

将 data 存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容，这是一个同步接口。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中异步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

从本地缓存中同步获取指定 key 对应的内容。

示例源码如下，请查看 pre > code 标签中的内容

异步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

同步获取当前 storage 的相关信息。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

uni-app的Storage在不同端的实现不同：

**Examples:**

Example 1 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 2 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 3 (css):
```css
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

Example 4 (javascript):
```javascript
uni.setStorage({
	key: 'storage_key',
	data: 'hello',
	success: function () {
		console.log('success');
	}
});
```

---

## uni.navigateTo(OBJECT) | uni-app官网

**URL:** https://uniapp.dcloud.net.cn/api/router#relaunch.md

**Contents:**
- # uni.navigateTo(OBJECT)
  - # navigateTo 兼容性
- # uni.redirectTo(OBJECT)
  - # redirectTo 兼容性
- # uni.reLaunch(OBJECT)
  - # reLaunch 兼容性
- # uni.switchTab(OBJECT)
  - # switchTab 兼容性
- # uni.navigateBack(OBJECT)
  - # navigateBack 兼容性

保留当前页面，跳转到应用内的某个页面，使用uni.navigateBack可以返回到原页面。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

vue3 script setup 语法糖中调用 getOpenerEventChannel 示例：

示例源码如下，请查看 pre > code 标签中的内容

url有长度限制，太长的字符串会传递失败，可改用窗体通信 、全局变量 ，另外参数中出现空格等特殊字符时需要对参数进行编码，如下为使用encodeURIComponent对参数进行编码的示例。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面。

注意： 如果调用了 uni.preloadPage(OBJECT) 不会关闭，仅触发生命周期 onHide

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层。

示例源码如下，请查看 pre > code 标签中的内容

string eventName 事件名称

取消监听一个事件。给出第二个参数时，只取消给出的监听函数，否则取消所有监听函数

string eventName 事件名称

string eventName 事件名称

string eventName 事件名称

本API仅App支持。小程序自身不支持自定义动画。H5的窗体动画可使用常规单页动画处理方案，见H5下单页动画示例

窗口的显示/关闭动画效果，支持在 API、组件、pages.json 中配置，优先级为：API = 组件 > pages.json。

示例源码如下，请查看 pre > code 标签中的内容

示例源码如下，请查看 pre > code 标签中的内容

pages.json 中配置的是窗口显示的动画

示例源码如下，请查看 pre > code 标签中的内容

显示动画与关闭动画，会有默认的对应规则。但是如果通过 API 或组件配置了窗口关闭的动画类型，则不会使用默认的类型。

**Examples:**

Example 1 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 2 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 3 (css):
```css
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

Example 4 (javascript):
```javascript
//在起始页面跳转到test.vue页面并传递参数
uni.navigateTo({
	url: 'test?id=1&name=uniapp'
});
```

---
