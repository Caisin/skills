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

## 5. `framework/axum/ctl/curd_trait.rs`

这里定义了 `crud_api!` 宏，能为实体快速生成：

```text
- all()
- page()
- save()
- get()
- del()
```

宏里默认依赖：

```text
- entc::Query
- entc::ModifyModel
- entc::Model
- SeaOrms::get(CODE)
```

这也是为什么它特别适合配合 kx-sea-orm 生成的 Query / ModifyModel 一起用。

对应文件：`crates/axum/src/framework/axum/ctl/curd_trait.rs`

## 6. `framework/axum/ctl/crud.rs`

这里是一个更通用的动态表 CRUD 路由样例，可帮助理解：

```text
- kx-axum 里的路由、Json、Path、QsQuery 组合方式
- 动态 page/list/save/update/del handler 怎么组织
```

对应文件：`crates/axum/src/framework/axum/ctl/crud.rs`

## 7. `framework/axum/ext/api.rs`

这里补了 Router introspection 能力：

```text
- Routers::set_router_info(app)
- RouterInfo { path, method }
```

一般不是业务接口第一入口，但在需要理解 router 聚合结果时可以回看。

对应文件：`crates/axum/src/framework/axum/ext/api.rs`

## 8. 这份 map 怎么用

### 当用户只想要 ctl/router/install 模板

优先贴 `references/patterns.md`，不要先讲源码。

### 当用户追问“R / AxumErr / QsQuery / crud_api! 是哪来的”

再补这份 map，并指出对应源码文件。

### 当用户追问 `*Qry / *ModifyModel` 的来源

切去 `kx-sea-orm` 的 `codegen-map.md`。

## 常见错误

```text
❌ 只会照抄业务侧代码，不知道 R / AxumErr / crud_api! 的来源
❌ 以为 crud_api! 自己生成 Query/ModifyModel，而不是依赖实体 codegen
❌ web 层问题和实体 codegen 问题混在一起，不区分 kx-axum 与 kx-sea-orm 的边界
```

## 正确做法

```text
✅ 先用 patterns.md 回答 web 层模板，再用这份 map 解释 kx-axum 出口
✅ 需要解释 Query / ModifyModel 来源时，直接联动 kx-sea-orm 的 codegen-map
✅ 让 web 层 skill 只关心 handler/router/install，实体与迁移模板交给 kx-sea-orm
```
