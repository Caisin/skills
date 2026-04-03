---
name: uview-pro
description: |
  Use when 任务明确聚焦 uView-Pro 组件库本身，包括组件用法、表单/反馈/布局组件、工具函数、ConfigProvider 与 uni-app 场景下的组件实践。

  触发场景：
  - 需要使用 uView-Pro 组件，如 ActionSheet、Collapse、Waterfall、Badge、Avatar
  - 需要使用 uView-Pro 工具函数与全局 `$u`
  - 需要配置样式、主题或组件行为
  - 需要排查 uView-Pro 组件在 uni-app 中的用法问题

  触发词：uview-pro、uview、ActionSheet、Collapse、Waterfall、Badge、Avatar、$u、ConfigProvider、uni-app 组件库
---

# uview-pro

`uview-pro` 是 uView-Pro 组件库专用 skill。
它负责组件 API、示例代码、工具函数与组件实践，不负责 uni-app 核心 API 的跨端兼容性总览。

## 适用边界

### 适用

- uView-Pro 组件使用
- `$u` 工具函数
- ConfigProvider / 主题配置
- uni-app 场景下的组件示例

### 不适用

- uni-app 核心 API 兼容性问题
  - 交给 `uni-app-core`
- 具体后台管理框架模板
  - 交给 `vue-vben-admin`

## Reference Selection

按任务类型优先读取：

- 组件索引与总览
  - 读 `references/index.md`
- 中文资料与详细说明
  - 读 `references/zh.md`
- LLM 摘要或扩展资料
  - 读 `references/llms.md`
  - 按需补 `references/llms-full.md`

## 核心规则

1. 先明确用户问的是哪个组件或哪类组件。
2. 优先给最小可运行示例，不先铺很多背景。
3. 涉及 `$u` 工具函数时，要明确 script 与 template 的调用方式差异。
4. 如果问题回到 uni-app 核心 API，本 skill 只做 handoff，不重复解释。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把 uView-Pro 组件问题当成 uni-app 核心 API 问题
❌ 只列组件名，不给最小示例
❌ 忽略 script/template 下 `$u` 的调用差异
```

### 正确做法

```text
✅ 先锁定具体组件或工具函数
✅ 优先给最小示例和关键参数
✅ 涉及 uni-app 核心边界时 handoff 到 uni-app-core
```

## 输出模板

```text
问题归类
目标组件 / 工具
最小示例
关键参数 / 注意点
相关参考
下一步
```

## 完整示例

**Input**

```text
给我一个 uView-Pro 的 ActionSheet 示例，顺便告诉我怎么处理点击事件。
```

**Output direction**

```text
- 先明确这是组件库问题。
- 给最小可运行 ActionSheet 示例。
- 再补点击事件处理和关键参数。
```
