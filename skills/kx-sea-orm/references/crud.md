# KX Sea ORM CRUD

用于 `kx-sea-orm` 的标准新增、查询、分页、更新与软删除模板。

## 适用场景

- 标准新增、按主键查、分页列表、更新、软删除
- 想展示 `get / sel / qry / m / update_set` 的边界

## 推荐模板

### 新增

```rust
pub async fn create_user<C: ConnectionTrait>(c: &C, name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    let now = kx_tools::times::sys_time_ts();
    SysDept::get(c, dept_id).await?;

    let mut m = SysUser::m();
    m.set_name(name)
        .set_mobile(mobile)
        .set_dept_id(dept_id)
        .set_is_del(false)
        .set_created_at(now)
        .set_updated_at(now);
    m.upsert(c).await
}
```

### 主键查询 / 条件查询

```rust
pub async fn get_user<C: ConnectionTrait>(c: &C, id: i64) -> Result<sys_user::Model> {
    SysUser::get(c, id).await
}

pub async fn get_user_by_mobile<C: ConnectionTrait>(c: &C, mobile: &str) -> Result<Option<sys_user::Model>> {
    SysUser::sel().mobile_eq(mobile).is_del_eq(false).one_opt(c).await
}
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
    let now = kx_tools::times::sys_time_ts();
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

### 软删除

```rust
pub async fn delete_user<C: ConnectionTrait>(c: &C, id: i64) -> Result<()> {
    let now = kx_tools::times::sys_time_ts();
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
- 主键冲突时插入或更新使用 upsert()；不要把它写成 save()。
- ActiveModelTrait::save 保留 SeaORM 原生的按主键状态 insert/update 语义。
- 软删表默认补 is_del_eq(false)。
```

## 常见错误

```text
❌ 忽略 derive 生成的 qry/sel/m/get，退回 Entity::find() / ActiveModel 大段手写
❌ 分页查询忘记 desc_id()，翻页结果不稳定
❌ 软删表没有 is_del_eq(false)
❌ 保存时不补 created_at / updated_at / set_default 语义
❌ 把 KX 冲突更新和 SeaORM ActiveModelTrait::save 当成同一种语义
```

## 正确做法

```text
✅ 查询优先用 <T>::get / <T>::sel / <T>::qry / <T>::m()
✅ 分页默认补稳定排序
✅ 软删表默认统一过滤 is_del_eq(false)
✅ 更新与保存语义尽量保持一致且可复用
✅ 需要冲突更新时显式调用 upsert()
```
