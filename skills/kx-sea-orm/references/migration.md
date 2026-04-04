# KX Sea ORM Migration

用于 `kx-sea-orm` 的建表、补字段与索引创建模板。

## 适用场景

- 需要给实体补建表/补字段
- 需要给实体补索引
- 需要展示当前仓库推荐的 migrate 入口

## 推荐模板

```rust
use anyhow::Result;
use sea_orm::ConnectionTrait;

use super::{sys_dept::SysDept, sys_user::SysUser};

pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
    SysDept::auto_migrate(c).await?;
    SysUser::auto_migrate(c).await?;

    SysUser::create_index(c, "idx_usr_dept", vec![sys_user::Column::DeptId]).await?;
    SysUser::create_index(c, "idx_usr_mobile", vec![sys_user::Column::Mobile]).await?;
    Ok(())
}
```

```rust
pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
    account::migrate(c).await?;
    order::migrate(c).await?;
    log::migrate(c).await?;
    Ok(())
}
```

## 关键点

```text
- auto_migrate() 来自 derives/codegen 的生成逻辑。
- 它适合“表不存在则建表、字段缺失则补字段”的常规场景。
- 索引继续用 Model::create_index() / create_index_statement()。
- 联合索引名尽量简短，普通索引用 idx_，唯一索引用 udx_。
- 本 reference 默认不展示 relation foreign key migration。
```

## 常见错误

```text
❌ 只会手写 SeaORM MigrationTrait，不知道当前仓库模型自带 auto_migrate()
❌ 联合索引命名过长
❌ 用 relation 去表达外键迁移
```

## 正确做法

```text
✅ 迁移优先用 auto_migrate() + create_index()
✅ 索引命名保持短而稳定
✅ 外键语义保持普通字段 + 业务层保证一致性
```
