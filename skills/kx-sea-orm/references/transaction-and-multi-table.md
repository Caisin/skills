# KX Sea ORM Transaction And Multi-table

用于 `kx-sea-orm` 的事务、多数据源与多表操作模板。

## 适用场景

- 同一数据源里跨多张表写入
- 主业务库 + 日志库
- 想查“用户 + 部门名”这类组合视图
- 不能用 relation，想看手工两段查询怎么写

## 推荐模板

### 事务

```rust
pub async fn create_user_with_dept_check(name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    SeaTrans::new()
        .transaction(|tx| {
            Box::pin(async move {
                let c = tx.sys().await?;
                let now = kx_tools::times::sys_time_ts();
                SysDept::qry().id_eq(dept_id).is_del_eq(false).one(c).await?;

                let mut m = SysUser::m();
                m.set_name(name.clone())
                    .set_mobile(mobile.clone())
                    .set_dept_id(dept_id)
                    .set_is_del(false)
                    .set_created_at(now)
                    .set_updated_at(now);
                Ok(m.save(c).await?)
            })
        })
        .await
}
```

### 多数据源

```rust
pub async fn create_user_and_log(name: String, mobile: String, dept_id: i64, uid: i64) -> Result<()> {
    SeaTrans::new()
        .transaction(|tx| {
            Box::pin(async move {
                let [base, log] = tx.get_dbs(["base", "log"]).await?;
                let now = kx_tools::times::sys_time_ts();

                let mut user = SysUser::m();
                user.set_name(name.clone())
                    .set_mobile(mobile.clone())
                    .set_dept_id(dept_id)
                    .set_is_del(false)
                    .set_created_at(now)
                    .set_updated_at(now);
                let saved = user.save(base).await?;

                let mut op = OpLog::m();
                op.set_uid(uid)
                    .set_uri_path("/sys/user/create".to_string())
                    .set_method("POST".to_string())
                    .set_created_at(now)
                    .set_default();
                op.save(log).await?;
                let _ = saved;
                Ok(())
            })
        })
        .await
}
```

### 多表读取

```rust
pub async fn page_users_with_dept<C: ConnectionTrait>(c: &C, paging: Paging) -> Result<Page<UserWithDept>> {
    let mut qry = SysUser::qry().is_del_eq(false);
    if !qry.has_order() {
        qry.desc_id();
    }
    let page = qry.page(c, paging).await?;

    let dept_ids = page.list.iter().map(|user| user.dept_id).collect::<Vec<_>>();
    let dept_map = SysDept::qry()
        .id_is_in(dept_ids)
        .is_del_eq(false)
        .all(c)
        .await?
        .into_iter()
        .map(|dept| (dept.id, dept.name))
        .collect::<std::collections::HashMap<_, _>>();

    Ok(Page {
        list: page.list.into_iter().map(|user| UserWithDept {
            dept_name: dept_map.get(&user.dept_id).cloned(),
            user,
        }).collect(),
        total: page.total,
        page_no: page.page_no,
        page_size: page.page_size,
    })
}
```

## 关键点

```text
- 事务边界集中放在 svc，不要散在 ctl/handler。
- 先做手工外键校验，再落库。
- 多表读优先两段式：主表 -> 收集 IDs -> 批量查从表 -> 内存组装。
- 多表写和多库写都优先用 SeaTrans 收口。
- 不使用 relation 也不影响一致性；一致性由 service 顺序与事务保证。
```

## 常见错误

```text
❌ 把多表读取全塞进 relation，而不是显式两段查询
❌ 多表读取只会 N+1 一条条查
❌ 事务逻辑散落在 ctl 和 svc 多处
❌ 明明是多库事务，却分散在多个函数里手动提交
```

## 正确做法

```text
✅ 多表读取优先批量 is_in + HashMap 组装
✅ 多表写和多库写都用 SeaTrans 收口
✅ 外键字段保持普通字段 + service 校验
✅ 一致性靠事务保证，不靠 relation 魔法
```
