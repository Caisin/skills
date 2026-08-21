# KX Sea ORM Transaction And Multi-table

用于 `kx-sea-orm` 的事务、多数据源与多表操作模板。

## 适用场景

- 同一数据源里跨多张表写入
- 主业务库 + 日志库
- 想查“用户 + 部门名”这类组合视图
- 需要在 relation、loader 与手工两段查询之间选择

## 推荐模板

### 事务

```rust
pub async fn create_user_with_dept_check(name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    SeaTrans::new()
        .transaction(|tx| {
            Box::pin(async move {
                let c = tx.sys().await?;
                let now = kx_tools::times::sys_timestamp();
                SysDept::qry().id_eq(dept_id).is_del_eq(false).one(c).await?;

                let mut m = SysUser::m();
                m.set_name(name.clone())
                    .set_mobile(mobile.clone())
                    .set_dept_id(dept_id)
                    .set_is_del(false)
                    .set_created_at(now)
                    .set_updated_at(now);
                m.upsert(c).await
            })
        })
        .await
}
```

### 多数据源

业务 crate 自己声明固定数据源快捷入口，不把业务 alias 追加到 `kx-sea-orm` 的全局列表：

```rust
kx_sea_orm::ext_db_trait!(asset);

// 在实际调用 SeaOrms::asset() / SeaTrans::asset() 的子模块中引入 trait。
use crate::{SeaOrmExt as _, SeaTransExt as _};
```

只有真实跨库调用才在调用方声明多个 alias，例如通知运行器需要访问任务库时使用
`ext_db_trait!(notify, task)`。没有调用事务 alias 的模块不导入 `SeaTransExt`。

```rust
pub async fn create_user_and_log(name: String, mobile: String, dept_id: i64, uid: i64) -> Result<()> {
    SeaTrans::new()
        .transaction(|tx| {
            Box::pin(async move {
                let [base, log] = tx.get_dbs(["base", "log"]).await?;
                let now = kx_tools::times::sys_timestamp();

                let mut user = SysUser::m();
                user.set_name(name.clone())
                    .set_mobile(mobile.clone())
                    .set_dept_id(dept_id)
                    .set_is_del(false)
                    .set_created_at(now)
                    .set_updated_at(now);
                let saved = user.upsert(base).await?;

                let mut op = OpLog::m();
                op.set_uid(uid)
                    .set_uri_path("/sys/user/create".to_string())
                    .set_method("POST".to_string())
                    .set_created_at(now)
                    .set_default();
                op.upsert(log).await?;
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
- 单库多表写可用 SeaTrans 收口并保持数据库事务原子性。
- 多库写仅是按顺序提交的 best-effort 协调，不保证跨库原子性；业务必须设计补偿或幂等重试。
- 业务数据源 alias 由对应业务 crate 使用 `ext_db_trait!` 声明，不进入框架全局 inherent 方法列表。
- relation 只提供查询元数据，不影响一致性边界；一致性由 service 顺序与事务保证。
- 列表分页和复杂组合读取仍优先两段式批量查询；明确的类型化 JOIN、loader 和 Seaography 可使用 relation。
```

## 常见错误

```text
❌ 列表逐行加载 relation，制造 N+1
❌ 把 relation 当成数据库外键或事务保证
❌ 多表读取只会 N+1 一条条查
❌ 事务逻辑散落在 ctl 和 svc 多处
❌ 明明是多库事务，却分散在多个函数里手动提交
❌ 把 SeaTrans 的多库顺序提交当成分布式原子事务
```

## 正确做法

```text
✅ 多表读取优先批量 is_in + HashMap 组装
✅ 多表写和多库写可用 SeaTrans 收口，但明确多库仅为 best-effort
✅ 外键字段保持普通字段 + service 校验
✅ `belongs_to` 声明 `skip_fk`，查询可使用 relation
✅ 一致性靠事务保证，不靠 relation 元数据
```
