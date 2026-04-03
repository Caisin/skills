---
name: uni-app-core
description: |
  Use when 任务明确聚焦 uni-app 跨端框架本身，包括 API 能力、平台兼容性、Vue 2/3 差异、页面导航、存储、文件、键盘与跨端行为差异。

  触发场景：
  - 需要查询 uni-app 官方 API 的跨端兼容性
  - 需要处理 storage、navigation、keyboard、file 相关能力
  - 需要排查 H5 / App / 小程序之间的行为差异
  - 需要解释 uni-app 的跨端运行模型与使用边界

  触发词：uni-app、跨端、小程序、H5、App、navigateTo、redirectTo、storage、setStorage、keyboard、saveFile、兼容性
---

# uni-app-core

`uni-app-core` 是 uni-app 框架能力本身的专用 skill。
它聚焦官方 API、平台兼容性、运行模型与跨端差异，不负责具体 UI 组件库的细节实现。

## 适用边界

### 适用

- uni-app 官方 API 查询
- H5 / App / 小程序兼容性说明
- storage / navigation / keyboard / file 等能力说明
- Vue 2/3 在 uni-app 语境下的使用边界

### 不适用

- 具体 UI 组件库用法
  - 如是 uView-Pro，交给 `uview-pro`
- 某个具体后台管理框架脚手架
  - 如是 vue-vben-admin，交给 `vue-vben-admin`
- 纯 Vue / TS / 编译器问题
  - 交给更通用的前端或语言技能

## Reference Selection

按任务类型优先读取：

- 官方 API / 平台兼容
  - 读 `references/api.md`
- 文档导航与整体索引
  - 读 `references/index.md`
  - 补 `references/llms.md`
- 真实案例或其它信息
  - 读 `references/other.md`
  - 按需补 `references/tutorials.md`

## 核心规则

1. 优先回答“这个 API 在哪些平台可用”与“是否有差异”。
2. 优先区分异步 API、同步 API 与事件监听 API。
3. 回答时尽量明确 H5 / App / 小程序的边界，不要笼统说“都支持”。
4. 如果问题其实是在问某个 UI 组件库，不要继续停在 uni-app-core。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把 uni-app 核心 API 和具体组件库能力混在一起
❌ 只给 API 名字，不说明平台兼容边界
❌ 忽略异步/同步接口差异
```

### 正确做法

```text
✅ 先说明平台边界，再给最小示例
✅ 官方 API 优先引用 references/api.md
✅ 组件库问题及时 handoff 到对应 skill
```

## 输出模板

```text
问题归类
相关平台
推荐 API / 文档
关键兼容性说明
最小示例
下一步
```

## 完整示例

**Input**

```text
uni-app 里 setStorage 和 navigateTo 在 H5、App、小程序上有什么区别？
```

**Output direction**

```text
- 先说明这是 uni-app 核心 API 与平台兼容性问题。
- 再分别给 storage 与 navigation 的关键平台差异。
- 最后附最小示例，并提醒可能的 URL 长度或存储限制。
```
