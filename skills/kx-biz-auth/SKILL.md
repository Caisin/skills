---
name: kx-biz-auth
description: |
  Use when 在 `kx-rs` 框架里需要接入、复用或扩展 `kx-biz-auth` 这个认证鉴权封装包，统一提供认证、登录、权限、菜单、角色、用户、OAuth2 与社交登录相关路由和安装能力。

  触发场景：
  - 在业务项目里接入统一认证鉴权路由
  - 需要复用 `AuthRouter::apis()`
  - 需要执行认证库与操作日志的初始化 `AuthInstall::migrate()`
  - 需要扩展 app/social/per/system/user 等认证子域

  触发词：kx-biz-auth、认证、鉴权、AuthRouter、AuthInstall、oauth2、角色、菜单、权限、用户管理、钉钉登录
---

# kx-biz-auth

`kx-biz-auth` 是当前仓库里专门面向 `kx-biz-auth` crate 的 repo-local skill。
它的首要定位不是教你从零重写这类业务，而是帮助你优先把 `kx-biz-auth` 当成**可被其他项目直接复用的封装包**来使用。

## 适用边界

### 适用

- 接入统一认证路由
- 扩展权限/用户/菜单/登录能力
- 排查 auth 与 log 数据源初始化

### 不适用

- 参数配置封装
- 资源内容路由
- 通用 SDK 封装实现

## Reference Selection

按任务类型优先读取：

- 想知道怎么在其他项目里接入 `kx-biz-auth`
  - 先读 `references/patterns.md`
- 想知道 `kx-biz-auth` 的模块边界、入口文件、路由或安装点
  - 读 `references/module-map.md`
- 如果问题已经下钻到通用 web 层写法
  - 切 `kx-axum-web`
- 如果问题已经下钻到实体、迁移、derive(Sea) 模板
  - 切 `kx-sea-orm`

## 其他项目接入示例

```toml
[dependencies]
kx-biz-auth = { version = "0.1", registry = "hekx" }
```

最常用入口：

```text
- Router: AuthRouter::apis()
- Install: AuthInstall::migrate()
```

## 回答时优先强调的事实

- 该 crate 同时涉及 `auth` 数据源和 `log` 数据源。
- 对外统一入口是 `AuthRouter::apis()`。
- 路由按 app / dt / user / per / system / api_per / tz 分域。

## 最常用的落地套路

```text
- 先复用统一 auth 路由，再决定是否扩展某个认证子域。
- 安装时不要只迁移 auth，`OpLog` 也在这个 crate 里一起初始化。
- 用户/角色/菜单/权限属于不同子域，回答时不要混成一个大而全说明。
```

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只接了用户登录接口，却忘了统一 auth router 里还有权限和系统管理子域。
❌ 只迁移了 auth 数据源，漏掉日志表。
❌ 把参数、SDK 或资源类问题混进 auth skill。
```

### 正确做法

```text
✅ 优先复用 `AuthRouter::apis()` 与 `AuthInstall::migrate()`。
✅ 按 app/social/per/system/user 子域拆回答案。
✅ 涉及参数或 SDK 时分别 handoff 到 kx-biz-param 或 sdk-mgr。
```

## 输出模板

```text
问题归类
推荐落点
关键约定
实现顺序
验证方式
下一步
```

## 完整示例

**Input**

```text
我在一个项目里想直接接用户登录、菜单角色、权限管理这些接口，不想自己散着挂，应该怎么接？
```

**Output direction**

```text
应命中 kx-biz-auth，并优先建议复用 `AuthRouter::apis()`。
```
