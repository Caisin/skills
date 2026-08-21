# Write Entity Patterns

## Dense Entity

```rust
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;

#[sea_orm::model]
#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq, Default)]
#[sea_orm(
    table_name = "job_outbox",
    comment = "任务事务外发事件。",
    model_attrs(derive(Sea))
)]
pub struct Model {
    #[sea_orm(primary_key, comment = "事件主键。")]
    pub id: i64,
    #[sea_orm(unique_key = "event_key", comment = "事件类型。")]
    pub event_type: String,
    #[sea_orm(unique_key = "event_key", comment = "业务幂等键。")]
    pub idempotency_key: String,
    #[sea_orm(indexed, comment = "待处理或已完成状态。")]
    pub state: String,
    #[sea_orm(comment = "最近更新 Unix 时间戳，单位秒。")]
    pub updated_at: i64,
}

impl ActiveModelBehavior for ActiveModel {}
```

## Relation Without Foreign Keys

允许 relation，但关系拥有侧必须 `skip_fk`。引用存在性由 service 校验并通过事务维护。

```rust
#[sea_orm(belongs_to, from = "dept_id", to = "id", skip_fk)]
pub dept: BelongsTo<super::dept::Entity>,
```

## Install-owned Migration

```rust
use crate::SeaOrmExt as _;
use anyhow::Result;
use kx_sea_common::SchemaCommentSyncExt;
use sea_orm::{ConnectionTrait, DatabaseConnection};

pub struct JobInstall;

impl JobInstall {
    pub async fn migrate() -> Result<()> {
        let db = kx_sea_orm::SeaOrms::job().await?;
        Self::migrate_with(&db).await
    }

    pub async fn migrate_with(db: &DatabaseConnection) -> Result<()> {
        db.sync_schema_with_comments("kx-biz-job::entity::*").await?;
        db.execute_raw(db.get_database_backend().build(
            &JobOutbox::create_index_statement(
                "idx_job_outbox_state_updated_at",
                vec![job_outbox::Column::State, job_outbox::Column::UpdatedAt],
            ),
        ))
        .await?;
        Ok(())
    }
}
```

## Index Boundary

```text
indexed                  -> 单列普通索引，官方 sync
unique                   -> 单列唯一索引，官方 sync
同名 unique_key          -> 联合唯一索引，官方 sync
联合普通索引             -> install.rs 显式创建
字段参与多个联合唯一分组 -> 额外分组在 install.rs 显式创建
```

不要为了保留旧索引名称而重复创建相同列集合；schema sync 主要按列集合判断索引是否缺失。

## Directory Boundary

```text
src/entity/<subdomain>/*.rs -> 表、枚举和 relation
src/entity/mod.rs           -> 子域声明与稳定重导出
src/install.rs              -> schema sync、备注和属性无法表达的索引
```

不要创建 `src/entity/prelude.rs` 作为第二套迁移入口。

## 常见错误

```text
❌ 给已写 comment 的表和字段重复保留同义 rustdoc
❌ 用 unique_key 表达联合普通索引
❌ 在 relation 上省略 skip_fk，从而创建数据库外键
❌ 在业务模块中逐表迁移，绕过 XxxInstall
```

## 正确做法

```text
✅ 表和持久化字段使用 comment
✅ 联合普通索引在 install.rs 显式创建
✅ relation 拥有侧声明 skip_fk
✅ 通过 XxxInstall::migrate()/migrate_with() 暴露迁移入口
```
