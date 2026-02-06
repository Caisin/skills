# kx-rs 详细规范

参考现有模块（如 `bizs/gift`、`ents/gift`）快速上手。

## 仓库结构

- `ents/<ds>/` — 实体层（SeaORM 实体 + `#[derive(Sea)]` 自动生成）
- `bizs/<biz>/` — 业务模块（svc/ctl/router/install），依赖 `kx-ents-*`
- `crates/sea-orm/` — DB 连接与事务封装（`SeaOrms` / `SeaTrans` / `ext_db_trait!`）
- `derives/sea/ai-readme.md` — `@sea` 宏能力说明

## 数据库连接

```rust
// lib.rs 注册数据源
pub use kx_ents_xxx::entity as ents;
kx_sea_orm::ext_db_trait!(xxx);  // 生成 SeaOrmExt / SeaTransExt

// 使用
use crate::SeaOrmExt;
let c = &mut SeaOrms::xxx().await?;

// 事务
use crate::SeaTransExt;
SeaTrans::new().transaction(|tx| {
    Box::pin(async move {
        let c = tx.xxx().await?;
        Ok(())
    })
}).await?;
```

## 模块模板

- **创建/编辑实体模块** → [ENT.md](ENT.md)（目录结构、lib.rs、entity/mod.rs、实体文件、Cargo.toml）
- **创建/编辑业务模块** → [BIZ.md](BIZ.md)（ctl/svc/dto/router/install 模板、crud_api! 宏、Cargo.toml）

## 常见问题

| 问题 | 解决 |
|------|------|
| `Cvt` 找不到 | `kx-tools = { ..., features = ["cvt"] }` |
| `qry()` 类型不匹配 | `bool` 字段传 `false` 不是 `0`，或改用 `sel()` |
| 未使用 import 警告 | 删除未用的 `anyhow` 等 |
| 索引 | 单字段用 `#[sea_orm(indexed)]`，联合索引在 `create_idxs` 中创建 |
