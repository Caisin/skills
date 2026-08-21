# KX Sea ORM Schema Design

用于 `kx-sea-orm` 的数据库字段、主键、索引与软删除设计规范。

## 适用场景

- 新建表结构前先定字段
- 需要决定主键、联合主键、索引和软删除规则
- 需要兼容 SQLite / PostgreSQL / MySQL 等多种数据库

## 推荐模板

```rust
#[sea_orm::model]
#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(
    table_name = "sys_user",
    comment = "用户表",
    model_attrs(derive(Sea))
)]
pub struct Model {
    /// 主键：普通业务表优先 i64
    #[sea_orm(primary_key)]
    pub id: i64,
    /// 用户 ID 缩写字段
    #[sea_orm(indexed)]
    pub uid: i64,
    /// 业务状态
    #[sea_orm(indexed)]
    pub state: i32,
    /// 软删除标记
    #[sea_orm(indexed)]
    pub is_del: bool,
    /// JSON 配置
    pub ext: Json,
    pub created_at: i64,
    pub updated_at: i64,
    pub deleted_at: Option<i64>,
}

impl ActiveModelBehavior for ActiveModel {}
```

关系拥有侧使用 `skip_fk`，保留 relation 元数据但不生成数据库外键：

```rust
#[sea_orm::model]
#[derive(Clone, Debug, PartialEq, DeriveEntityModel, Eq)]
#[sea_orm(table_name = "sys_user", model_attrs(derive(Sea)))]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub dept_id: i64,
    #[sea_orm(belongs_to, from = "dept_id", to = "id", skip_fk)]
    pub dept: BelongsTo<super::sys_dept::Entity>,
}
```

```rust
pub async fn migrate<C: SchemaSyncConnection>(c: &C) -> Result<()> {
    SysUser::auto_migrate(c).await?;

    SysUser::create_index(
        c,
        "idx_usr_uid_state",
        vec![sys_user::Column::Uid, sys_user::Column::State],
    )
    .await?;

    SysUser::create_index(
        c,
        "udx_usr_uid_mobile",
        vec![sys_user::Column::Uid, sys_user::Column::Mobile],
    )
    .await?;
    Ok(())
}
```

## 关键约定

```text
- 字段名不要太长，优先用稳定缩写；例如 `uid` 优先于 `user_id`。
- 普通业务表主键不要默认用 UUID；优先 `i64` 这类整数主键。
- 兼容 SQLite 时，数字字段不要用 `u64` / `u32` / `usize`，统一优先 `i64` / `i32`。
- 需要存 JSON 时，字段类型直接用 `Json`，不要退回 `String`。
- 软删除表统一使用 `is_del: bool`，建议同时配 `deleted_at: Option<i64>`。
- `state` / `status` 不能替代 `is_del`；状态字段表达业务状态，`is_del` 只表达删除语义。
- 避免直接使用 SQL / 数据库保留关键字作为字段名，例如：`order`、`group`、`key`、`index`、`table`、`select`、`from`、`desc`。
- 每个表必须有主键。
- 实体使用 `#[sea_orm::model]` + `model_attrs(derive(Sea))`；不要手写空 `Relation`。
- relation 字段使用 `BelongsTo` / `HasOne` / `HasMany`；拥有外键字段的 `belongs_to` 必须声明 `skip_fk`。
- relation 只用于 JOIN、loader 和 Seaography；关联存在性继续由 service 校验，数据库不创建外键。
- 普通业务表优先单整数主键；只有在关系表、桥表、天然联合唯一键场景下，才考虑联合主键。
- 单字段索引优先直接使用 `#[sea_orm(indexed)]`。
- 联合唯一索引让相关字段共享同一 `#[sea_orm(unique_key = "...")]`，由官方 sync 创建。
- dense entity 当前不能用字段属性表达联合普通索引；在 `install.rs` 显式创建，索引名以
  `idx_` 开头。字段需要参与多个联合唯一分组时，额外分组同样显式创建。
```

## 常见错误

```text
❌ 字段名过长，例如默认把每个外键都写成 user_id / department_id / organization_id
❌ 普通业务表默认上 UUID 主键
❌ 兼容 SQLite 的表里使用 u64 / u32 作为持久化字段
❌ 需要存 JSON 却用 String 保存原始 JSON 文本
❌ 软删表没有 is_del / deleted_at 组合
❌ 联合索引名字过长，难读也难维护
❌ 把 `state` 当成删除标志用
❌ `belongs_to` 遗漏 `skip_fk`，让实体迁移创建数据库外键
```

## 正确做法

```text
✅ 字段命名优先短而统一，例如 uid / dept_id / app_id
✅ 普通业务表优先单整数主键，特殊关系表再考虑联合主键
✅ 兼容 SQLite 时优先 i64 / i32
✅ JSON 字段直接使用 Json 类型
✅ 软删除表统一用 is_del 表达删除语义
✅ 索引命名保持 idx_/udx_ 规则，且尽量简短
✅ relation 拥有侧使用 skip_fk，并由 service + 事务维护关联一致性
```
