# KX Sea ORM CRUD

用于 `kx-sea-orm` 的标准新增、查询、分页、更新与软删除模板。

## 适用场景

- 标准新增、按主键查、分页列表、更新、软删除
- 想展示 `get / sel / qry / m / update_set` 的边界

## 推荐模板

### 新增

```rust
pub async fn create_user<C: ConnectionTrait>(c: &C, name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    let now = kx_tools::times::sys_timestamp();
    SysDept::get(c, dept_id).await?;

    SysUser {
        name,
        mobile,
        dept_id,
        is_del: false,
        created_at: now,
        updated_at: now,
        ..Default::default()
    }
    .insert(c)
    .await
}
```

创建接口使用 `insert`，让重复主键或唯一键按数据库约束失败。只有调用方明确要求
“不存在则创建、存在则覆盖”时才使用 `upsert`。

### 主键查询 / 条件查询

```rust
pub async fn get_user<C: ConnectionTrait>(c: &C, id: i64) -> Result<sys_user::Model> {
    SysUser::get(c, id).await
}

pub async fn get_user_by_mobile<C: ConnectionTrait>(c: &C, mobile: &str) -> Result<Option<sys_user::Model>> {
    SysUser::sel().mobile_eq(mobile).is_del_eq(false).one_opt(c).await
}
```

业务代码使用实体业务别名，不展开模块全路径，也不手写静态 `Column::Field`：

```rust
let lots = AstLot::qry()
    .acct_id_eq(req.acct_id)
    .asset_item_id_eq(req.asset_item_id)
    .state_eq(AssetLotState::Active)
    .all(tx)
    .await?;
```

需要连续多个排序条件时使用 `sel()`：

```rust
let lots = AstLot::sel()
    .acct_id_eq(req.acct_id)
    .asc_expires_at()
    .asc_id()
    .all(tx)
    .await?;
```

### 分页查询

```rust
pub async fn page_users<C: ConnectionTrait>(c: &C, dept_id: Option<i64>, paging: Paging) -> Result<Page<sys_user::Model>> {
    let mut qry = SysUser::qry().is_del_eq(false);
    if let Some(dept_id) = dept_id {
        qry = qry.dept_id_eq(dept_id);
    }
    if !qry.has_order() {
        qry.desc_id();
    }
    qry.page(c, paging).await
}
```

### 更新

```rust
pub async fn rename_user<C: ConnectionTrait>(c: &C, id: i64, name: String) -> Result<()> {
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

已经加载完整模型、主键确定且业务允许覆盖时，直接修改模型并调用业务 alias 的
`upsert`，不需要转成 `ActiveModel` 再调用 `update`：

```rust
pub async fn replace_user_name<C: ConnectionTrait>(c: &C, id: i64, name: String) -> Result<sys_user::Model> {
    let mut user = SysUser::get(c, id).await?;
    user.name = name;
    user.updated_at = kx_tools::times::sys_timestamp();
    user.upsert(c).await
}
```

复合主键全部已知的配置或 binding 可以直接构造完整 `Model` 后 `upsert`，无需先查询
目标行。批量覆盖使用 `Alias::upsert_many`，避免逐行往返。

### 软删除

```rust
pub async fn delete_user<C: ConnectionTrait>(c: &C, id: i64) -> Result<()> {
    let now = kx_tools::times::sys_timestamp();
    SysUser::qry()
        .id_eq(id)
        .is_del_eq(false)
        .update_set(c, |m| {
            m.set_is_del(true)
                .set_deleted_at(now)
                .set_updated_at(now);
        })
        .await?;
    Ok(())
}
```

## 关键点

```text
- 主键查询优先 get()。
- 简单条件查优先 sel()。
- 分页 / 排序 / 批量更新优先 qry()。
- 更新构造优先 m() 或 update_set()。
- 完整 Model、主键已知且允许覆盖时使用 upsert()；批量覆盖使用 upsert_many()。
- upsert() 的冲突目标是主键；不要假设它会按任意自然唯一键更新。
- 创建时必须拒绝重复、数据库生成主键、不可变流水、审计/安全事件时使用 insert()。
- 乐观锁、lease、fencing、claim 和依赖数据库状态前置条件的转换使用带条件的
  update_many()/update_set()，不能用 upsert() 绕过并发条件。
- ActiveModelTrait::save 保留 SeaORM 原生的按主键状态 insert/update 语义。
- 软删表默认补 is_del_eq(false)。
- 业务静态查询优先 Alias::get/qry/sel；不要展开成 module::Entity::find() + module::Column::Field。
- 聚合投影、运行时字段排序、复合 Condition、批量更新和 CAS 可保留底层 SeaORM builder。
```

## 常见错误

```text
❌ 忽略 derive 生成的 qry/sel/m/get，退回 Entity::find() / ActiveModel 大段手写
❌ 分页查询忘记 desc_id()，翻页结果不稳定
❌ 软删表没有 is_del_eq(false)
❌ 保存时不补 created_at / updated_at / set_default 语义
❌ 把 KX 冲突更新和 SeaORM ActiveModelTrait::save 当成同一种语义
❌ 把自然唯一键当作 generated upsert 的冲突目标
❌ 用 upsert 绕过 version、lease、fencing 或状态前置条件
```

## 正确做法

```text
✅ 查询优先用 <T>::get / <T>::sel / <T>::qry / <T>::m()
✅ 分页默认补稳定排序
✅ 软删表默认统一过滤 is_del_eq(false)
✅ 更新与保存语义尽量保持一致且可复用
✅ 主键覆盖写显式调用 upsert()，创建和条件更新保留各自语义
```
