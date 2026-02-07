---
name: kx-rs
description: kx-rs Rust 后端框架开发规范与 CRUD 模板。当进行 Rust 后端开发时使用，包括：(1) 创建 kx-rs 框架新项目（含 openapi-scan 自动生成 swagger 文档）(2) 创建/编辑 SeaORM 实体（ents/）(3) 编写业务服务层 CRUD（svc/）(4) 编写控制器和路由（ctl/ + router.rs，axum Router）(5) 使用 #[derive(Sea)] 自动生成的 Query/Modify/Select (6) 数据库连接与事务处理 (7) 分页查询与软删除 (8) 响应类型 R<T> 与错误处理 AxumErr (9) openapi-scan 文档扫描兼容 (10) 外部项目引入 kx 框架包。触发场景：用户提到 kx-rs、kx 框架、创建 kx 项目、SeaORM 实体、CRUD 服务、axum 控制器、R<T> 响应、AxumErr、业务模块开发、kx Cargo.toml 配置、openapi-scan、swagger 文档生成。
---

# kx-rs 开发规范

优先使用 `#[derive(Sea)]` 自动生成的方法，用最少试错完成 CRUD。生成的代码必须兼容 openapi-scan 静态扫描。

## 创建新项目

用户要求创建 kx-rs 项目时 → 参考 [TEMPLATE.md](references/TEMPLATE.md) 生成完整项目结构（含 build.rs openapi-scan 集成）。

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

## 控制器模式（openapi-scan 兼容）

Router 函数和 Handler **必须在同一 `impl Xxx` 块内**，扫描器才能关联路由与参数类型。

```rust
pub struct XxxCtl;
impl XxxCtl {
    pub fn apis() -> Router {                              // 非 async、无参、返回 Router
        Router::new()
            .route("/", get(Self::page))                   // Handler 用 Self::method
            .route("/{id}", get(Self::get))
    }
    /// 分页查询                                            // /// 注释 → swagger summary
    async fn page(QsQuery(req): QsQuery<XxxQry>, QsQuery(p): QsQuery<Paging>) -> Result<R<Page<Xxx>>, AxumErr> { ... }
}
```

Handler 签名：`async fn xxx() -> Result<R<T>, AxumErr>`，`anyhow::Error` 自动转 `AxumErr`。

```rust
R::ok(data) / R::succ() / R::err("msg") / R::un_auth("msg") / R::forbid("msg") / R::not_found("msg")
data.into()  // From<T> 自动包装为 R::ok(data)，NR = R<()>
```

## 关键规则

1. `qry()` 类型严格（`bool` 字段必须传 `bool`），`sel()` 更宽松，简单查询优先用 `sel()`
2. 有软删字段时查询始终加 `is_del_eq(false)`
3. DTO/实体 struct 字段必须写 `/// xxx` 文档注释（openapi-scan 从注释生成 schema）
4. 使用 `kx_tools::cvt::Cvt` 需启用 `features = ["cvt"]`
5. `qry().select()` 可将 Query 转为 Select
6. **openapi-scan 兼容**：ctl 用 `impl Struct` + `Router`（非 `ApiRouter`），Handler 用 `Self::method` 引用，路径参数用 `{id}`（非 `:id`）

## 详细参考

- **通用规范**（仓库结构、数据库连接/事务、常见问题）→ [AGENTS.md](references/AGENTS.md)
- **ent 模块模板**（目录结构、实体文件、Cargo.toml）→ [ENT.md](references/ENT.md)
- **biz 模块模板**（ctl/svc/dto/router/install）→ [BIZ.md](references/BIZ.md)
- **高级功能**（feature 列表、历史表、VxeTable、完整方法列表）→ [ADVANCED.md](references/ADVANCED.md)
- **openapi-scan 扫描规则**（扫描识别规则、build.rs 集成、公开路由配置）→ [OPENAPI-SCAN.md](references/OPENAPI-SCAN.md)
- **项目模板**（创建新 kx-rs 项目的完整模板）→ [TEMPLATE.md](references/TEMPLATE.md)
