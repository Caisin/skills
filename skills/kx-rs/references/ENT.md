# ent 模块模板

## 目录结构

```
ents/<ds>/
├── Cargo.toml
└── src/
    ├── lib.rs
    └── entity/
        ├── mod.rs
        └── <table>.rs
```

## lib.rs

```rust
pub mod entity;
pub use kx_sea_common as common;
```

## entity/mod.rs

```rust
use anyhow::Result;
use sea_orm::ConnectionTrait;
use crate::entity::{<alias1>::<Alias1>, <alias2>::<Alias2>};

pub mod <table1>;
pub mod <table2>;

pub struct <Ds>Migrate;
impl <Ds>Migrate {
    pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
        <Alias1>::auto_migrate(c).await?;
        <Alias1>::create_idxs(c).await?;  // 如有索引
        <Alias2>::auto_migrate(c).await?;
        Ok(())
    }
}
```

## 实体文件（`<table>.rs`）

```rust
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Sea, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
// ai请注意,别名是 table_name 转大驼峰,当前别名为 XxxYyy
#[sea_orm(table_name = "xxx_yyy", comment = "表描述")]
pub struct Model {
    /// ID
    #[sea_orm(primary_key)]
    pub id: i64,
    /// 用户ID
    #[sea_orm(indexed)]
    pub uid: i64,
    /// 名称
    pub name: String,
    /// 内容（Text 类型）
    #[sea_orm(column_type = "Text")]
    pub content: String,
    /// 备注（指定长度）
    #[sea_orm(column_type = "String(StringLen::N(500))")]
    pub remark: String,
    /// 金额
    #[sea_orm(column_type = "Decimal(Some((10, 2)))")]
    pub amount: Decimal,
    /// 创建时间
    pub created_at: i64,
    /// 更新时间
    pub updated_at: i64,
    /// 是否删除
    #[sea_orm(indexed)]
    pub is_del: bool,
    /// 删除时间
    pub deleted_at: i64,
}

impl Model {
    /// 联合索引（仅业务需要时创建，单字段索引用 sea_orm 属性 indexed/unique）
    pub async fn create_idxs<C: ConnectionTrait>(c: &C) -> Result<()> {
        let st = Self::create_index_statement("idx_uid_name", vec![Column::Uid, Column::Name]);
        // 唯一索引: st.unique();
        if let Err(_) = Self::exec_idx(c, &st).await {}
        Ok(())
    }
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}
impl ActiveModelBehavior for ActiveModel {}
```

## 联合主键

```rust
#[sea_orm(table_name = "xxx_union_pk", comment = "联合主键表")]
pub struct Model {
    #[sea_orm(primary_key, auto_increment = false)]
    pub pk_1: i64,
    #[sea_orm(primary_key, auto_increment = false)]
    pub pk_2: i64,
}
```

## Cargo.toml

```toml
[package]
name = "kx-ents-<ds>"
version.workspace = true
authors.workspace = true
edition.workspace = true
license.workspace = true
publish.workspace = true

[dependencies]
anyhow = { workspace = true }
chrono = { workspace = true, features = ["serde"] }
kx-sea-common = { workspace = true }
sea-orm = { workspace = true, features = ["macros", "runtime-tokio-rustls"] }
serde = { workspace = true }
# 按需: rust_decimal, serde_with

[features]
full = ["mysql", "postgres", "sqlite"]
mysql = ["sea-orm/sqlx-mysql"]
postgres = ["sea-orm/sqlx-postgres"]
sqlite = ["sea-orm/sqlx-sqlite"]
```
