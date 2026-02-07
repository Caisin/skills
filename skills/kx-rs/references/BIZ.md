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
use kx_axum::{axum::Router, routing::get};
use crate::ctl::xxx_ctl::XxxCtl;

pub struct BizRouter;

impl BizRouter {
    pub fn apis() -> Router {
        Router::new().nest("/xxx", XxxCtl::apis())
    }
}
```

## 控制器（ctl/xxx_ctl.rs）

> **重要**：Router 函数和 Handler 必须在同一 `impl` 块内，openapi-scan 才能正确扫描。

```rust
use crate::ents::xxx_table::{XxxTable, XxxTableModify, XxxTableQry};
use kx_axum::{
    AxumErr, Json, R,
    axum::Router,
    axum::routing::{delete, get, post},
    ext::QsQuery,
    extract::Path,
};
use kx_sea_orm::common::{Page, Paging};
use crate::svc::xxx_svc::XxxSvc;

pub struct XxxCtl;

impl XxxCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/{id}", get(Self::get))
            .route("/{id}", delete(Self::del))
    }

    /// 分页查询
    async fn page(
        QsQuery(req): QsQuery<XxxTableQry>,
        QsQuery(page): QsQuery<Paging>,
    ) -> Result<R<Page<XxxTable>>, AxumErr> {
        let ret = XxxSvc::page(req, page).await?;
        Ok(ret.into())
    }

    /// 详情
    async fn get(Path(id): Path<i64>) -> Result<R<XxxTable>, AxumErr> {
        let ret = XxxSvc::get(id).await?;
        Ok(ret.into())
    }

    /// 保存
    async fn save(Json(req): Json<XxxTableModify>) -> Result<R<XxxTable>, AxumErr> {
        let ret = XxxSvc::save(req).await?;
        Ok(ret.into())
    }

    /// 删除
    async fn del(Path(id): Path<i64>) -> Result<R<()>, AxumErr> {
        XxxSvc::del(id).await?;
        Ok(R::succ())
    }
}
```

## 服务层（svc/xxx_svc.rs）

```rust
use anyhow::Result;
use crate::ents::xxx_table::{XxxTable, XxxTableModify, XxxTableQry};
use kx_sea_orm::{SeaOrms, common::{Page, Paging}};
use kx_tools::times;
use crate::SeaOrmExt;

pub struct XxxSvc;

impl XxxSvc {
    pub async fn page(mut qry: XxxTableQry, paging: Paging) -> Result<Page<XxxTable>> {
        let c = &mut SeaOrms::xxx().await?;
        if !qry.has_order() { qry.desc_id(); }
        let ret = qry.select().is_del_eq(false).page(c, paging).await?;
        Ok(ret)
    }

    pub async fn get(id: i64) -> Result<XxxTable> {
        let c = &mut SeaOrms::xxx().await?;
        let ret = XxxTable::sel().id_eq(id).is_del_eq(false).one(c).await?;
        Ok(ret)
    }

    pub async fn save(mut req: XxxTableModify) -> Result<XxxTable> {
        let c = &mut SeaOrms::xxx().await?;
        let now = times::sys_time_ts();
        if req.get_pk_val().is_err() { req.set_created_at(now).set_default().unset_id(); }
        req.set_updated_at(now);
        let ret = req.save(c).await?;
        Ok(ret)
    }

    pub async fn del(id: i64) -> Result<()> {
        let c = &mut SeaOrms::xxx().await?;
        let now = times::sys_time_ts();
        XxxTable::m().set_id(id).set_is_del(true).set_deleted_at(now).set_updated_at(now).to_owned().update(c).await?;
        Ok(())
    }
    
    pub async fn real_del(id: i64) -> Result<()> {
        let c = &mut SeaOrms::xxx().await?;
        XxxTable::del(c, id).await?;
        Ok(())
    }
}
```

## DTO（dto/xxx_dto.rs）

```rust
use serde::{Deserialize, Serialize};

/// 创建请求
#[derive(Debug, Serialize, Deserialize)]
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
serde = { workspace = true }
serde_json = { workspace = true }
kx-axum = { workspace = true }
kx-sea-orm = { workspace = true }
kx-tools = { workspace = true }
kx-ents-xxx = { workspace = true }
```
