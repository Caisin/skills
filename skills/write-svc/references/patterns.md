# Write Svc Patterns

## Query Through Domain Aliases

这里的 alias、`qry/sel/get/get_opt`、字段条件链、`update_set`、`insert/upsert/upsert_many` 和
ActiveModel 的 `set_<field>` 均由 entity 的 `model_attrs(derive(Sea))` 生成。业务 service 直接使用，
不要为了“统一入口”再包一层无业务规则的 CRUD service。旧公共 API 所需语义 alias 可以保留，
新代码默认使用表名生成 alias。

```rust
let lots = AstLot::sel()
    .acct_id_eq(req.acct_id)
    .asset_item_id_eq(req.asset_item_id)
    .state_eq(AssetLotState::Active)
    .asc_expires_at()
    .asc_id()
    .all(tx)
    .await?;
```

前端动态排序优先使用生成的 `sort/sort_or`，由实体 `Column::from_str` 校验字段：

```rust
let page = AstItem::sel()
    .enabled_eq(true)
    .sort_or(query.sort.as_deref(), query.descending, |s| {
        s.asc_spend_priority()
    })
    .asc_id()
    .page(db, paging)
    .await?;
```

`sort` 在排序字段为空或非法时不追加排序；`sort_or` 此时执行类型化 fallback，适合分页默认排序。
二者都只接受当前实体可解析的列，不能把前端字符串直接拼入 SQL。若接口直接使用生成的 Query，
也可通过 `_order_by[asc]=id` / `_order_by[desc]=created_at` 传递 `OrderBy`。分页仍要追加主键作为
稳定次级排序。

聚合投影、复合 `Condition`、批量更新和 CAS 可以使用底层 SeaORM builder。接口需要字段别名或
对非法排序返回稳定错误时，可以保留显式排序白名单。

表名决定生成 alias，例如 `msg_evt -> MsgEvt`、`ast_lot -> AstLot`。若旧业务名称与表名不同，迁移时
优先改调用方使用生成 alias；只有公共 API 兼容有明确必要时才保留独立语义类型，不能用手写 alias
掩盖命名差异。

## Conditional Update With update_set

局部更新不需要先读取完整 Model。通过 alias query 收口更新条件，并在闭包中只设置允许修改的字段：

```rust
pub async fn rename_user<C: ConnectionTrait>(
    c: &C,
    id: i64,
    name: String,
) -> Result<()> {
    let now = kx_tools::times::sys_timestamp();
    SysUser::qry()
        .id_eq(id)
        .is_del_eq(false)
        .update_set(c, |m| {
            m.set_name(name.clone()).set_updated_at(now);
        })
        .await?;
    Ok(())
}
```

`update_set` 适合按主键、软删状态或其它业务条件做局部字段更新，并返回 SeaORM
`UpdateResult`。version/CAS、lease、fencing、claim 等并发控制必须把预期状态放进条件，并校验
`rows_affected == 1`；不满足时返回稳定并发冲突错误。

字段条件使用规范后缀：`_gte/_gt/_lte/_lt/_in/_not_in/_between/_not_between`、
`_starts_with/_ends_with/_is_not_null`。旧缩写方法已从宏移除，业务代码不得自行补兼容 trait。
`qry()` 的每个字段只能保存一个条件；同字段范围优先 `_between`，更复杂的 AND/OR 组合使用
`sel().to_select()` 或 SeaORM builder。

## Choose Write Semantics

```text
insert       -> 新建、数据库生成主键、不可变流水、审计/安全事件
upsert       -> 完整 Model、主键已知、业务允许覆盖
upsert_many  -> 多条完整 Model 的主键覆盖写
update_set   -> 按 alias query 条件局部更新普通业务字段
update_set   -> 可直接校验影响行数的 version/CAS、lease、fencing、claim、状态机转换
```

```rust
let mut item = AstItem::get(db, id).await?;
item.name = name;
item.updated_at = kx_tools::times::sys_timestamp();
item.upsert(db).await?;
```

自然唯一键不是 generated upsert 的冲突目标。需要按自然键创建时，先按业务语义选择拒绝重复，或显式构造 `OnConflict`。

已加载记录转换成 `ActiveModel` 后，SeaORM 原生 `update` 只提交已设置字段，适合普通局部更新。
不要机械替换为可能在记录缺失时插入的 `upsert`。CAS 仍必须使用带条件且可检查影响行数的更新。

## Default Model Fields

实体已 `derive(Default)`，且可选字段的 `None`、计数的 `0`、开关的 `false` 就是统一初始状态时，省略重复初始化：

```rust
let run = TaskRun {
    run_key,
    executor_code,
    status: TaskRunStatus::Queued,
    scheduled_at: now,
    queued_at: now,
    updated_at: now,
    message: "任务已进入队列".to_owned(),
    ..Default::default()
};
```

状态、时间、版本、租约、权限、审计主体和其它会改变业务语义的字段保持显式。请求 DTO 的必填字段不能通过 `Default` 掩盖缺失输入；SeaORM `ActiveModel` 只用 `..Default::default()` 表达剩余字段 `NotSet`。

## Transaction Shape

```rust
use sea_orm::TransactionTrait;

db.transaction(|tx| {
    Box::pin(async move {
        let row = write_primary(tx, &req).await?;
        write_ledger(tx, &row).await?;
        Ok(row)
    })
})
.await?;
```

单数据源直接使用 SeaORM transaction helper。需要从注册 alias 获取事务或协调多个数据源时使用
`SeaTrans::t/sea_trans`；多个数据源只按顺序提交，是 best-effort 而非分布式原子事务。远端 SDK
调用通常不放在长事务内，使用 outbox、任务或可重试状态机衔接。

## Optimistic Concurrency

```text
UPDATE item
SET value = ?, version = version + 1
WHERE id = ? AND version = ?
```

影响行数不是 1 时返回稳定并发冲突错误。禁止先读 version 后无条件 upsert。

## Multi-table Reads

列表查询优先：

1. 主表按稳定顺序分页；
2. 收集本页关联 ID；
3. 批量查询从表；
4. 在 service 内组装 DTO/view。

明确的一对一类型化 JOIN 或 loader 可以使用 relation；不要逐行查询制造 N+1。

## Data Source Aliases

业务 crate 在根模块声明自己使用的数据源：

```rust
kx_sea_orm::ext_db_trait!(asset);
```

实际调用模块导入：

```rust
use crate::SeaOrmExt as _;
```

只有真实跨库调用才声明多个 alias。单 alias 通过 `SeaTrans` 获取的仍是普通数据库事务；多个 alias 按顺序提交，不提供分布式原子性。

## File Boundary

业务实现文件最多 1000 行。按稳定子域拆分，跨子域 helper 使用最小的 `pub(super)` 可见性；
`svc/mod.rs` 只声明模块与重导出公共 service。不得用 `include!` 保留单一巨型模块，也不得为了拆行数
把一个函数或事务任意截断到多个文件。

## 常见错误

```text
❌ 先读取 version，再无条件 upsert
❌ 手写 begin/commit/rollback，或把单库事务误写成跨库协调
❌ 对不可变流水或审计记录做覆盖写
❌ 分页查询没有稳定排序
❌ 把外部 SDK 调用放进长数据库事务
❌ 为 `derive(Sea)` 已生成的 Query、setter、CRUD 再建无业务逻辑 wrapper
❌ 在无需别名/错误契约时重复排序 match，或把排序字段直接拼 SQL
```

## 正确做法

```text
✅ CAS 和状态机使用带前置条件的更新
✅ 单库用 SeaORM transaction helper；alias/跨库协调使用 SeaTrans
✅ 不可变记录使用 insert
✅ 分页和批处理提供稳定排序
✅ 前端排序使用 `sort/sort_or`，默认排序用类型化 fallback
✅ 用 outbox 或可重试任务衔接外部副作用
```
