# KX Sea ORM Patterns

用于 `kx-sea-orm` 的六段式示例模板。

> 说明：下面凡是提到 `ents/`、`bizs/`、`bins/` 的地方，都属于**下游业务仓库约定**，不是当前工作区事实。
>
> 本 reference 默认遵守：**禁止使用 SeaORM relation 做外键**。也就是不使用 `belongs_to` / `has_many` / `find_with_related`；统一改用普通字段 + service 校验 + 事务。

## 先记住这几条

1. Alias 来自 `#[sea_orm(table_name = "...")]` 的表名转 PascalCase。
   - 例如 `sys_user` -> `SysUser`
   - `sys_dept` -> `SysDept`
2. `derives/codegen/src/table/sea` 已经给模型生成了：
   - `get()` / `get_opt()` / `exists()`
   - `sel()` / `qry()` / `m()`
   - `auto_migrate()` / `create_index()`
   - `ModifyModel::save()` / `update()` / `insert()`
3. 多表场景不要先想 relation，先想：
   - 关联字段是什么
   - 是否要先校验关联记录存在
   - 读路径是两段查询还是事务写入
4. 软删表默认补 `is_del_eq(false)`；分页默认补稳定排序。

---

## 1. 模型定义

### 适用场景

- 需要写实体模型示例
- 需要示范手工外键字段（如 `dept_id`）
- 需要明确 relation 为空

### 推荐模板

```rust
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Sea, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(table_name = "sys_dept", comment = "部门表")]
pub struct Model {
    /// 部门ID
    #[sea_orm(primary_key)]
    pub id: i64,
    /// 部门名称
    #[sea_orm(indexed)]
    pub name: String,
    /// 是否删除
    #[sea_orm(indexed)]
    pub is_del: bool,
    /// 创建时间
    pub created_at: i64,
    /// 更新时间
    pub updated_at: i64,
    /// 删除时间
    pub deleted_at: Option<i64>,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

```rust
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Sea, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(table_name = "sys_user", comment = "用户表")]
pub struct Model {
    /// 用户ID
    #[sea_orm(primary_key)]
    pub id: i64,
    /// 用户名
    #[sea_orm(indexed)]
    pub name: String,
    /// 手机号
    #[sea_orm(indexed)]
    pub mobile: String,
    /// 部门ID：这里只是普通字段，不使用 relation 建外键
    #[sea_orm(indexed)]
    pub dept_id: i64,
    /// 是否删除
    #[sea_orm(indexed)]
    pub is_del: bool,
    /// 创建时间
    pub created_at: i64,
    /// 更新时间
    pub updated_at: i64,
    /// 删除时间
    pub deleted_at: Option<i64>,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

### 关键点

```text
- dept_id 是普通字段，不是 SeaORM relation。
- Relation 维持空枚举即可。
- 只要 table_name 正确，宏就会生成 SysDept / SysUser / SysUserQry / SysUserModify 等能力。
```

---

## 2. 迁移

### 适用场景

- 需要给实体补建表/补字段
- 需要给实体补索引
- 需要展示当前仓库推荐的 migrate 入口

### 推荐模板

当前仓库里，实体模型已经生成了 `auto_migrate()` 和 `create_index()`，因此迁移优先用下面这种方式：

```rust
use anyhow::Result;
use sea_orm::ConnectionTrait;

use super::{sys_dept::SysDept, sys_user::SysUser};

pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
    SysDept::auto_migrate(c).await?;
    SysUser::auto_migrate(c).await?;

    SysUser::create_index(c, "idx_sys_user_dept_id", vec![sys_user::Column::DeptId]).await?;
    SysUser::create_index(c, "idx_sys_user_mobile", vec![sys_user::Column::Mobile]).await?;
    Ok(())
}
```

如果某个库需要按模块分开迁移，保持 `prelude.rs` 汇总入口即可：

```rust
pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
    account::migrate(c).await?;
    order::migrate(c).await?;
    log::migrate(c).await?;
    Ok(())
}
```

### 关键点

```text
- auto_migrate() 来自 derives/codegen/src/table/sea/sea_entity.rs 和 sea_model.rs 的生成逻辑。
- 它适合“表不存在则建表、字段缺失则补字段”的常规场景。
- 索引继续用 Model::create_index() / create_index_statement()，不要为了简单场景先回退到整套 MigrationTrait。
- 本 skill 默认不展示 relation foreign key migration。
```

---

## 3. 通用增删改查

### 适用场景

- 标准新增、按主键查、分页列表、更新、软删除
- 想展示 `get / sel / qry / m / update_set` 的边界

### 推荐模板

#### 3.1 新增

```rust
use anyhow::Result;
use sea_orm::ConnectionTrait;

use crate::entity::{sys_dept::SysDept, sys_user::SysUser};

pub async fn create_user<C: ConnectionTrait>(c: &C, name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    let now = kx_tools::times::sys_time_ts();

    // 手工外键校验：不依赖 relation。
    SysDept::get(c, dept_id).await?;

    let mut m = SysUser::m();
    m.set_name(name)
        .set_mobile(mobile)
        .set_dept_id(dept_id)
        .set_is_del(false)
        .set_created_at(now)
        .set_updated_at(now);

    let ret = m.save(c).await?;
    Ok(ret)
}
```

#### 3.2 主键查询 / 条件查询

```rust
pub async fn get_user<C: ConnectionTrait>(c: &C, id: i64) -> Result<sys_user::Model> {
    let user = SysUser::get(c, id).await?;
    Ok(user)
}

pub async fn get_user_by_mobile<C: ConnectionTrait>(c: &C, mobile: &str) -> Result<Option<sys_user::Model>> {
    SysUser::sel()
        .mobile_eq(mobile)
        .is_del_eq(false)
        .one_opt(c)
        .await
}
```

#### 3.3 分页查询

```rust
use kx_sea_common::Page;
use kx_tools::page::Paging;

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

#### 3.4 更新

```rust
pub async fn rename_user<C: ConnectionTrait>(c: &C, id: i64, name: String) -> Result<()> {
    let now = kx_tools::times::sys_time_ts();

    SysUser::qry()
        .id_eq(id)
        .is_del_eq(false)
        .update_set(c, |m| {
            m.set_name(name.clone())
                .set_updated_at(now);
        })
        .await?;
    Ok(())
}
```

#### 3.5 软删除

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

### 关键点

```text
- 主键查询优先 get()。
- 简单条件查优先 sel()。
- 分页 / 排序 / 批量更新优先 qry()。
- 更新构造优先 m() 或 update_set()。
- 软删表默认补 is_del_eq(false)。
```

---

## 4. 事务

### 适用场景

- 同一数据源里跨多张表写入
- 需要手工外键校验 + 落库保持一致

### 推荐模板

> 下面示例属于**下游业务仓库约定**：通常会在 `lib.rs` 注册 `ext_db_trait!`，从而得到 `SeaTransExt`。

```rust
pub use kx_ents_sys::entity as ents;
kx_sea_orm::ext_db_trait!(sys);
```

```rust
use anyhow::Result;
use crate::SeaTransExt;
use kx_sea_orm::SeaTrans;
use crate::ents::{sys_dept::SysDept, sys_user::SysUser};

pub async fn create_user_with_dept_check(name: String, mobile: String, dept_id: i64) -> Result<sys_user::Model> {
    SeaTrans::new()
        .transaction(|tx| {
            Box::pin(async move {
                let c = tx.sys().await?;
                let now = kx_tools::times::sys_time_ts();

                // 先校验部门存在，再写用户。
                SysDept::qry().id_eq(dept_id).is_del_eq(false).one(c).await?;

                let mut m = SysUser::m();
                m.set_name(name.clone())
                    .set_mobile(mobile.clone())
                    .set_dept_id(dept_id)
                    .set_is_del(false)
                    .set_created_at(now)
                    .set_updated_at(now);

                let user = m.save(c).await?;
                Ok(user)
            })
        })
        .await
}
```

### 关键点

```text
- 事务边界集中放在 svc，不要散在 ctl/handler。
- 先做手工外键校验，再落库。
- 不使用 relation 也不影响事务一致性；一致性由 SeaTrans + service 顺序保证。
```

---

## 5. 多数据源操作示例

### 适用场景

- 主业务库 + 日志库
- 主库写业务数据，另一个库记审计/操作日志

### 推荐模板

```rust
pub use kx_ents_base::entity as base_ents;
pub use kx_ents_log::entity as log_ents;
kx_sea_orm::ext_db_trait!(base, log);
```

```rust
use anyhow::Result;
use crate::SeaTransExt;
use kx_sea_orm::SeaTrans;
use base_ents::sys_user::SysUser;
use log_ents::op_log::OpLog;

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
                    .set_req_host("admin".to_string())
                    .set_uri_path("/sys/user/create".to_string())
                    .set_method("POST".to_string())
                    .set_ip("127.0.0.1".to_string())
                    .set_ua("internal".to_string())
                    .set_op_day(20260403)
                    .set_in_time(now)
                    .set_use_time(0)
                    .set_done_time(now)
                    .set_qry_param("".to_string())
                    .set_body(serde_json::json!({"user_id": saved.id, "dept_id": dept_id}))
                    .set_resp(serde_json::json!({"ok": true}))
                    .set_resp_code(0)
                    .set_http_status(200);
                op.save(log).await?;

                Ok(())
            })
        })
        .await
}
```

### 关键点

```text
- SeaTrans 天然支持一次事务里打开多个数据源事务句柄。
- 读写哪个库，用 tx.get_dbs([...]) / tx.xxx().await? 显式拿连接。
- 多库示例同样不需要 relation；跨库一致性靠 SeaTrans 成功提交 / 失败回滚。
```

---

## 6. 多表操作示例

### 适用场景

- 想查“用户 + 部门名”这类组合视图
- 不能用 relation，想看手工两段查询怎么写

### 推荐模板

```rust
use std::collections::HashMap;

use anyhow::Result;
use kx_sea_common::Page;
use kx_tools::page::Paging;
use sea_orm::ConnectionTrait;

use crate::entity::{sys_dept::SysDept, sys_user::SysUser};

#[derive(Debug, Clone)]
pub struct UserWithDept {
    pub user: sys_user::Model,
    pub dept_name: Option<String>,
}

pub async fn page_users_with_dept<C: ConnectionTrait>(c: &C, paging: Paging) -> Result<Page<UserWithDept>> {
    let mut qry = SysUser::qry().is_del_eq(false);
    if !qry.has_order() {
        qry.desc_id();
    }

    let page = qry.page(c, paging).await?;

    let dept_ids = page
        .list
        .iter()
        .map(|user| user.dept_id)
        .collect::<Vec<_>>();

    let dept_map = if dept_ids.is_empty() {
        HashMap::new()
    } else {
        SysDept::qry()
            .id_is_in(dept_ids)
            .is_del_eq(false)
            .all(c)
            .await?
            .into_iter()
            .map(|dept| (dept.id, dept.name))
            .collect::<HashMap<_, _>>()
    };

    let list = page
        .list
        .into_iter()
        .map(|user| UserWithDept {
            dept_name: dept_map.get(&user.dept_id).cloned(),
            user,
        })
        .collect::<Vec<_>>();

    Ok(Page {
        list,
        total: page.total,
        page_no: page.page_no,
        page_size: page.page_size,
    })
}
```

如果是多表写入，也优先显式事务：

```rust
pub async fn move_user_to_dept<C: ConnectionTrait>(c: &C, user_id: i64, new_dept_id: i64) -> Result<()> {
    SysDept::qry().id_eq(new_dept_id).is_del_eq(false).one(c).await?;

    let now = kx_tools::times::sys_time_ts();
    SysUser::qry()
        .id_eq(user_id)
        .is_del_eq(false)
        .update_set(c, |m| {
            m.set_dept_id(new_dept_id)
                .set_updated_at(now);
        })
        .await?;
    Ok(())
}
```

### 关键点

```text
- 多表读优先两段式：主表 -> 收集 IDs -> 批量查从表 -> 内存组装。
- 多表写优先先校验、再 update/insert。
- 不用 relation 也能把一对多、多对一和桥表场景写清楚。
```

---

## 常见错误

```text
❌ 把 dept_id 写成 relation，然后到处 find_with_related()
❌ 多表读取只会 N+1 一条条查
❌ 分页查询忘记 desc_id()，翻页结果不稳定
❌ 软删表没有 is_del_eq(false)
❌ 明明是多库事务，却分散在多个函数里手动提交
```

## 正确做法

```text
✅ 外键字段就是普通字段，关联一致性在 service 层保证
✅ 查询优先复用 derive 生成的 get / sel / qry / m
✅ 多表读取优先批量 is_in + HashMap 组装
✅ 多表写和多库写都用 SeaTrans 收口
✅ 迁移优先用 auto_migrate() + create_index()
```
