# kx-biz-auth Patterns

用于 `kx-biz-auth` 的模块级 reference，聚焦 `kx-biz-auth` 作为“认证鉴权封装包”时，如何被其他项目复用，以及其内部主要入口与边界。

## 适用场景

- 接入统一认证路由
- 扩展权限/用户/菜单/登录能力
- 排查 auth 与 log 数据源初始化

## 先记住这几条

1. 其他项目依赖写法：`kx-biz-auth = { version = "0.1", registry = "hekx" }`。
2. 优先复用对外入口：`AuthRouter::apis()`。
3. 安装或初始化入口：`AuthInstall::migrate()`。
4. 只有现有封装不够时，再继续下钻到 crate 内部 `src/*`。

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-auth = { version = "0.1", registry = "hekx" }
```

### 最小入口

```text
- Router: AuthRouter::apis()
- Install: AuthInstall::migrate()
```

### 接入顺序

```text
1. 先引入依赖
2. 再复用 install / migrate 入口
3. 再复用 router 或 manager 入口
4. 最后按需扩展内部实现
```

---

## 回答策略

```text
- 先复用统一 auth 路由，再决定是否扩展某个认证子域。
- 安装时不要只迁移 auth，`OpLog` 也在这个 crate 里一起初始化。
- 用户/角色/菜单/权限属于不同子域，回答时不要混成一个大而全说明。
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
