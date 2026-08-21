# KX Axum Map

用于把 `crates/axum` 暴露的 web 层能力，映射成业务侧可直接使用的入口。

## 1. `crates/axum/src/lib.rs`

关键点：

```text
- 对外统一导出 kx_axum::axum
- 导出 core::*，所以业务侧可直接用 R / AxumErr / jwt / Query 等
- 重导出 axum，所以 Json、extract::Path 等能从 kx_axum 入口拿到
- 导出 ApiRouter / ApiMeta / ApiCatalog 与注册式启动入口
```

对应文件：`crates/axum/src/lib.rs`

## 2. `core/r.rs`

业务侧最常直接用到的统一返回结构：

```text
- R<T>::ok(data)
- R::<()>::succ()
- IntoResponse 已实现，可直接作为 handler 返回体
```

所以业务接口常见写法是：

```rust
async fn list() -> Result<R<Vec<Foo>>, AxumErr> {
    Ok(ret.into())
}
```

对应文件：`crates/axum/src/core/r.rs`

## 3. `core/error.rs`

业务侧最常直接用到的统一错误类型：

```text
- AxumErr::fail(...)
- AxumErr::biz_err(...)
- AxumErr::with_http_status(...)
- IntoResponse 已实现
```

所以 handler 可以直接：

```rust
Err(AxumErr::fail("参数错误"))?
```

对应文件：`crates/axum/src/core/error.rs`

## 4. `core/query.rs`

这里直接导出：

```text
- serde_qs::axum::QsQuery
```

这就是为什么业务侧分页接口常见写法是：

```rust
async fn page(
    QsQuery(req): QsQuery<FooQry>,
    QsQuery(page): QsQuery<Paging>,
) -> Result<R<Page<Foo>>, AxumErr>
```

对应文件：`crates/axum/src/core/query.rs`

## 5. `api_router.rs`

这里定义注册式路由和安全策略：

```text
- ApiRouter：同时构造 Axum Router 和 API catalog
- ApiMeta：声明稳定 code、备注、访问策略和 KxEd 策略
- RegisteredRouter：finish 校验后的启动输入
- ApiAuthorizer / ApiRuntime：注入权限校验、ingress 和调试选项
```

普通接口默认只需要：

```rust
ApiRouter::new().get(
    "/users",
    UserCtl::page,
    ApiMeta::new("user.page", "用户分页"),
)
```

默认策略是 `Protected + Required`。`.public()`、`.auth_only()`、`.plaintext()` 和
`.external_callback()` 只用于明确的例外，不能由 TOML 覆盖注册式策略。

对应文件：`crates/axum/src/api_router.rs`

## 6. `layer/jwt` 与 `layer/security`

注册式策略中间件复用这里的 JWT 和 KxEd 单步能力：

```text
- ExternalAuthenticated 先执行 ingress
- Required 再解密请求
- Authenticated / Protected 再执行 JWT
- Protected 最后调用 ApiAuthorizer
- Required 对 handler 和认证授权错误响应统一加密
```

对应文件：`crates/axum/src/layer/jwt/mid.rs`、`crates/axum/src/layer/security/mod.rs`

## 7. `ext/api.rs`

这里补了 Router introspection 能力：

```text
- Routers::set_router_info(app)
- RouterInfo { path, method }
```

一般不是业务接口第一入口，但在需要理解 router 聚合结果时可以回看。
注册式应用以 `ApiCatalog` 为事实源，不依赖该 Debug 扫描结果。

对应文件：`crates/axum/src/ext/api.rs`

## 8. 这份 map 怎么用

### 当用户只想要 ctl/router/install 模板

优先贴 `references/patterns.md`，不要先讲源码。

### 当用户追问“R / AxumErr / QsQuery / ApiRouter 是哪来的”

再补这份 map，并指出对应源码文件。

### 当用户追问 `*Qry / *ModifyModel` 的来源

切去 `kx-sea-orm` 的 `codegen-map.md`。

## 常见错误

```text
❌ 返回原生 Router，再分别维护 TOML 白名单和权限 API 表
❌ 把 ApiCatalog 当成数据库实体，让 kx-axum 依赖 ORM
❌ web 层问题和实体 codegen 问题混在一起，不区分 kx-axum 与 kx-sea-orm 的边界
```

## 正确做法

```text
✅ 先用 patterns.md 回答 web 层模板，再用这份 map 解释 kx-axum 出口
✅ 需要解释 Query / ModifyModel 来源时，直接联动 kx-sea-orm 的 codegen-map
✅ 新业务路由使用 ApiRouter + ApiMeta，并在聚合完成后调用 finish
✅ 让 web 层 skill 只关心 handler/router/install，实体与迁移模板交给 kx-sea-orm
```
