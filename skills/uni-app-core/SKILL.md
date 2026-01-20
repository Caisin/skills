---
name: uni-app-core
description: Deep understanding of uni-app cross-platform framework, including Vue 2/3 compatibility, compiler logic, and platform-specific APIs.
---

# Uni-App-Core Skill

Comprehensive knowledge of uni-app cross-platform framework, generated from official documentation. This skill covers APIs for storage, navigation, keyboard handling, file operations, and more across multiple platforms (H5, App, WeChat Mini Program, etc.).

## When to Use This Skill

This skill should be triggered when:
- **Building cross-platform applications** with uni-app (H5, iOS, Android, Mini Programs)
- **Implementing local storage** functionality (async/sync storage operations)
- **Handling page navigation** and routing (navigateTo, redirectTo, switchTab, etc.)
- **Managing keyboard interactions** (height changes, hiding keyboard, cursor position)
- **Working with file operations** (saving, reading, removing files)
- **Debugging platform-specific** API compatibility issues
- **Migrating from WeChat Mini Program** to uni-app
- **Understanding Vue 2/3 compatibility** in uni-app context

## Key Concepts

### Cross-Platform Architecture
uni-app uses a unified API that compiles to different platforms:
- **H5**: Web browser environment
- **App**: Native iOS/Android via custom runtime
- **Mini Programs**: WeChat, Alipay, Baidu, etc.
- **HarmonyOS**: Native HarmonyOS applications

### API Patterns
Most uni-app APIs follow these patterns:
- **Async APIs**: Accept an object with `success`, `fail`, `complete` callbacks
- **Sync APIs**: Suffix with `Sync`, return values directly
- **Event Listeners**: `on*` to register, `off*` to unregister

### Storage Implementation
Storage varies by platform:
- **H5**: localStorage
- **App**: Native file system
- **Mini Programs**: Platform-specific storage APIs

## Quick Reference

### Storage Operations

**Async Storage - Set Data** (javascript):
```javascript
uni.setStorage({
  key: 'storage_key',
  data: 'hello',
  success: function () {
    console.log('success');
  }
});
```

**Sync Storage - Set Data** (javascript):
```javascript
try {
  uni.setStorageSync('storage_key', 'hello');
} catch (e) {
  console.error(e);
}
```

**Async Storage - Get Data** (javascript):
```javascript
uni.getStorage({
  key: 'storage_key',
  success: function (res) {
    console.log(res.data);
  }
});
```

**Sync Storage - Get Data** (javascript):
```javascript
try {
  const value = uni.getStorageSync('storage_key');
  if (value) {
    console.log(value);
  }
} catch (e) {
  console.error(e);
}
```

### Navigation & Routing

**Navigate to Page with Parameters** (javascript):
```javascript
// Navigate to test.vue page and pass parameters
uni.navigateTo({
  url: 'test?id=1&name=uniapp'
});
```

**Redirect to Page** (javascript):
```javascript
// Close current page and redirect
uni.redirectTo({
  url: 'test?id=1'
});
```

**Navigate Back** (javascript):
```javascript
// Go back one page
uni.navigateBack({
  delta: 1
});
```

**Switch to Tab Page** (javascript):
```javascript
// Jump to tabBar page
uni.switchTab({
  url: '/pages/index/index'
});
```

### Keyboard Handling

**Monitor Keyboard Height Changes** (javascript):
```javascript
uni.onKeyboardHeightChange(res => {
  console.log(res.height)
})
```

**Hide Keyboard** (javascript):
```javascript
uni.hideKeyboard();
```

**Remove Keyboard Listener** (javascript):
```javascript
const callback = (res) => {
  console.log(res.height);
};

// Register listener
uni.onKeyboardHeightChange(callback);

// Remove specific listener
uni.offKeyboardHeightChange(callback);

// Remove all listeners
uni.offKeyboardHeightChange();
```

### File Operations

**Save File from Temp Path** (javascript):
```javascript
uni.chooseImage({
  success: function (res) {
    var tempFilePaths = res.tempFilePaths;
    uni.saveFile({
      tempFilePath: tempFilePaths[0],
      success: function (res) {
        var savedFilePath = res.savedFilePath;
        console.log('File saved:', savedFilePath);
      }
    });
  }
});
```

**Get Saved File Info** (javascript):
```javascript
uni.getSavedFileInfo({
  filePath: savedFilePath,
  success: function (res) {
    console.log('File size:', res.size);
    console.log('Create time:', res.createTime);
  }
});
```

**Remove Saved File** (javascript):
```javascript
uni.removeSavedFile({
  filePath: savedFilePath,
  success: function (res) {
    console.log('File removed');
  }
});
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### api.md (27 pages)
**Source:** Official uni-app documentation
**Confidence:** Medium
**Content:** Complete API reference covering:
- **Storage APIs**: setStorage, getStorage, removeStorage, clearStorage (async/sync variants)
- **Navigation APIs**: navigateTo, redirectTo, reLaunch, switchTab, navigateBack
- **Keyboard APIs**: hideKeyboard, onKeyboardHeightChange, getSelectedTextRange
- **File APIs**: saveFile, getSavedFileList, getSavedFileInfo, removeSavedFile, getFileInfo
- **Compatibility tables** for each API across platforms

### other.md (1 page)
**Source:** Official uni-app case studies
**Confidence:** Medium
**Content:** Real-world applications built with uni-app:
- Official examples (Hello uni-app)
- Enterprise cases (Huawei, CSDN, vivo)
- HarmonyOS applications
- Government and financial sector apps

### llms.md
**Source:** Official documentation index
**Confidence:** Medium
**Content:** Complete documentation structure and navigation links

### index.md
**Source:** Documentation index
**Confidence:** Medium
**Content:** Category overview and file organization

## Working with This Skill

### For Beginners
1. **Start with storage APIs** - They're simple and demonstrate the async/sync pattern
2. **Learn navigation basics** - Understanding page routing is fundamental
3. **Review compatibility tables** - Each API has platform-specific support
4. **Check the official examples** - Hello uni-app demonstrates all core features

### For Intermediate Users
1. **Master event channels** - For complex page-to-page communication
2. **Understand lifecycle hooks** - onLoad, onShow, onHide, etc.
3. **Handle platform differences** - Use conditional compilation when needed
4. **Optimize storage usage** - Be aware of size limits on different platforms

### For Advanced Users
1. **Leverage FileSystemManager** - For complex file operations (WeChat deprecated old APIs)
2. **Implement custom animations** - App platform supports custom window animations
3. **Use EventChannel** - For advanced page communication patterns
4. **Handle edge cases** - URL length limits, special character encoding, etc.

## Platform Compatibility Notes

### Storage APIs
- **H5**: Uses localStorage (5-10MB limit)
- **App**: Native file system (no practical limit)
- **Mini Programs**: Platform-specific limits (usually 10MB)
- **Note**: Data is NOT shared between platforms

### Navigation APIs
- **navigateTo**: Max 10 pages in stack (Mini Programs), unlimited (App)
- **Animation**: Only supported on App platform
- **URL length**: Limited, use EventChannel for large data
- **Special characters**: Must use encodeURIComponent

### Keyboard APIs
- **getSelectedTextRange**: Vue pages only (nvue use weex's getSelectionRange)
- **onKeyboardHeightChange**: Not supported on all platforms

### File APIs
- **WeChat Mini Program**: Many file APIs deprecated, use FileSystemManager instead
- **saveFile**: Moves temp file (original path becomes invalid)
- **openDocument**: Supports doc, xls, ppt, pdf, docx, xlsx, pptx

## Best Practices

### Storage
1. **Always handle errors** - Use try-catch with sync APIs
2. **Don't store sensitive data** - Storage is not encrypted
3. **Clean up unused data** - Use removeStorage or clearStorage
4. **Check storage info** - Monitor usage with getStorageInfo

### Navigation
1. **Encode URL parameters** - Use encodeURIComponent for special characters
2. **Use EventChannel** - For passing complex data between pages
3. **Manage page stack** - Be aware of navigateTo stack limits
4. **Handle navigation failures** - Always provide fail callbacks

### Keyboard
1. **Remove listeners** - Call offKeyboardHeightChange when done
2. **Check focus state** - getSelectedTextRange only works when focused
3. **Handle platform differences** - Test keyboard behavior on each platform

### Files
1. **Use FileSystemManager** - For WeChat Mini Program (new API)
2. **Handle temp files** - saveFile moves the file, original path invalid
3. **Check file size** - Use getFileInfo before operations
4. **Clean up saved files** - Remove files when no longer needed

## Common Patterns

### Persistent User Preferences
```javascript
// Save user settings
const saveSettings = (settings) => {
  uni.setStorageSync('userSettings', JSON.stringify(settings));
};

// Load user settings
const loadSettings = () => {
  try {
    const data = uni.getStorageSync('userSettings');
    return data ? JSON.parse(data) : {};
  } catch (e) {
    return {};
  }
};
```

### Page Communication with EventChannel
```javascript
// Page A: Open page B with event channel
uni.navigateTo({
  url: '/pages/test/test',
  success: function(res) {
    res.eventChannel.emit('acceptDataFromOpenerPage', { data: 'test' });
  }
});

// Page B: Receive data from page A
const eventChannel = this.getOpenerEventChannel();
eventChannel.on('acceptDataFromOpenerPage', function(data) {
  console.log(data);
});
```

### Responsive Keyboard Handling
```javascript
// Adjust UI when keyboard appears
uni.onKeyboardHeightChange(res => {
  this.keyboardHeight = res.height;
  // Adjust bottom padding or scroll position
});

// Clean up on page unload
onUnload() {
  uni.offKeyboardHeightChange();
}
```

## Migration Notes

### From WeChat Mini Program
- Replace `wx.*` with `uni.*`
- Use FileSystemManager for file operations (old APIs deprecated)
- Check compatibility tables for platform differences
- Test on all target platforms

### From Vue.js Web App
- Use uni-app APIs instead of browser APIs
- Handle platform-specific features with conditional compilation
- Be aware of storage implementation differences
- Test navigation behavior (different from vue-router)

## Resources

### Official Documentation
- Main site: https://uniapp.dcloud.net.cn/
- API reference: https://uniapp.dcloud.net.cn/api/
- Component reference: https://uniapp.dcloud.net.cn/component/

### Reference Files
All reference files contain:
- Detailed API explanations
- Code examples with language annotations
- Links to original documentation
- Compatibility tables
- Platform-specific notes

### Example Projects
- **Hello uni-app**: Official demo showcasing all features
- **DCloud App**: Real-world app using uni-im
- **ColorUI**: High-quality UI component library

## Notes

- This skill was automatically generated from official uni-app documentation
- Reference files preserve structure and examples from source docs
- Code examples include proper language detection for syntax highlighting
- Compatibility information is based on official documentation
- Some APIs may be deprecated on specific platforms (especially WeChat Mini Program)

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Check for API deprecations and new features
4. Update compatibility tables as platforms evolve
