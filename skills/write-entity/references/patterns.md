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
    model_attrs(
        derive(Sea),
        kx(index(
            name = "idx_job_outbox_state_updated_at",
            columns(state, updated_at)
        ))
    )
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

## `derive(Sea)` 已生成的契约

`model_attrs(derive(Sea))` 会根据 `table_name` 的 UpperCamelCase 名称生成业务 alias。例如
`msg_evt` 生成 `MsgEvt`，`ast_lot` 生成 `AstLot`。不要再手写：

```rust
// 错误：宏已经生成表名对应的 Model alias。
pub type DeviceEvent = Model;
```

每个 dense entity 当前自动提供：

```text
<TableName>       -> Model
<TableName>Qry    -> Query
<TableName>Modify -> ModifyModel
<TableName>Entity -> Entity
<TableName>Col    -> Column
PkType            -> 主键值类型
COLUMN            -> SeaORM 2 强类型列常量
```

同时生成以下常用能力，新增 entity 或迁移旧 ORM 时先复用，禁止重复包装同名逻辑：

```text
Model::get/get_opt/exists/del/del_by_ids
Model::qry/sel/m/e
Model::insert/upsert/upsert_many/upsert_many_statement
Entity::get/get_opt/page/upsert/upsert_many/insert_many_do_nothing
Query::<field>_eq/ne/gte/gt/lte/lt/in/not_in/between/not_between
Query::<field>_like/contains/not_contains/starts_with/ends_with/is_null/is_not_null
Query::one/one_opt/all/page/count/exists/delete_many/update_set
EntitySelect::<field 条件>/asc_<field>/desc_<field>/sort/sort_or/order_by/limit/offset/distinct
ActiveModel::set_<field>/not_set_<field>
Model::create_index_statement/create_index/exec_idx
Model::col_comments/add_col_comment/auto_migrate
```

`Query::update_set` 返回 SeaORM `UpdateResult`，普通更新可以忽略返回值；CAS、lease、claim、状态机转换
必须检查 `rows_affected`。`_in/_not_in` 接受任意 `IntoIterator`，不要求调用方先构造 `Vec`。
`Qry` 每个字段保存一个条件；同一字段的范围查询使用 `_between`，需要多个独立表达式时改用 `sel()`
或 SeaORM builder，不能连续调用同字段方法并假设条件会累加。

`Query::_order_by` 支持 `_order_by[asc]=id` / `_order_by[desc]=created_at`。兼容前端已有的
`sort + descending` 参数时使用 `EntitySelect::sort`；分页需要默认排序时使用 `sort_or` 的类型化
fallback。两个入口都通过当前实体的 `Column::from_str` 校验字段，非法字段不会进入 SQL。

旧的 `_ge/_g/_le/_l/_is_in/_bt/_not_bt/_start_with/_end_with/_not_null` 不再生成。迁移时直接改为
`_gte/_gt/_lte/_lt/_in/_between/_not_between/_starts_with/_ends_with/_is_not_null`，不要在业务 crate
补兼容 extension trait。

```rust
let lots = AstLot::qry()
    .acct_id_eq(req.acct_id)
    .asset_item_id_eq(req.asset_item_id)
    .state_eq(AssetLotState::Active)
    .all(c)
    .await?;
```

动态复合条件、JOIN/聚合、CAS 影响行数校验等不适合生成 Query 的场景，才直接使用 `Entity`、
`COLUMN` 与 SeaORM builder。普通前端单列排序已由 `sort/sort_or/order_by` 覆盖。宏生成能力是便利
API，不改变 insert/upsert/CAS 的业务语义。

PostgreSQL 专属 `ilike`、array 操作、子查询、聚合投影、JOIN 和锁不统一生成；这些能力的类型与后端
约束差异较大，应从 `Entity::find()` 或 `Alias::sel().to_select()` 下沉到 SeaORM builder。

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
use sea_orm::DatabaseConnection;

pub struct JobInstall;

impl JobInstall {
    pub async fn migrate() -> Result<()> {
        let db = kx_sea_orm::SeaOrms::job().await?;
        Self::migrate_with(&db).await
    }

    pub async fn migrate_with(db: &DatabaseConnection) -> Result<()> {
        db.sync_schema_with_comments("kx-biz-job::entity::*").await?;
        Ok(())
    }
}
```

## Index Boundary

```text
indexed                  -> 单列普通索引，官方 sync
unique                   -> 单列唯一索引，官方 sync
同名 unique_key          -> 联合唯一索引，官方 sync
联合普通索引             -> kx(index(name = "...", columns(...)))
额外联合唯一分组         -> kx(unique_index(name = "...", columns(...)))
表达式/部分/前缀索引     -> install.rs 显式 migration
```

`columns(...)` 使用 Rust 字段名，顺序就是数据库索引列顺序；`column_name` 映射由宏自动处理。
SeaORM 官方 sync 主要按列集合判断缺失，KX 联合索引按显式索引名幂等创建；不要重复声明相同列集合。

## Directory Boundary

```text
src/entity/<subdomain>/*.rs -> 表、枚举和 relation
src/entity/mod.rs           -> 子域声明与稳定重导出
src/install.rs              -> schema sync、备注和属性无法表达的复杂迁移
```

不要创建 `src/entity/prelude.rs` 作为第二套迁移入口。

## 常见错误

```text
❌ 给已写 comment 的表和字段重复保留同义 rustdoc
❌ 用 unique_key 表达联合普通索引
❌ 在 relation 上省略 skip_fk，从而创建数据库外键
❌ 在业务模块中逐表迁移，绕过 XxxInstall
❌ 为宏已生成的 alias、Query、ActiveModel setter、CRUD 或索引 helper 再写一层包装
❌ 已有 `sort/sort_or` 时继续逐字段匹配前端排序参数
```

## 正确做法

```text
✅ 表和持久化字段使用 comment
✅ 联合普通索引在实体 `model_attrs` 的 KX 索引声明中创建并显式固定列顺序
✅ relation 拥有侧声明 skip_fk
✅ 通过 XxxInstall::migrate()/migrate_with() 暴露迁移入口
✅ 先检查 `derive(Sea)` 生成契约，再只补业务特有行为
```
