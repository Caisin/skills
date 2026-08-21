# Write Svc Patterns

## Query Through Domain Aliases

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

动态排序、聚合投影、复合 `Condition`、批量更新和 CAS 可以使用底层 SeaORM builder；不要机械替换动态 `Column`。

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

`update_set` 适合按主键、软删状态或其它业务条件做局部字段更新。version/CAS、lease、fencing、claim 等并发控制还必须把预期状态放进条件，并校验影响行数；当前 `update_set` 只返回 `Result<()>` 时，应使用能返回 `UpdateResult` 的底层条件更新完成该校验。

## Choose Write Semantics

```text
insert       -> 新建、数据库生成主键、不可变流水、审计/安全事件
upsert       -> 完整 Model、主键已知、业务允许覆盖
upsert_many  -> 多条完整 Model 的主键覆盖写
update_set   -> 按 alias query 条件局部更新普通业务字段
底层条件更新 -> 需要校验影响行数的 version/CAS、lease、fencing、claim、状态机转换
```

```rust
let mut item = AstItem::get(db, id).await?;
item.name = name;
item.updated_at = kx_tools::times::sys_timestamp();
item.upsert(db).await?;
```

自然唯一键不是 generated upsert 的冲突目标。需要按自然键创建时，先按业务语义选择拒绝重复，或显式构造 `OnConflict`。

## Transaction Shape

```rust
use crate::SeaTransExt as _;
use kx_sea_orm::SeaTrans;

SeaTrans::t(|trans| {
    Box::pin(async move {
        let tx = trans.asset().await?;
        validate(&req)?;
        let row = write_primary(tx, &req).await?;
        write_ledger(tx, &row).await?;
        enqueue_outbox(tx, &row).await?;
        Ok(row)
    })
})
.await
```

`SeaTrans::t` 统一处理成功提交和失败回滚；需要让调用方区分领域错误与数据库错误时使用 `SeaTrans::sea_trans`。事务必须覆盖所有需要原子提交的数据库写入。远端 SDK 调用通常不放在长事务内，使用 outbox、任务或可重试状态机衔接。

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

## 常见错误

```text
❌ 先读取 version，再无条件 upsert
❌ 手写 begin/commit/rollback，重复实现 SeaTrans 的控制流
❌ 对不可变流水或审计记录做覆盖写
❌ 分页查询没有稳定排序
❌ 把外部 SDK 调用放进长数据库事务
```

## 正确做法

```text
✅ CAS 和状态机使用带前置条件的更新
✅ 使用 SeaTrans::t 或 SeaTrans::sea_trans 统一事务控制流
✅ 不可变记录使用 insert
✅ 分页和批处理提供稳定排序
✅ 用 outbox 或可重试任务衔接外部副作用
```
