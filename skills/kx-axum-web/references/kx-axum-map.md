# KX Axum Map

用于把 `crates/axum` 暴露的 web 层能力，映射成业务侧可直接使用的入口。

## 1. `crates/axum/src/lib.rs`

关键点：

```text
- 对外统一导出 kx_axum::axum
- 导出 core::*，所以业务侧可直接用 R / AxumErr / jwt / Query 等
- 导出 framework::axum::*，所以 ext::QsQuery、Json、extract::Path 等都能从 kx_axum 入口拿到
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

## 5. `layer/log.rs`

这里定义后端无关的操作日志边界：

```text
- OperationLog：纯 HTTP 日志记录
- OperationLogProcessor：异步处理接口
- with_operation_log_processor()：为 Router 安装处理器
- run_with_log_processor()：启动时传入处理方法
```

处理方法只接收 `OperationLog`，不接收数据库连接或实体：

```rust
run_with_log_processor::<Claims, _>(app, |log: OperationLog| async move {
    send_to_log_center(log).await
}).await?;
```

数据库、消息队列、文件和远端日志服务都由下游处理器选择，`kx-axum` 不依赖指定后端。

对应文件：`crates/axum/src/layer/log.rs`

## 6. `cfg/args.rs`

这里提供启动后处理入口：

```text
- AppArgs::init_args_with(post_process)
- AppArgs::init_with_args_and(args, post_process)
```

数据库连接、模型注册、alias 和迁移通过应用后处理装配，不进入 Web crate。

对应文件：`crates/axum/src/cfg/args.rs`

## 7. `ext/api.rs`

这里补了 Router introspection 能力：

```text
- Routers::set_router_info(app)
- RouterInfo { path, method }
```

一般不是业务接口第一入口，但在需要理解 router 聚合结果时可以回看。

对应文件：`crates/axum/src/ext/api.rs`

## 8. 这份 map 怎么用

### 当用户只想要 ctl/router/install 模板

优先贴 `references/patterns.md`，不要先讲源码。

### 当用户追问“R / AxumErr / QsQuery / OperationLog 是哪来的”

再补这份 map，并指出对应源码文件。

### 当用户追问 `*Qry / *ModifyModel` 的来源

切去 `kx-sea-orm` 的 `codegen-map.md`。

## 常见错误

```text
❌ 继续引用已经删除的 crud_api! 或旧 framework 路径
❌ 把日志处理器设计成只能接收某个 ORM 的连接或实体
❌ web 层问题和实体 codegen 问题混在一起，不区分 kx-axum 与 kx-sea-orm 的边界
```

## 正确做法

```text
✅ 先用 patterns.md 回答 web 层模板，再用这份 map 解释 kx-axum 出口
✅ 需要解释 Query / ModifyModel 来源时，直接联动 kx-sea-orm 的 codegen-map
✅ 日志处理方法只接收 OperationLog，持久化后端由应用选择
✅ 让 web 层 skill 只关心 handler/router/install，实体与迁移模板交给 kx-sea-orm
```
