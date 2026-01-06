---
name: kx-rs
description: kx-rs Rust 项目开发规范与 CRUD 模板。当在 kx-rs 项目中进行开发时使用，包括：(1) 创建/编辑 SeaORM 实体（ents/）(2) 编写业务服务层 CRUD（bizs/*/svc/）(3) 使用 #[derive(Sea)] 自动生成的 Query/Modify/Select (4) 数据库连接与事务处理 (5) 分页查询与软删除。触发场景：用户提到 kx-rs、SeaORM 实体、CRUD 服务、gift/ai-demo 等业务模块开发。
---

# kx-rs 开发规范

快速在 kx-rs 项目中完成 CRUD 开发，优先使用 `#[derive(Sea)]` 自动生成的方法。

## 核心速查

### 数据库连接

```rust
// 普通连接
let c = &mut SeaOrms::xxx().await?;

// 事务
SeaTrans::new().transaction(|tx| {
    Box::pin(async move {
        let c = tx.xxx().await?;
        // 操作...
        Ok(())
    })
}).await?
```

### CRUD 模板

```rust
// 查询
<T>::get(c, pk).await?                        // 主键查
<T>::sel().uid_eq(uid).is_del_eq(0).one(c).await?  // 条件查

// 分页
let mut qry = <T>::qry();
if !qry.has_order() { qry.desc_id(); }
qry = qry.status_eq("active");
qry.select().is_del_eq(0).page(c, paging).await?

// 保存
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
    m.set_is_del(1).set_updated_at(now);
}).await?

// 软删,**关键点**需要设置主键
<T>::m().set_id(id).set_is_del(1).set_updated_at(now).to_owned().update(c).await?
```

## 关键注意点

1. **类型严格匹配**：`qry()` 要求严格类型，`is_del` 是 `i16` 需传 `0i16`
2. **cvt feature**：使用 `kx_tools::cvt::Cvt` 需在 Cargo.toml 启用 `features = ["cvt"]`
3. **Alias 命名**：来自 `table_name` 转大驼峰，不是文件名
4. **软删查询**：始终加 `is_del_eq(0)` 或 `is_del_eq(0i16)`
5. **分页排序**：`if !qry.has_order() { qry.desc_id(); }`

## 详细规范

完整的开发规范、ent 模块模板、常见问题解决方案见 [AGENTS.md](references/AGENTS.md)。

包含：
- 仓库结构说明
- `#[derive(Sea)]` 生成的类型别名
- 数据库连接与事务详解
- CRUD 完整模板
- ent 模块编写规范（目录结构、lib.rs、entity/mod.rs、实体文件模板）
- 常见问题与注意点
