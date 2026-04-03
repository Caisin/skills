# KX Axum Web Patterns

用于 `kx-axum-web` 的 web 层模板。

> 说明：下面的业务目录如 `bizs/`、`ctl/`、`svc/` 属于**下游业务仓库约定**，不是当前工作区事实。
>
> 代码风格优先复用两类已验证模式：业务模块风格（ctl 薄、svc 收口、router nest、install 迁移）与 bin 入口风格（main 子命令分流、cfg 装配、kx_axum::run 启动）。

## 先记住这几条

1. handler 默认返回：

```rust
Result<R<T>, AxumErr>
```

2. 列表 / 分页优先接 `*Qry`，保存优先接 `*ModifyModel`。
3. `ctl/` 负责收参与返回；复杂事务、多表拼装、关联写入优先下沉到 `svc/`。
4. `router.rs` 负责 `nest()` 路由聚合；`install.rs` 负责迁移或初始化。
5. 默认先给单工程 / 单 crate 模板，只有大型工程再拆 `bins/* + bizs/* + ents/*`。
6. `bins/*` 负责 server / install 子命令与 `kx_axum::run(...)` 启动；`build.rs` 生成 OpenAPI 是可选项。
7. 如果只是简单 CRUD，可优先考虑 `crud_api!`。

---

## 0. 单工程 / 单 crate 简单模板

### 适用场景

- 小型项目
- Demo / 内部工具
- 一个工程里直接把模型、接口、启动都放在同一个 crate

### 推荐模板

这是默认优先推荐的简单模板：

```text
my-app/
├── Cargo.toml
├── cfg.toml
├── src/
│   ├── main.rs
│   ├── ents/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── ctl/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── svc/
│   └── router.rs
└── build.rs        # 可选
```

```rust
// src/main.rs
use anyhow::Result;
use clap::Parser;
use kx_axum::{axum::Router, cfg::AppArgs, jwt::AdmClaims};

mod ctl;
mod ents;
mod router;

#[derive(Parser, Debug, Clone)]
enum SubCmd {
    Server,
}

#[tokio::main]
async fn main() -> Result<()> {
    let _arg = AppArgs::<SubCmd>::init_def_args().await?;
    let app: Router = router::apis();
    kx_axum::run::<AdmClaims>(app).await?;
    Ok(())
}
```

```rust
// src/router.rs
use kx_axum::axum::Router;

use crate::ctl::user::UserCtl;

pub fn apis() -> Router {
    Router::new().nest("/user", UserCtl::apis())
}
```

```rust
// src/ents/user.rs
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Sea, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(table_name = "user", comment = "用户表")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub name: String,
    pub created_at: i64,
    pub updated_at: i64,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

### 关键点

```text
- 小型工程没必要一开始拆多 crate。
- 可以直接把 sea-orm 模型放到 src/ents/ 目录。
- 可以直接把 web 启动入口写到 src/main.rs。
- 只有工程变大、模块增多、协作复杂时，再拆 bins/bizs/ents。
```
---

## 1. 模块结构

### 适用场景

- 中大型工程
- 已经决定采用 `bins/* + bizs/* + ents/*` 分 crate 结构
- 想先知道 ctl/router/install 应该怎么拆

### 推荐模板

```text
bizs/<biz>/src/
├── ctl/
│   ├── adm/
│   ├── app/
│   └── mod.rs
├── dto/
├── svc/
├── install.rs
├── router.rs
└── lib.rs
```

```rust
pub mod ctl;
pub mod dto;
pub mod install;
pub mod router;
pub mod svc;

pub use kx_ents_xxx as ents;
```

### 关键点

```text
- ctl/ 放 handler。
- svc/ 放事务与业务编排。
- router.rs 聚合 ctl。
- install.rs 负责模块迁移或初始化。
```

---

## 2. 分页 + 保存控制器模板

### 适用场景

- 标准 page/list/save 接口
- 直接复用 `*Qry` / `*ModifyModel`

### 推荐模板

下面这个模式直接来自 `bizs/asset/src/ctl/adm/pay_tmp.rs` / `asset_item.rs`：

```rust
use kx_axum::{
    AxumErr, Json, R,
    axum::{
        Router,
        routing::{get, post},
    },
    ext::QsQuery,
};
use kx_ents_xxx::foo::{Foo, FooModify, FooQry};
use kx_sea_orm::{
    SeaOrms,
    common::{Page, Paging},
};
use kx_tools::times;

pub struct AdmFooCtl;

impl AdmFooCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/list", get(Self::list))
    }

    async fn list() -> Result<R<Vec<Foo>>, AxumErr> {
        let c = &mut SeaOrms::xxx().await?;
        let ret = Foo::sel().desc_id().all(c).await?;
        Ok(ret.into())
    }

    async fn page(
        QsQuery(mut req): QsQuery<FooQry>,
        QsQuery(page): QsQuery<Paging>,
    ) -> Result<R<Page<Foo>>, AxumErr> {
        let c = &mut SeaOrms::xxx().await?;
        if !req.has_order() {
            req.desc_id();
        }
        let ret = req.page(c, page).await?;
        Ok(ret.into())
    }

    async fn save(Json(mut req): Json<FooModify>) -> Result<R<()>, AxumErr> {
        let c = &mut SeaOrms::xxx().await?;
        let now = times::sys_time_ts();
        if req.get_pk_val().is_err() {
            req.set_created_at(now).set_default().unset_id();
        }
        req.set_updated_at(now);
        req.save(c).await?;
        Ok(R::ok(()))
    }
}
```

### 关键点

```text
- FooQry / FooModify 是 kx-sea-orm 生成结构体，不建议手写一套重复分页保存 DTO。
- page 接口默认补 has_order()/desc_id()。
- save 接口默认补 created_at / updated_at / set_default / unset_id 语义。
```

---

## 3. 控制器薄、service 收口模板

### 适用场景

- handler 只有一层转发
- 想把分页/保存逻辑沉到 service

### 推荐模板

这个模式直接来自 `bizs/asset/src/ctl/adm/vip_item.rs`：

```rust
use kx_axum::{
    AxumErr, Json, R,
    axum::{
        Router,
        routing::{get, post},
    },
    ext::QsQuery,
};
use kx_ents_xxx::foo::{Foo, FooModify, FooQry};
use kx_sea_orm::common::{Page, Paging};

use crate::svc::foo_svc::FooSvc;

pub struct AdmFooCtl;

impl AdmFooCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/list", get(Self::list))
    }

    async fn list() -> Result<R<Vec<Foo>>, AxumErr> {
        Ok(FooSvc::list().await?.into())
    }

    async fn page(
        QsQuery(req): QsQuery<FooQry>,
        QsQuery(page): QsQuery<Paging>,
    ) -> Result<R<Page<Foo>>, AxumErr> {
        Ok(FooSvc::page(req, page).await?.into())
    }

    async fn save(Json(req): Json<FooModify>) -> Result<R<()>, AxumErr> {
        FooSvc::save(req).await?;
        Ok(R::ok(()))
    }
}
```

### 关键点

```text
- 一旦逻辑开始变复杂，就把分页默认排序、保存时间戳、事务、多表拼装收口到 svc/。
- ctl/ 保持 web 层职责，不承担重业务逻辑。
```

---

## 4. 复杂写入接口模板

### 适用场景

- 保存时要带属性、子表、事务
- 请求体不是纯 `*ModifyModel`

### 推荐模板

这个模式直接来自 `bizs/asset/src/ctl/adm/pay_item.rs`：

```rust
use kx_axum::{
    AxumErr, Json, R,
    axum::{
        Router,
        routing::post,
    },
};
use kx_sea_orm::SeaTrans;
use serde_json::Value;

pub struct AdmFooCtl;

impl AdmFooCtl {
    pub fn apis() -> Router {
        Router::new().route("/", post(Self::save))
    }

    async fn save(Json(data): Json<Value>) -> Result<R<()>, AxumErr> {
        SeaTrans::new()
            .transaction(|tx| {
                Box::pin(async move {
                    let db = tx.xxx().await?;
                    // 1. data -> ModifyModel
                    // 2. 保存主表
                    // 3. 删除并重建子表 / 属性表
                    // 4. 同一事务提交
                    let _ = db;
                    Ok(())
                })
            })
            .await?;
        Ok(R::ok(()))
    }
}
```

### 关键点

```text
- 请求体复杂时，可先收 `Json<Value>` 再自行拆字段。
- 主表、属性表、子表联动时，优先直接在事务里收口。
- 真正的实体/事务写法可继续参考 kx-sea-orm。
```

---

## 5. router.rs 聚合模板

### 适用场景

- 需要聚合多个 controller
- 需要 admin/app 两套路由入口

### 推荐模板

这个模式直接来自 `bizs/asset/src/router.rs`：

```rust
use kx_axum::axum::Router;

use crate::ctl::adm::{foo::AdmFooCtl, bar::AdmBarCtl};

pub struct XxxRouter;

impl XxxRouter {
    pub fn adm_apis() -> Router {
        Router::new()
            .nest("/foo", AdmFooCtl::apis())
            .nest("/bar", AdmBarCtl::apis())
    }

    pub fn app_router() -> Router {
        Router::new()
    }
}
```

### 关键点

```text
- 路由路径收口在 router.rs，不要散在多个模块随意拼。
- admin/app 两套路由可分开暴露。
```

---

## 6. install.rs 模板

### 适用场景

- 模块启动时要自动迁移
- 需要一个模块级安装入口

### 推荐模板

这个模式直接来自 `bizs/asset/src/install.rs`：

```rust
use kx_sea_orm::SeaOrms;

pub struct XxxInstall;

impl XxxInstall {
    pub async fn install() -> anyhow::Result<()> {
        let c = &mut SeaOrms::xxx().await?;
        kx_ents_xxx::auto_migrate(c).await?;
        Ok(())
    }
}
```

### 关键点

```text
- install.rs 只负责模块安装入口。
- 实体迁移本身的模板与规则，继续参考 kx-sea-orm。
```

---

## 7. `bins/*` 入口模板（大型工程可选）

### 适用场景

- 需要补 `main.rs` 启动入口
- 需要补可选的 `build.rs` 生成 OpenAPI
- 需要说明 `cfg.toml` 里 app/db/jwt/security 的基本组织

### 推荐模板

下面这个模式直接来自 `bins/adm`：

#### 7.1 `src/main.rs`

```rust
use anyhow::Result;
use clap::Parser;
use kx_axum::{cfg::AppArgs, jwt::AdmClaims};
use kx_biz_xxx::{install::XxxInstall, router::XxxRouter};

#[derive(Parser, Debug, Clone)]
#[clap(author, version, about, long_about = None)]
enum SubCmd {
    /// Start the server
    Server,
    /// install
    Install,
}

#[tokio::main]
async fn main() -> Result<()> {
    let arg = AppArgs::<SubCmd>::init_def_args().await?;
    match &arg.sub {
        SubCmd::Server => {
            let app = XxxRouter::apis();
            let app = app.nest("/app", XxxRouter::app_apis());
            kx_axum::run::<AdmClaims>(app).await?;
        }
        SubCmd::Install => {
            XxxInstall::migrate().await?;
        }
    }
    Ok(())
}
```

#### 7.2 `build.rs`（可选）

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 中文备注：在当前 bin crate 构建时生成专属 OpenAPI。
    kx_openapi_scan::generate(None)?;
    Ok(())
}
```

#### 7.3 `Cargo.toml` 最小依赖

```toml
[dependencies]
anyhow = { workspace = true }
kx-axum = { workspace = true }
clap = { workspace = true }
kx-biz-xxx = { workspace = true }
tokio = { workspace = true, features = ["full"] }

[build-dependencies]
kx-openapi-scan = { version = "0.1", registry = "hekx" }
```

#### 7.4 `cfg.toml` 关注点

```toml
[app]
name = "kx"
port = 8888

[dbs]
base = "postgres://..."

[db_alias]
auth = "base"
asset = "base"

[jwt]
secret = "..."
jwt_exp = 7200
refresh_exp = 604800

[security]
enable = false
skip_routes = [
  "/auth/dt/callback/{app_id}"
]
```

### 关键点

```text
- `main.rs` 负责 Server / Install 子命令切换。
- 运行入口通常通过 `AppArgs::<SubCmd>::init_def_args()` 读取 cfg 与命令行。
- `kx_axum::run::<Claims>(app)` 负责真正启动服务。
- 如果项目需要独立生成 OpenAPI，再额外补 `build.rs` 调用 `kx_openapi_scan::generate(None)`。
- `cfg.toml` 一般至少包含 app/db_alias/jwt/security 等块。
```

---

## 8. `crud_api!` 模板

### 适用场景

- 纯 page/get/save/del
- 基本不加业务逻辑

### 推荐模板

这个模式可参考 `bizs/auth/src/ctl/system/user.rs`、`role.rs`、`permission.rs`：

```rust
use kx_axum::{
    axum::Router,
    axum::routing::{delete, get, post},
    crud_api,
};
use kx_ents_auth::entity::kx_role::{self, KxRole};

crud_api!(kx_role, RoleCtl, "auth");

impl RoleCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/{id}", get(Self::get))
            .route("/{id}", delete(Self::del))
    }
}
```

### 关键点

```text
- crud_api! 会自动生成 all/page/save/get/del。
- 适合基础 CRUD，不适合复杂事务、多表写入、额外校验很多的接口。
- openapi-scan 已对 crud_api! 做了额外识别处理。
```

---

## 常见错误

```text
❌ 明明只是简单 CRUD，还手写一整套重复 handler
❌ 明明有复杂事务，却还硬塞进 crud_api!
❌ save/page 接口不接 *ModifyModel / *Qry，重复手写 web DTO
❌ ctl/ 里直接堆复杂事务和多表逻辑
❌ install.rs、router.rs、ctl/、bins/main.rs 职责混在一起
❌ 小项目一开始就拆成很多 crate，导致模板过重
❌ bin 入口里直接堆业务逻辑，而不是只做启动、装配和 install 分流
```

## 正确做法

```text
✅ 简单 CRUD 优先评估 crud_api!
✅ 标准 page/save/list 优先接 *Qry / *ModifyModel
✅ 复杂写入优先 ctl + svc + SeaTrans
✅ router.rs 统一收口 nest()，install.rs 只做安装入口
✅ 小型工程优先用单工程 / 单 crate 模板
✅ bins/main.rs 只负责子命令分流、装配 app 与调用 kx_axum::run(...)
✅ web 层专注接口形状，实体/迁移模板继续参考 kx-sea-orm
```
