# kx-rs 项目模板

当用户要求创建 kx-rs 框架项目时，按此模板生成完整项目结构。

## 目录结构

```
<project-name>/
├── .cargo/config.toml
├── .gitignore
├── Cargo.toml
├── build.rs
├── openapi.json          # 编译期自动生成
└── src/
    ├── main.rs
    ├── lib.rs
    ├── router.rs
    ├── install.rs
    ├── ctl/
    │   ├── mod.rs
    │   └── <module>_ctl.rs
    ├── svc/
    │   ├── mod.rs
    │   └── <module>_svc.rs
    ├── dto/               # 可选
    │   ├── mod.rs
    │   └── <module>_dto.rs
    └── ents/
        ├── mod.rs
        └── <table>.rs
```

## .cargo/config.toml

```toml
[registry]
default = "hekx"

[registries.hekx]
index = "sparse+http://10.126.126.5:8000/api/v1/crates/"
credential-provider = ["cargo:token"]
```

## Cargo.toml

```toml
[package]
name = "<project-name>"
version = "0.1.0"
edition = "2024"
publish = false

[workspace.dependencies]
anyhow = { version = "1" }
clap = { version = "4.5", features = ["derive"] }
sea-orm = { version = "2.0.0-rc.30" }
serde = { version = "1", features = ["derive"] }
serde_json = { version = "1" }
tokio = { version = "1", features = ["full"] }

kx-axum = { version = "0.1", registry = "hekx" }
kx-sea-common = { version = "0.1", registry = "hekx" }
kx-sea-orm = { version = "0.1", registry = "hekx" }
kx-openapi-scan = { version = "0.1", registry = "hekx" }
kx-tools = { version = "0.1", registry = "hekx", features = ["cvt"] }

[dependencies]
tokio = { workspace = true }
anyhow = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
clap = { workspace = true }
kx-axum = { workspace = true }
kx-sea-orm = { workspace = true }
kx-sea-common = { workspace = true }
sea-orm = { workspace = true }
kx-tools = { workspace = true }

[build-dependencies]
anyhow = { workspace = true }
kx-openapi-scan = { workspace = true }
```

## build.rs

```rust
use std::path::PathBuf;

fn main() -> anyhow::Result<()> {
    println!("cargo:rerun-if-changed=src");
    println!("cargo:rerun-if-changed=cfg.toml");
    let manifest_dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?);
    let title = "<project-name>";
    let description = "<project-name> API 文档";
    let out = manifest_dir.join("openapi.json");
    let scan_cfg = kx_openapi_scan::default_config(Some(&manifest_dir))?
        .with_output(&out)
        .with_openapi_info(title, description);
    kx_openapi_scan::generate_with_config(scan_cfg)?;
    Ok(())
}
```

## src/main.rs

```rust
use anyhow::Result;
use clap::Parser;
use kx_axum::{cfg::AppArgs, jwt::AdmClaims};
use <crate_name>::{install::<Project>Install, router::<Project>Router};

#[derive(Parser, Debug, Clone, Default)]
#[clap(author, version, about, long_about = None)]
enum SubCmd {
    #[default]
    Server,
    Install,
}

#[tokio::main]
async fn main() -> Result<()> {
    let arg = AppArgs::<SubCmd>::init_def_args().await?;
    match arg.sub {
        SubCmd::Server => {
            let app = <Project>Router::apis();
            kx_axum::run::<AdmClaims>(app).await?;
        }
        SubCmd::Install => {
            <Project>Install::install().await?;
        }
    }
    Ok(())
}
```

## src/lib.rs

```rust
pub mod ctl;
pub mod dto;
pub mod ents;
pub mod install;
pub mod router;
pub mod svc;

kx_sea_orm::ext_db_trait!(<db_name>);
```

## src/router.rs

```rust
use kx_axum::{axum::Router, routing::get};
use crate::ctl::<module>_ctl::<Module>Ctl;

pub struct <Project>Router;

impl <Project>Router {
    pub fn apis() -> Router {
        Router::new()
            .nest("/<module>", <Module>Ctl::apis())
            .route("/openapi.json", get(|| async { include_str!("../openapi.json") }))
    }
}
```

## src/install.rs

```rust
use anyhow::Result;
use kx_sea_orm::SeaOrms;
use crate::SeaOrmExt;

pub struct <Project>Install;

impl <Project>Install {
    pub async fn install() -> Result<()> {
        let c = &mut SeaOrms::<db_name>().await?;
        crate::ents::<Project>Migrate::migrate(c).await?;
        Ok(())
    }
}
```

## .gitignore

```
/target
openapi.json
```

## 占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `<project-name>` | 项目名（kebab-case） | `my-app` |
| `<crate_name>` | crate 名（snake_case） | `my_app` |
| `<Project>` | 项目大驼峰 | `MyApp` |
| `<db_name>` | 数据源名 | `demo` |
| `<module>` | 业务模块名（snake_case） | `note` |
| `<Module>` | 模块大驼峰 | `Note` |
| `<table>` | 表名（snake_case） | `note` |
