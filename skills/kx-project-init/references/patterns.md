# KX Project Init Patterns

用于 `kx-project-init` 的完整项目初始化模板。

## 先记住这几条

1. **第一步一定是**：

```bash
cargo new <project-name>
```

2. 初始化后至少要补：
   - kx-rs 必要依赖
   - `AGENTS.md`
   - `docs/long-term-memory.md`
   - `.agents` 子模块
   - 数据库模块、`install.rs` 与 CRUD 骨架
   - `README.md`
3. 默认先给简化模板；只有大型工程再拆多 crate。

---

## 1. 简化模板（默认）

### 适用场景

- 小型项目
- Demo / 内部工具
- 需要快速起项目并完整跑起来

### 推荐初始化顺序

```text
1. cargo new <project-name>
2. 补 Cargo.toml 必要依赖
3. 初始化 .agents 子模块
4. 写 AGENTS.md
5. 写 docs/long-term-memory.md
6. 建 src/ents / src/ctl / src/svc / src/router.rs
7. 建 main.rs、install.rs、数据库模块与 CRUD 模板
8. 写 README.md
```

### 推荐目录结构

```text
<project-name>/
├── .agents/
├── Cargo.toml
├── AGENTS.md
├── README.md
├── cfg.toml
├── docs/
│   └── long-term-memory.md
└── src/
    ├── main.rs
    ├── router.rs
    ├── install.rs
    ├── ents/
    │   ├── mod.rs
    │   └── user.rs
    ├── ctl/
    │   ├── mod.rs
    │   └── user.rs
    └── svc/
        ├── mod.rs
        └── user.rs
```

### Cargo.toml 依赖模板

```toml
[dependencies]
anyhow = "1"
clap = { version = "4.5", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

kx-axum = { version = "0.1", registry = "hekx" }
kx-sea-orm = { version = "0.1", registry = "hekx", features = ["postgres", "sqlite"] }
kx-sea-common = { version = "0.1", registry = "hekx" }
kx-tools = { version = "0.1", registry = "hekx", features = ["times"] }
kx-tracing = { version = "0.1", registry = "hekx" }
sea-orm = { version = "2.0.0-rc.37" }
```

### `.agents` 子模块初始化

```bash
git submodule add -b master https://github.com/Caisin/skills.git .agents
```

### 最小数据库模块模板

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

### install.rs 模板

```rust
// src/install.rs
use anyhow::Result;
use kx_sea_orm::SeaOrms;
use crate::ents::user::User;

pub struct AppInstall;

impl AppInstall {
    pub async fn install() -> Result<()> {
        let c = &mut SeaOrms::get("base").await?;
        User::auto_migrate(c).await?;
        Ok(())
    }
}
```

### 最小 CRUD 模板

```rust
// src/ctl/user.rs
use kx_axum::{
    AxumErr, Json, R,
    axum::{
        Router,
        routing::{get, post},
    },
    ext::QsQuery,
};
use kx_sea_orm::{SeaOrms, common::{Page, Paging}};
use crate::ents::user::{User, UserModify, UserQry};
use kx_tools::times;

pub struct UserCtl;

impl UserCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
    }

    async fn page(
        QsQuery(mut req): QsQuery<UserQry>,
        QsQuery(page): QsQuery<Paging>,
    ) -> Result<R<Page<User>>, AxumErr> {
        let c = &mut SeaOrms::get("base").await?;
        if !req.has_order() {
            req.desc_id();
        }
        Ok(req.page(c, page).await?.into())
    }

    async fn save(Json(mut req): Json<UserModify>) -> Result<R<()>, AxumErr> {
        let c = &mut SeaOrms::get("base").await?;
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

### main.rs 模板

```rust
use anyhow::Result;
use clap::Parser;
use kx_axum::{axum::Router, cfg::AppArgs, jwt::AdmClaims};

mod ctl;
mod ents;
mod router;
mod svc;

#[derive(Parser, Debug, Clone)]
enum SubCmd {
    Server,
    Install,
}

#[tokio::main]
async fn main() -> Result<()> {
    let arg = AppArgs::<SubCmd>::init_def_args().await?;
    match &arg.sub {
        SubCmd::Server => {
            let app: Router = router::apis();
            kx_axum::run::<AdmClaims>(app).await?;
        }
        SubCmd::Install => {
            crate::install::AppInstall::install().await?;
        }
    }
    Ok(())
}
```

---

## 2. 大型项目模板

### 适用场景

- 大型业务项目
- 模块多
- 明确需要 `bins/* + bizs/* + ents/*`

### 推荐目录结构

```text
<project-name>/
├── .agents/
├── Cargo.toml
├── AGENTS.md
├── README.md
├── docs/
│   └── long-term-memory.md
├── bins/
│   └── app/
├── bizs/
│   └── user/
└── ents/
    └── user/
```

### 关键点

```text
- bins/* 负责启动与装配
- bizs/* 负责 web / service 层
- ents/* 负责实体、迁移、索引
- 只有明确需要时再上这种结构
```

---

## 3. README 初始化模板

### 推荐内容

```md
# <project-name>

## 简介

这里写项目简介。

## 初始化

```bash
cargo build
```

## 配置

- 编辑 `cfg.toml`
- 配置数据库连接

## 运行

```bash
cargo run -- server
```

## 数据库迁移

```bash
cargo run -- install
```

## 目录说明

- `src/ents/`：实体模型
- `src/ctl/`：控制器
- `src/svc/`：业务服务
- `src/router.rs`：路由聚合
```

### 关键点

```text
- README 至少要写“如何配置、如何运行、如何迁移、如何更新 `.agents` 子模块”。
- 新项目不应缺最基本的启动说明与子模块维护说明。
```

## 常见错误

```text
❌ 只初始化代码，不写 install.rs
❌ README 里没有 install / server / `.agents` 更新方法，导致模板不可落地
❌ 小项目默认上重型多 crate 结构
```

## 正确做法

```text
✅ 从 cargo new 开始给完整初始化顺序
✅ 默认给单工程模板
✅ 初始化 AGENTS / long-term-memory / .agents / README
✅ 至少补一个可跑通的数据库模块、install.rs 和 CRUD 骨架
```
