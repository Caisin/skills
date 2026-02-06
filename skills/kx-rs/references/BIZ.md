# biz 模块模板

## 目录结构

```
bizs/<biz>/
├── Cargo.toml
└── src/
    ├── lib.rs
    ├── install.rs
    ├── router.rs
    ├── ctl/
    │   ├── mod.rs
    │   └── xxx_ctl.rs
    ├── svc/
    │   ├── mod.rs
    │   └── xxx_svc.rs
    └── dto/          # 可选
        ├── mod.rs
        └── xxx_dto.rs
```

## lib.rs

```rust
pub mod ctl;
pub mod dto;
pub mod svc;
pub mod install;
pub mod router;

pub use kx_ents_xxx::entity as ents;
kx_sea_orm::ext_db_trait!(xxx);
```

## install.rs

```rust
use anyhow::Result;
use crate::SeaOrmExt;
use kx_sea_orm::SeaOrms;

pub async fn install() -> Result<()> {
    let c = &mut SeaOrms::xxx().await?;
    crate::ents::XxxMigrate::migrate(c).await?;
    Ok(())
}
```

## router.rs

```rust
use aide::axum::{ApiRouter, routing::{get, post, put, delete}};
use crate::ctl;

pub fn apis() -> ApiRouter {
    ApiRouter::new().nest("/xxx", ctl::xxx_ctl::apis())
}
```

## 控制器（ctl/xxx_ctl.rs）

```rust
use aide::axum::{ApiRouter, routing::{get, post, put, delete}};
use axum::{Json, extract::Path};
use kx_axum::{R, NR, AxumErr};
use kx_sea_orm::{SeaOrms, common::{Page, Paging}};
use kx_axum::ext::QsQuery;
use crate::ents::xxx_table::*;
use crate::SeaOrmExt;

pub fn apis() -> ApiRouter {
    ApiRouter::new()
        .api_route("/page", get(page))
        .api_route("/get/{id}", get(get_by_id))
        .api_route("/save", post(save))
        .api_route("/del/{id}", delete(del))
}

async fn page(QsQuery(mut qry): QsQuery<XxxTableQry>, QsQuery(paging): QsQuery<Paging>) -> Result<R<Page<XxxTable>>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    if !qry.has_order() { qry.desc_id(); }
    let ret = qry.select().is_del_eq(false).page(c, paging).await?;
    Ok(ret.into())
}

async fn get_by_id(Path(id): Path<i64>) -> Result<R<XxxTable>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    Ok(XxxTable::get(c, id).await?.into())
}

async fn save(Json(mut req): Json<XxxTableModify>) -> Result<R<XxxTable>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    let now = kx_tools::times::sys_time_ts();
    if req.get_pk_val().is_err() { req.set_created_at(now).set_default().unset_id(); }
    req.set_updated_at(now);
    Ok(req.save(c).await?.into())
}

async fn del(Path(id): Path<i64>) -> Result<NR, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    let now = kx_tools::times::sys_time_ts();
    XxxTable::m().set_id(id).set_is_del(true).set_deleted_at(now).set_updated_at(now).to_owned().update(c).await?;
    Ok(R::succ())
}
```

### crud_api! 宏（快速替代手写控制器）

```rust
use kx_axum::crud_api;
crud_api!(crate::ents::xxx_table, XxxCtl, "xxx");

pub fn apis() -> ApiRouter {
    ApiRouter::new()
        .api_route("/all", get(XxxCtl::all))
        .api_route("/page", get(XxxCtl::page))
        .api_route("/save", post(XxxCtl::save))
        .api_route("/get/{id}", get(XxxCtl::get))
        .api_route("/del/{id}", delete(XxxCtl::del))
}
```

## 服务层（svc/xxx_svc.rs）

```rust
use anyhow::Result;
use kx_sea_orm::SeaOrms;
use crate::ents::xxx_table::*;
use crate::SeaOrmExt;

pub async fn create_xxx(name: &str, uid: i64) -> Result<XxxTable> {
    let c = &mut SeaOrms::xxx().await?;
    let now = kx_tools::times::sys_time_ts();
    let mut m = XxxTable::m();
    m.set_name(name).set_uid(uid).set_created_at(now).set_updated_at(now).set_default().unset_id();
    m.save(c).await
}
```

## DTO（dto/xxx_dto.rs）

```rust
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

/// 创建请求
#[derive(Debug, Serialize, Deserialize, JsonSchema)]
pub struct CreateXxxReq {
    /// 名称
    pub name: String,
    /// 用户ID
    pub uid: i64,
}
```

## Cargo.toml

```toml
[package]
name = "kx-biz-xxx"
version.workspace = true
authors.workspace = true
edition.workspace = true
license.workspace = true
publish.workspace = true

[dependencies]
anyhow = { workspace = true }
schemars = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
kx-axum = { workspace = true }
kx-sea-orm = { workspace = true }
kx-tools = { workspace = true }
kx-ents-xxx = { workspace = true }
```
