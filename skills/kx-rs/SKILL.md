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
<T>::get(c, pk).await?                            // 主键查
<T>::sel().uid_eq(uid).is_del_eq(false).one(c).await?  // 条件查单条(必有)
<T>::sel().uid_eq(uid).one_opt(c).await?          // 条件查单条(可选)
<T>::sel().name_eq("test").exists(c).await?       // 检查是否存在

// 分页
let mut qry = <T>::qry();
if !qry.has_order() { qry.desc_id(); }
qry = qry.status_eq("active");
qry.select().is_del_eq(false).page(c, paging).await?

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
    m.set_is_del(true).set_updated_at(now);
}).await?

// 软删,**关键点**需要设置主键
<T>::m().set_id(id).set_is_del(true).set_updated_at(now).to_owned().update(c).await?
```

## 关键注意点

1. **类型严格匹配**：`qry()` 要求严格类型，`is_del` 是 `bool` 需传 `false/true`；`sel()` 对数值类型更宽松
2. **查询方法选择**：
   - `one(c)` - 必定存在，不存在会报错
   - `one_opt(c)` - 可能不存在，返回 `Option<Model>`
   - `exists(c)` - 仅检查存在性，返回 `bool`，性能优于 `one_opt().is_some()`
3. **cvt feature**：使用 `kx_tools::cvt::Cvt` 需在 Cargo.toml 启用 `features = ["cvt"]`
4. **Alias 命名**：来自 `table_name` 转大驼峰，不是文件名
5. **软删查询**：始终加 `is_del_eq(false)`
6. **分页排序**：`if !qry.has_order() { qry.desc_id(); }`

## 详细规范

完整的开发规范、ent 模块模板、常见问题解决方案见 [AGENTS.md](references/AGENTS.md)。

包含：
- 仓库结构说明
- `#[derive(Sea)]` 生成的类型别名
- 数据库连接与事务详解
- CRUD 完整模板
- ent 模块编写规范（目录结构、lib.rs、entity/mod.rs、实体文件模板）
- 常见问题与注意点
