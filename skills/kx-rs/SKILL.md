---
name: kx-rs
description: kx-rs Rust 后端框架开发规范与 CRUD 模板。当进行 Rust 后端开发时使用，包括：(1) 创建/编辑 SeaORM 实体（ents/）(2) 编写业务服务层 CRUD（svc/）(3) 编写控制器和路由（ctl/ + router.rs，aide + axum）(4) 使用 #[derive(Sea)] 自动生成的 Query/Modify/Select (5) 数据库连接与事务处理 (6) 分页查询与软删除 (7) 响应类型 R<T> 与错误处理 AxumErr (8) 外部项目引入 kx 框架包。触发场景：用户提到 kx-rs、kx 框架、SeaORM 实体、CRUD 服务、aide/axum 控制器、R<T> 响应、AxumErr、业务模块开发、kx Cargo.toml 配置。
---

# kx-rs 开发规范

优先使用 `#[derive(Sea)]` 自动生成的方法，用最少试错完成 CRUD。

## 引入方式

```toml
kx = { version = "0.1", registry = "hekx", features = ["axum", "tools", "sea-orm", "cache"] }
# 按需加: "derive-sea", "ents-base", "ents-log", "ed", "global", "tracing", "i18n" 等
```

## CRUD 速查

`<T>` = 实体 Alias（来自 `table_name` 转大驼峰，非文件名）。自动生成 `<T>Qry` / `<T>Modify` / `<T>Entity`。

```rust
let c = &mut SeaOrms::xxx().await?;  // 连接（需 lib.rs 注册 ext_db_trait!(xxx)）

// 查询
<T>::get(c, pk).await?                                   // 主键查
<T>::sel().uid_eq(uid).is_del_eq(false).one(c).await?     // 条件查(必有，不存在报错)
<T>::sel().uid_eq(uid).one_opt(c).await?                  // 条件查(可选，返回 Option)
<T>::sel().name_eq("test").exists(c).await?                // 存在性检查(返回 bool)

// 分页
let mut qry = <T>::qry();
if !qry.has_order() { qry.desc_id(); }                   // 分页必须有排序
qry.select().is_del_eq(false).page(c, paging).await?

// 保存（Upsert）
let now = kx_tools::times::sys_time_ts();
if req.get_pk_val().is_err() { req.set_created_at(now).set_default().unset_id(); }
req.set_updated_at(now);
req.save(c).await?

// 更新（链式 set 后需 .to_owned() 再 .update()）
<T>::m().set_id(id).set_updated_at(now).to_owned().update(c).await?

// 批量更新
<T>::qry().id_bt(100,200).update_set(c, |m| { m.set_is_del(true); }).await?

// 软删（推荐）/ 物理删除
<T>::m().set_id(id).set_is_del(true).set_updated_at(now).to_owned().update(c).await?
<T>::del(c, pk).await?                                    // 物理删除（谨慎）
```

## 控制器模式

Handler 签名：`async fn xxx() -> Result<R<T>, AxumErr>`，`anyhow::Error` 自动转 `AxumErr`。

```rust
R::ok(data) / R::succ() / R::err("msg") / R::un_auth("msg") / R::forbid("msg") / R::not_found("msg")
data.into()  // From<T> 自动包装为 R::ok(data)，NR = R<()>
```

## 关键规则

1. `qry()` 类型严格（`bool` 字段必须传 `bool`），`sel()` 更宽松，简单查询优先用 `sel()`
2. 有软删字段时查询始终加 `is_del_eq(false)`
3. DTO/实体 struct 必须 derive `schemars::JsonSchema`，字段必须写 `/// xxx` 文档注释
4. 使用 `kx_tools::cvt::Cvt` 需启用 `features = ["cvt"]`
5. `qry().select()` 可将 Query 转为 Select

## 详细参考

- **通用规范**（仓库结构、数据库连接/事务、常见问题）→ [AGENTS.md](references/AGENTS.md)
- **ent 模块模板**（目录结构、实体文件、Cargo.toml）→ [ENT.md](references/ENT.md)
- **biz 模块模板**（ctl/svc/dto/router/install、crud_api! 宏）→ [BIZ.md](references/BIZ.md)
- **高级功能**（feature 列表、历史表、VxeTable、完整方法列表）→ [ADVANCED.md](references/ADVANCED.md)
