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

## Choose Write Semantics

```text
insert       -> 新建、数据库生成主键、不可变流水、审计/安全事件
upsert       -> 完整 Model、主键已知、业务允许覆盖
upsert_many  -> 多条完整 Model 的主键覆盖写
条件更新     -> version/CAS、lease、fencing、claim、状态机转换
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
let tx = db.begin().await?;
let result = async {
    validate(&req)?;
    let row = write_primary(&tx, &req).await?;
    write_ledger(&tx, &row).await?;
    enqueue_outbox(&tx, &row).await?;
    Ok(row)
}
.await;

match result {
    Ok(value) => {
        tx.commit().await?;
        Ok(value)
    }
    Err(err) => {
        tx.rollback().await?;
        Err(err)
    }
}
```

事务必须覆盖所有需要原子提交的数据库写入。远端 SDK 调用通常不放在长事务内，使用 outbox、任务或可重试状态机衔接。

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

只有真实跨库调用才声明多个 alias。`SeaTrans` 顺序提交多个数据库连接，不提供分布式原子性。

## 常见错误

```text
❌ 先读取 version，再无条件 upsert
❌ 对不可变流水或审计记录做覆盖写
❌ 分页查询没有稳定排序
❌ 把外部 SDK 调用放进长数据库事务
```

## 正确做法

```text
✅ CAS 和状态机使用带前置条件的更新
✅ 不可变记录使用 insert
✅ 分页和批处理提供稳定排序
✅ 用 outbox 或可重试任务衔接外部副作用
```
