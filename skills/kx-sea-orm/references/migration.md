# KX Sea ORM Migration

用于 `kx-sea-orm` 的建表、补字段与索引创建模板。

## 适用场景

- 需要给实体补建表/补字段
- 需要给实体补索引
- 需要展示当前仓库推荐的 migrate 入口

## 推荐模板

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
- 它只创建缺失表、列和索引，不修改或删除已有 schema 对象。
- 字段类型、约束修改和删除必须使用显式 migration，并经过发布审查。
- 泛型连接边界使用 SchemaSyncConnection，不重新实现 schema diff。
- 索引继续用 Model::create_index() / create_index_statement()。
- 联合索引名尽量简短，普通索引用 idx_，唯一索引用 udx_。
- relation 拥有侧必须声明 `skip_fk`，让实体建表和 schema sync 跳过数据库外键。
- `skip_fk` 不会删除已有外键；移除旧约束仍需显式 migration。
```

## 常见错误

```text
❌ 只会手写 SeaORM MigrationTrait，不知道当前仓库模型自带 auto_migrate()
❌ 误以为 schema sync 会修改列类型或删除旧字段
❌ 联合索引命名过长
❌ `belongs_to` 遗漏 `skip_fk`，让 schema sync 创建外键
❌ 以为增加 `skip_fk` 会自动删除已有数据库外键
```

## 正确做法

```text
✅ 迁移优先用 auto_migrate() + create_index()
✅ 破坏性 schema 变更使用显式 migration
✅ 索引命名保持短而稳定
✅ relation 用于查询建模，数据库外键保持禁用
✅ 外键字段由业务层校验并通过事务维护一致性
```
