# KX Sea ORM Migration

用于 `kx-sea-orm` 的建表、补字段与索引创建模板。

## 适用场景

- 需要给实体补建表/补字段
- 需要给实体补索引
- 需要展示当前仓库推荐的 migrate 入口

## 推荐模板

业务 crate 的迁移入口放在 `install.rs`，优先使用 entity registry 一次同步 Schema 和备注：

```rust
use anyhow::Result;
use kx_sea_orm::{DatabaseConnection, SchemaCommentSyncExt};

pub struct MyInstall;

impl MyInstall {
    pub async fn migrate() -> Result<()> {
        let db = kx_sea_orm::SeaOrms::my_alias().await?;
        Self::migrate_with(&db).await
    }

    pub async fn migrate_with(db: &DatabaseConnection) -> Result<()> {
        db.sync_schema_with_comments("my_crate::entity::*").await?;
        Ok(())
    }
}
```

`#[derive(Sea)]` 会把 `#[sea_orm(..., comment = "...")]` 中的表和字段备注注册到 KX
registry。该方法先调用 SeaORM 官方 `SchemaBuilder::sync`，再以相同 prefix 同步备注，
业务 crate 不维护逐表备注调用清单。

不要再为业务 crate 创建 `entity/prelude.rs` 包装相同的 migrate。单个 entity 或未采用
registry 的框架模块仍可使用模型入口：

```rust
use anyhow::Result;
use kx_sea_common::SchemaSyncConnection;

use super::{sys_dept::SysDept, sys_user::SysUser};

pub async fn migrate<C: SchemaSyncConnection>(c: &C) -> Result<()> {
    SysDept::auto_migrate(c).await?;
    SysUser::auto_migrate(c).await?;

    SysUser::create_index(c, "idx_usr_dept", vec![sys_user::Column::DeptId]).await?;
    SysUser::create_index(c, "idx_usr_mobile", vec![sys_user::Column::Mobile]).await?;
    Ok(())
}
```

```rust
pub async fn migrate<C: SchemaSyncConnection>(c: &C) -> Result<()> {
    account::migrate(c).await?;
    order::migrate(c).await?;
    log::migrate(c).await?;
    Ok(())
}
```

## 关键点

```text
- auto_migrate() 来自 derives/codegen，内部调用实验性的 SchemaBuilder::sync。
- sync_schema_with_comments() 是官方 sync 的补充，不重新实现 Schema diff。
- PostgreSQL 通过 COMMENT ON TABLE/COLUMN 同步备注；字符串和标识符必须转义。
- MySQL 新建对象的备注由上游 DDL 写入；SQLite 不持久化表/字段备注。
- 它只创建缺失表、列和索引，不修改或删除已有 schema 对象。
- 字段类型、约束修改和删除必须使用显式 migration，并经过发布审查。
- 泛型连接边界使用 SchemaSyncConnection，不重新实现 schema diff。
- `#[sea_orm(indexed)]`、`#[sea_orm(unique)]` 和共享同一名称的
  `#[sea_orm(unique_key = "...")]` 分别表达单列普通、单列唯一和联合唯一索引，由官方
  sync 创建。
- dense entity 当前不能用字段属性表达联合普通索引；这类索引继续在 `install.rs` 用
  `Alias::create_index_statement()` 显式创建。
- 同一字段只能属于一个 `unique_key` 分组；字段需要参与多个联合唯一索引时，额外分组
  仍在 `install.rs` 显式创建。
- 联合索引名尽量简短，普通索引用 idx_，唯一索引用 udx_。
- relation 拥有侧必须声明 `skip_fk`，让实体建表和 schema sync 跳过数据库外键。
- `skip_fk` 不会删除已有外键；移除旧约束仍需显式 migration。
```

## 常见错误

```text
❌ 只会手写 SeaORM MigrationTrait，不知道当前仓库模型自带 auto_migrate()
❌ 误以为 schema sync 会修改列类型或删除旧字段
❌ 把联合普通索引误写成 `unique_key`，改变业务唯一性
❌ 在 install 中重复创建 entity 属性已经声明的索引
❌ `belongs_to` 遗漏 `skip_fk`，让 schema sync 创建外键
❌ 以为增加 `skip_fk` 会自动删除已有数据库外键
❌ 在业务 migrate 中逐个调用 Model::add_col_comment()
```

## 正确做法

```text
✅ 业务迁移只由 XxxInstall::migrate()/migrate_with() 暴露
✅ 官方 sync 负责单列索引和联合唯一索引，install 只补无法由属性表达的索引
✅ 破坏性 schema 变更使用显式 migration
✅ 索引命名保持短而稳定
✅ relation 用于查询建模，数据库外键保持禁用
✅ 外键字段由业务层校验并通过事务维护一致性
✅ crate 级迁移用 sync_schema_with_comments() 统一同步 Schema 与备注
```
