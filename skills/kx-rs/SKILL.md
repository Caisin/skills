---
name: kx-rs
description: kx-rs Rust 后端框架开发规范与 CRUD 模板。当进行 Rust 后端开发时使用，包括：(1) 创建/编辑 SeaORM 实体（ents/）(2) 编写业务服务层 CRUD（svc/）(3) 编写控制器和路由（ctl/ + router.rs，aide + axum）(4) 使用 #[derive(Sea)] 自动生成的 Query/Modify/Select (5) 数据库连接与事务处理 (6) 分页查询与软删除 (7) 响应类型 R<T> 与错误处理 AxumErr (8) 外部项目引入 kx 框架包。触发场景：用户提到 kx-rs、kx 框架、SeaORM 实体、CRUD 服务、aide/axum 控制器、R<T> 响应、AxumErr、业务模块开发、kx Cargo.toml 配置。
---

# kx-rs 开发规范

快速使用 kx-rs 框架完成 Rust 后端 CRUD 开发，优先使用 `#[derive(Sea)]` 自动生成的方法。

## 外部项目引入

```toml
# Cargo.toml - 通过统一包引入（推荐）
[dependencies]
kx = { version = "0.1", registry = "hekx", features = ["axum", "tools", "sea-orm", "cache"] }
# 按需启用: "derive-sea", "ents-base", "ents-log", "ed", "global", "tracing", "i18n" 等

# 或单独引入子包
kx-sea-common = { version = "0.1", registry = "hekx" }
kx-sea-orm = { version = "0.1", registry = "hekx" }
kx-axum = { version = "0.1", registry = "hekx" }
kx-tools = { version = "0.1", registry = "hekx", features = ["cvt"] }
```

## 核心速查

### 数据库连接

```rust
// 普通连接
let c = &mut SeaOrms::xxx().await?;

// 事务
SeaTrans::new().transaction(|tx| {
    Box::pin(async move {
        let c = tx.xxx().await?;
        Ok(())
    })
}).await?
```

### CRUD 模板

```rust
// 查询
<T>::get(c, pk).await?                                  // 主键查
<T>::sel().uid_eq(uid).is_del_eq(false).one(c).await?    // 条件查单条(必有)
<T>::sel().uid_eq(uid).one_opt(c).await?                 // 条件查单条(可选)
<T>::sel().name_eq("test").exists(c).await?               // 检查是否存在

// 分页
let mut qry = <T>::qry();
if !qry.has_order() { qry.desc_id(); }
qry = qry.status_eq("active");
qry.select().is_del_eq(false).page(c, paging).await?

// 保存（新增/更新 Upsert）
let now = kx_tools::times::sys_time_ts();
if req.get_pk_val().is_err() {
    req.set_created_at(now).set_default().unset_id();
}
req.set_updated_at(now);
req.save(c).await?

// 更新
<T>::m().set_id(id).set_updated_at(now).to_owned().update(c).await?

// 批量更新
<T>::qry().id_bt(100,200).update_set(c, |m| {
    m.set_is_del(true).set_updated_at(now);
}).await?

// 软删（需设置主键）
<T>::m().set_id(id).set_is_del(true).set_updated_at(now).to_owned().update(c).await?
```

### 控制器模式（aide + axum）

```rust
use aide::axum::{ApiRouter, routing::{get, post, put, delete}};
use axum::{Json, extract::Path};
use kx_axum::{R, NR, AxumErr};
use kx_sea_orm::{SeaOrms, common::{Page, Paging}};

// 路由定义
pub fn apis() -> ApiRouter {
    ApiRouter::new()
        .api_route("/list", get(list))
        .api_route("/get/{id}", get(get_by_id))
        .api_route("/save", post(save))
        .api_route("/del/{id}", delete(del))
}

// Handler 返回 Result<R<T>, AxumErr>
async fn list() -> Result<R<Vec<MyModel>>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    let items = MyModel::sel().is_del_eq(false).all(c).await?;
    Ok(items.into())  // From<T> for R<T> 自动转换
}

async fn get_by_id(Path(id): Path<i64>) -> Result<R<MyModel>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    let item = MyModel::get(c, id).await?;
    Ok(item.into())
}

async fn save(Json(mut req): Json<MyModelModify>) -> Result<R<MyModel>, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    let now = kx_tools::times::sys_time_ts();
    if req.get_pk_val().is_err() {
        req.set_created_at(now).set_default().unset_id();
    }
    req.set_updated_at(now);
    let saved = req.save(c).await?;
    Ok(saved.into())
}

// 无返回数据用 NR (= R<()>)
async fn del(Path(id): Path<i64>) -> Result<NR, AxumErr> {
    let c = &mut SeaOrms::xxx().await?;
    MyModel::del(c, id).await?;
    Ok(R::succ())
}
```

### R<T> 响应类型

```rust
R::ok(data)           // 200 + data
R::succ()             // 200 无数据
R::err("msg")         // 500 错误
R::un_auth("msg")     // 401 未授权
R::forbid("msg")      // 403 禁止
R::not_found("msg")   // 404 未找到
data.into()           // From<T> 自动包装为 R::ok(data)
```

## 关键注意点

1. **类型严格匹配**：`qry()` 要求严格类型，`is_del` 是 `bool` 需传 `false/true`；`sel()` 对数值类型更宽松
2. **查询方法选择**：
   - `one(c)` - 必定存在，不存在会报错
   - `one_opt(c)` - 可能不存在，返回 `Option<Model>`
   - `exists(c)` - 仅检查存在性，返回 `bool`
3. **cvt feature**：使用 `kx_tools::cvt::Cvt` 需在 Cargo.toml 启用 `features = ["cvt"]`
4. **Alias 命名**：来自 `table_name` 转大驼峰，不是文件名
5. **软删查询**：始终加 `is_del_eq(false)`
6. **分页排序**：`if !qry.has_order() { qry.desc_id(); }`
7. **DTO 必须 derive**：`schemars::JsonSchema`（OpenAPI 生成）
8. **字段文档注释**：`/// xxx` 用于 Aide 接口文档生成
9. **update 链式调用**：set 后调 `update()` 需先 `.to_owned()`
10. **anyhow 错误**：自动通过 `From<anyhow::Error>` 转为 `AxumErr`

## 详细规范

完整的开发规范、ent 模块模板、biz 模块模板、常见问题解决方案见 [AGENTS.md](references/AGENTS.md)。

包含：
- 仓库结构说明
- `#[derive(Sea)]` 生成的类型别名
- 数据库连接与事务详解
- CRUD 完整模板
- ent 模块编写规范（目录结构、lib.rs、entity/mod.rs、实体文件模板）
- biz 模块编写规范（ctl/svc/router/install 模板）
- 常见问题与注意点

kx 统一包 feature 列表和高级功能见 [ADVANCED.md](references/ADVANCED.md)。
