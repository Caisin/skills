# Write Ctl Patterns

## Thin Controller

```rust
use kx_axum::{
    ApiMeta, ApiRouter, AxumErr, R,
    axum::{Json, extract::{Path, Query}},
};

pub struct ItemCtl;

impl ItemCtl {
    pub fn apis() -> ApiRouter {
        ApiRouter::new()
            .get("/", Self::page, ApiMeta::new("item.page", "项目分页"))
            .get("/{id}", Self::detail, ApiMeta::new("item.detail", "项目详情"))
            .post("/", Self::save, ApiMeta::new("item.save", "保存项目"))
            .delete("/{id}", Self::delete, ApiMeta::new("item.delete", "删除项目"))
    }

    pub async fn page(Query(req): Query<ItemPageQuery>) -> Result<R<ItemPage>, AxumErr> {
        Ok(ItemSvc::page(req).await?.into())
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
❌ 使用 Axum 0.7 的 /:id 路径语法
❌ 第三方回调只标 public，没有 ingress 和 plaintext 策略
```

## 正确做法

```text
✅ handler 只提取参数、调用 svc 和转换响应
✅ 请求与响应使用最小 DTO/View
✅ 路径参数使用 Axum 0.8 的 {id} 语法
✅ 第三方回调显式登记 external_callback、ingress 和 plaintext
```
