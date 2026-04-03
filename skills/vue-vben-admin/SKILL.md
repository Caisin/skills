---
name: vue-vben-admin
description: |
  Use when 任务明确聚焦 vue-vben-admin v5，包括页面开发、路由配置、VbenForm / VxeTable / VbenModal 等框架组件、请求层、权限与 Monorepo 架构。

  触发场景：
  - 需要在 vue-vben-admin 项目中开发新页面、组件或功能
  - 需要配置路由、菜单、权限控制
  - 需要使用 VbenForm、VxeTable、VbenModal、VbenDrawer 等组件
  - 需要配置请求客户端、API 模块或理解框架架构

  触发词：vue-vben-admin、vben、VbenForm、VxeTable、VbenModal、VbenDrawer、路由、权限、monorepo、request、后台管理框架
---

# vue-vben-admin

`vue-vben-admin` 是 Vue Vben Admin v5 的专用 skill。
它聚焦该框架的架构、页面模板、组件使用、请求层与路由权限，不覆盖一般性的 uni-app 或组件库问题。

## 适用边界

### 适用

- vue-vben-admin 页面开发
- 路由与权限配置
- Vben 组件使用
- RequestClient / API 组织
- Monorepo 与适配器结构理解

### 不适用

- uni-app 跨端框架问题
  - 交给 `uni-app-core`
- uView-Pro 组件库问题
  - 交给 `uview-pro`

## Reference Selection

按任务类型优先读取：

- 整体架构
  - 读 `references/architecture.md`
- 路由与权限
  - 读 `references/routing.md`
- 组件使用
  - 读 `references/components.md`
- 请求与 API
  - 读 `references/request.md`

## 核心规则

1. 先判断用户是在问架构、路由、组件还是请求层。
2. 页面示例优先给最小 CRUD 模板，不先铺很长背景。
3. 涉及权限或动态路由时，要明确是前端路由还是后端返回路由。
4. 如果问题不在 vue-vben-admin 边界，不要强行套这个框架。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 不区分架构、路由、组件、请求层问题
❌ 只贴大段框架介绍，不给最小页面模板
❌ 把普通 Vue 问题强行解释成 Vben 特有问题
```

### 正确做法

```text
✅ 先锁定问题层次，再选对应 reference
✅ 页面开发优先给最小 CRUD 页面模板
✅ 权限问题显式说明是前端还是后端路由模式
```

## 输出模板

```text
问题归类
相关模块
最小模板 / 关键配置
注意点
参考文档
下一步
```

## 完整示例

**Input**

```text
给我一个 vue-vben-admin 的页面模板，包含表格、弹窗编辑和接口请求。
```

**Output direction**

```text
- 先明确这是框架页面开发问题。
- 给最小 CRUD 页面模板。
- 再补表格、弹窗和请求层的落点。
```
