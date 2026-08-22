# Write Ctl Patterns

## Thin Controller

```rust
use kx_axum::{
    ApiMeta, ApiRouter, AxumErr, R,
    axum::{Json, extract::Path},
    ext::QsQuery,
};
use kx_sea_common::Paging;

pub struct ItemCtl;

impl ItemCtl {
    pub fn apis() -> ApiRouter {
        ApiRouter::new()
            .get("/", Self::page, ApiMeta::new("item.page", "项目分页"))
            .get("/{id}", Self::detail, ApiMeta::new("item.detail", "项目详情"))
            .post("/", Self::save, ApiMeta::new("item.save", "保存项目"))
            .delete("/{id}", Self::delete, ApiMeta::new("item.delete", "删除项目"))
    }

    pub async fn page(
        QsQuery(req): QsQuery<ItemQuery>,
        QsQuery(page): QsQuery<Paging>,
    ) -> Result<R<ItemPage>, AxumErr> {
        Ok(ItemSvc::page(req, page).await?.into())
    }

    pub async fn detail(Path(id): Path<i64>) -> Result<R<ItemView>, AxumErr> {
        Ok(ItemSvc::detail(id).await?.into())
    }

    pub async fn save(Json(req): Json<ItemWrite>) -> Result<R<ItemView>, AxumErr> {
        Ok(ItemSvc::save(req).await?.into())
    }

    pub async fn delete(Path(id): Path<i64>) -> Result<R<bool>, AxumErr> {
        Ok(ItemSvc::delete(id).await?.into())
    }
}
```

handler 中不直接访问 `SeaOrms`、不 begin transaction、不逐表写入。

分页条件与分页参数必须分离：`ItemQuery` 只定义业务过滤条件，`Paging` 统一承载
`page/page_size/pageSize/size`。不要在每个查询 DTO 中重复定义分页字段或 `paging()`。两个
`QsQuery` 会分别解析完整 query string，因此分页查询 DTO 不要标记
`#[serde(deny_unknown_fields)]`，否则业务条件 extractor 会拒绝分页字段。

## Generated Entity Query

`model_attrs(derive(Sea))` 已生成 `<TableName>Qry`，包含可序列化字段条件和规范链式方法。单表后台管理
接口在确认所有字段都允许成为筛选条件后，可以直接提取：

```rust
pub async fn page(
    QsQuery(query): QsQuery<MsgEvtQry>,
    QsQuery(page): QsQuery<Paging>,
) -> Result<R<Page<MsgEvt>>, AxumErr> {
    Ok(MsgEvtSvc::page(query, page).await?.into())
}
```

接口需要 `keyword`、跨表条件、字段别名，或必须隐藏 tenant/version/token 等内部字段时，保留专用协议
Query DTO，并在 svc 中映射到 `MsgEvt::qry()` / `MsgEvt::sel()`。不要在 ctl/dto 中复制 entity 的
`_eq/_gte/_in/update_set` 等生成器。

## Router Aggregation

```rust
pub struct ItemRouter;

impl ItemRouter {
    pub fn apis() -> ApiRouter {
        ApiRouter::new().nest("/items", ItemCtl::apis())
    }

    pub fn registered() -> anyhow::Result<RegisteredRouter> {
        Self::apis().finish()
    }
}
```

聚合应用只在最终路由树上调用一次 `finish()`，让 method/path/API code 冲突在启动时失败。

## Security Policy

```text
默认业务接口     -> Protected + Required
登录/公开读取    -> 显式 public
仅要求登录       -> 显式 auth_only
允许明文         -> 显式 plaintext
第三方回调       -> external_callback + ingress + plaintext
```

公开不等于自动明文，也不等于跳过 ingress。不存在 authorizer、存在未知 API code 或验证出错时保持 fail-closed。

## DTO Boundary

- 写入 DTO 只包含调用方允许提交的字段。
- 响应 View 不返回密码哈希、token、credential 密文、内部 claim token 或 provider secret。
- `entity::Model` 只在确认所有字段都可公开时直接返回；默认显式映射为 View。
- 分页 query、write request、detail view 分开定义，避免一个 DTO 同时承担多种协议语义。
- 分页 handler 使用两个 `QsQuery`：一个提取业务查询条件，一个提取 `Paging`。

## Directory Boundary

```text
src/dto/<subdomain>.rs -> HTTP 输入输出结构
src/ctl/<subdomain>.rs -> extractor、svc 调用、统一响应
src/router.rs           -> 跨功能路由聚合与 finish
src/ctl/mod.rs          -> 模块声明和稳定重导出
```

## 常见错误

```text
❌ handler 直接访问 SeaOrms 或开启事务
❌ 请求 DTO 复用完整 entity，允许调用方写内部字段
❌ 使用 Axum 原生 `Query` 解析复杂查询，或把 `page/page_size/size` 重复塞进业务查询 DTO
❌ 已有 `<TableName>Qry` 时再复制同字段、同语义的 Query DTO
❌ 使用 Axum 0.7 的 /:id 路径语法
❌ 第三方回调只标 public，没有 ingress 和 plaintext 策略
```

## 正确做法

```text
✅ handler 只提取参数、调用 svc 和转换响应
✅ 请求与响应使用最小 DTO/View
✅ 分页使用 `QsQuery(req): QsQuery<XxxQuery>` 和 `QsQuery(page): QsQuery<Paging>`
✅ 路径参数使用 Axum 0.8 的 {id} 语法
✅ 第三方回调显式登记 external_callback、ingress 和 plaintext
```
