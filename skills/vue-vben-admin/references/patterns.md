# Vue Vben Admin Patterns

用于 `vue-vben-admin` 的页面开发、路由权限与请求层问题。

## 适用场景

- 页面 CRUD 模板
- 路由 / 菜单 / 权限配置
- RequestClient / API 模块组织

## 推荐做法

```text
先判断是架构、路由、组件还是请求层
-> 给最小模板
-> 再补关键配置
```

## 常见错误

```text
❌ 只讲架构，不给页面最小模板
❌ 不区分前端权限路由与后端权限路由
```

## 正确做法

```text
✅ 页面类问题优先给最小 CRUD 模板
✅ 路由权限问题显式区分模式
✅ 请求层问题直接指向 references/request.md
```
