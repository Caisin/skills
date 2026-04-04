# kx-biz-auth Module Map

这是 `kx-biz-auth` 的快速导航图，适合在回答前先确认“该改哪里”。

## 文件职责速查

- `kx-biz-auth/src/install.rs`
  - 迁移 `auth` 实体并在 `log` 数据源中创建 `OpLog`
- `kx-biz-auth/src/router.rs`
  - 统一聚合 app、social、per、system、user 等认证路由
- `kx-biz-auth/src/ctl/system/*`
  - 菜单、角色、用户后台接口
- `kx-biz-auth/src/ctl/per/*`
  - 权限与 API 权限接口
- `kx-biz-auth/src/ctl/user/*`
  - 用户 OAuth2 与时区接口
- `kx-biz-auth/src/svc/*`
  - 登录、权限、时区、用户业务逻辑

## 快速决策表

| 需求 | 优先改哪里 |
| --- | --- |
| 业务项目接认证路由 | `AuthRouter::apis()` |
| 初始化 auth 与 oplog | `AuthInstall::migrate()` |
| 改角色/菜单/用户后台接口 | `src/ctl/system/*` + `src/svc/*` |
| 改 OAuth2 / 社交登录 | `src/ctl/app/*` / `src/ctl/social/*` / `src/svc/login_svc.rs` |

## 回答时优先强调的事实

```text
- 该 crate 同时涉及 `auth` 数据源和 `log` 数据源。
- 对外统一入口是 `AuthRouter::apis()`。
- 路由按 app / dt / user / per / system / api_per / tz 分域。
```

## 常见错误

```text
❌ 只接了用户登录接口，却忘了统一 auth router 里还有权限和系统管理子域。
❌ 只迁移了 auth 数据源，漏掉日志表。
❌ 把参数、SDK 或资源类问题混进 auth skill。
```

## 正确做法

```text
✅ 优先复用 `AuthRouter::apis()` 与 `AuthInstall::migrate()`。
✅ 按 app/social/per/system/user 子域拆回答案。
✅ 涉及参数或 SDK 时分别 handoff 到 kx-biz-param 或 sdk-mgr。
```
