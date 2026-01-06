# kx-rs 项目 AI 开发规则（面向快速正确 CRUD）

目标：让 AI 在本仓库里写代码时，**优先使用框架通过 `#[derive(Sea)]` 自动生成的 struct / 方法**，用最少的试错完成增删改查与事务。

> 参考示例：`bizs/ai-demo`（控制器、服务、安装/迁移、数据源注册）。
> 参考示例：`ents/ai-demo`（实体定义、索引创建、迁移）。

---

## 1) 仓库结构（你写业务时最常用的部分）

- `ents/<ds>/`：实体层（SeaORM 实体 + `#[derive(Sea)]` 自动生成的 Query/Modify 等）。
- `bizs/<biz>/`：业务模块（svc/ctl/router/install 等），依赖对应的 `kx-ents-*`。
- `crates/sea-orm/`：DB 连接与事务封装（`SeaOrms` / `SeaTrans` / `ext_db_trait!`）。
- `derives/sea/ai-readme.md`：`@sea` 宏能力说明（建议遇到疑问先看这里）。

---

## 2) `#[derive(Sea)]` 会自动生成哪些"关键 struct/别名"（CRUD 核心）

在 `ents/<ds>/src/entity/<table>.rs` 里，你只会看到 `pub struct Model { ... }`，但 `#[derive(Sea)]` 会额外生成并 **导出类型别名**：

- `<Alias>`：`Model` 的别名（例：`AiDemo`）
- `<Alias>Qry`：查询构建器 `Query` 的别名（例：`AiDemoQry`）
- `<Alias>Modify`：修改模型 `ModifyModel` 的别名（例：`AiDemoModify`）
- `<Alias>Entity` / `<Alias>Col`：实体与列（一般不需要手写）

### 2.1 Alias 命名规则（非常重要）

**Alias 来自 `#[sea_orm(table_name = "...")]` 的 `table_name` 转大驼峰，而不是文件名。**

例：`table_name = "ai_demo"` → Alias 是 `AiDemo`（对应 `AiDemoQry / AiDemoModify`）。

当你不确定 Alias：
1) 打开对应实体文件 `ents/<ds>/src/entity/<table>.rs`
2) 看顶部注释里 `ai请注意` 的说明，或直接根据 `table_name` 推导。

---

## 3) 如何正确拿到数据库连接（单库/多库/事务）

### 3.1 模块内注册数据源（写在 `bizs/<biz>/src/lib.rs`）

```rust
pub use kx_ents_xxx::entity as ents;
kx_sea_orm::ext_db_trait!(xxx);
```

这会在当前业务 crate 内生成 `SeaOrmExt / SeaTransExt`，让你能这样取连接：

```rust
use crate::SeaOrmExt;
use kx_sea_orm::SeaOrms;

let c = &mut SeaOrms::xxx().await?;
```

### 3.2 事务（推荐复杂保存/多表一致性）

```rust
use crate::SeaTransExt;
use kx_sea_orm::SeaTrans;

let ret = SeaTrans::new()
  .transaction(|tx| {
    Box::pin(async move {
      let c = tx.xxx().await?;
      // ... 在 c 上做多次写操作
      Ok(())
    })
  })
  .await?;
```

---

## 4) CRUD 最快最稳的写法（直接套模板）

下面以 `<T>` 代表你的实体 Alias（例如 `AiDemo` / `TodoTask` / `MktgLink`）。

### 4.1 查（Read）

- 主键查询：`<T>::get(c, pk).await?`
- 条件查多条：`<T>::sel().xxx_eq(...).all(c).await?`
- 条件查 1 条：`<T>::sel().xxx_eq(...).one(c).await?`
- 条件查 1 条 Option：`<T>::sel().xxx_eq(...).one_opt(c).await?`
- 快速 Select（更宽松的数值类型匹配）：`<T>::sel().id_eq(1).all(c).await?`

> 小坑：`qry()` 的条件类型更严格（字段是 `i16` 就要传 `i16`），`sel()` 通常更宽松，适合快速写查询。

> 转化: `qry().select()` 可将Query转为Select。

### 4.2 分页（Page）

```rust
use kx_sea_orm::common::{Page, Paging};

let mut qry: <T>Qry = <T>::qry();
if !qry.has_order() { qry.desc_id(); }
let ret: Page<<T>> = qry.select().is_del_eq(0).page(c, Paging::new(1, 20)).await?;
```

### 4.3 新增/保存（Create / Upsert）

#### 简单场景：直接收 `Json<<T>Modify>`

```rust
let now = kx_tools::times::sys_time_ts();
if req.get_pk_val().is_err() {
  req.set_created_at(now).set_default().unset_id(); // 视主键字段名调整 unset_*
}
req.set_updated_at(now);
let saved: <T> = req.save(c).await?;
```

#### 复杂场景：先 `Value -> <T>Modify`（适合混合字段/attrs）

```rust
use kx_tools::cvt::Cvt;
let mut req = data.cvt::<<T>Modify>()?;
// 其余逻辑同上
```

> 关键点：
> - `get_pk_val()`：判断是插入还是更新的最通用方式（联合主键也适用）。
> - `set_default()`：给"非主键字段"补默认值（避免遗漏必填/默认字段）。
> - `unset_id()`：常用于自增主键插入（避免前端传 id 造成冲突）；如果主键不是 `id`，用对应的 `unset_<pk>()`。

### 4.4 更新（Update）

#### 方式 A：用 ModifyModel 直接 update（最常见）

```rust
<T>::m()
  .set_id(id)
  .set_updated_at(now)
  .to_owned()
  .update(c)
  .await?;
```

> 小坑：链式 set 后如果调用 `update()`，通常需要 `.to_owned()` 把 builder 变成 owned。

#### 方式 B：批量更新（按条件更新多行）

```rust
<T>::qry()
  .uid_eq(uid)
  .update_set(c, |m| {
    m.set_is_del(1).set_deleted_at(now);
  })
  .await?;
```

### 4.5 删除（Delete）

- 软删（推荐）：更新 `is_del / deleted_at`（见上面的 update 模板）
- 物理删除（谨慎）：`<T>::del(c, pk).await?`
- 条件批量删除：`<T>::qry().xxx_eq(...).delete_many(c).await?`

---

## 5) 开发时优先遵循的约定（能省大量返工）

1) **优先使用 `<T>::sel() / <T>::qry() / <T>::m() / <T>::get() / <T>::del() / <T>::save_batch()`**，不要手写 SeaORM 的 `Entity::find()`/`ActiveModel`（除非确实需要底层能力）。
2) 看到实体里有 `ai请注意` 注释：按注释执行（通常是 alias、索引、迁移等关键点）。
3) 有软删字段时：查询默认补 `is_del_eq(0/false)`；删除优先走软删。
4) 分页默认加排序：`if !qry.has_order() { qry.desc_id(); }`（避免结果不稳定）。
5) 新增模块/新数据源：记得在业务 crate `lib.rs` 里加 `kx_sea_orm::ext_db_trait!(<ds>)`，并在 `install.rs` 里调用 `crate::ents::<Ds>Migrate::migrate(c).await?`。
6) **实体/DTO struct 生成时 `derive` 里必须带 `schemars::JsonSchema`**（可先 `use schemars::JsonSchema;`，再写 `#[derive(..., JsonSchema, ...)]`），保证 Aide/OpenAPI 能正确生成 schema。
7) **字段必须写 `/// xxx` 风格的文档注释**（放在字段上方），用于 Aide 生成接口文档与字段描述；不写会导致文档缺失/语义不清。

---

## 6) ent 模块编写规范（参考 `ents/ai-demo`）

### 6.1 目录结构

```
ents/<ds>/
├── Cargo.toml
└── src/
    ├── lib.rs           # 导出 entity 模块和 common
    └── entity/
        ├── mod.rs       # 导出所有实体和 Migrate 结构体
        ├── prelude.rs   # 可选的 prelude 导出
        └── <table>.rs   # 各个表的实体定义
```

### 6.2 lib.rs 模板

```rust
pub mod entity;
pub use kx_sea_common as common;
```

### 6.3 entity/mod.rs 模板

```rust
use anyhow::Result;
use sea_orm::ConnectionTrait;

use crate::entity::{<alias1>::<Alias1>, <alias2>::<Alias2>};
pub mod <table1>;
pub mod <table2>;
pub struct <Ds>Migrate;

impl <Ds>Migrate {
    pub async fn migrate<C: ConnectionTrait>(c: &C) -> Result<()> {
        <Alias1>::auto_migrate(c).await?;
        // ai请注意,如果有创建索引方法,则需要将索引创建放到migrate
        <Alias1>::create_idxs(c).await?;
        <Alias2>::auto_migrate(c).await?;
        Ok(())
    }
}
```

### 6.4 实体文件模板（`<table>.rs`）

```rust
use kx_sea_common::Sea;
use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Sea, schemars::JsonSchema, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
// ai请注意,各个模块的别名是以table_name转大驼峰的,不是以文件名来的,当前别名为XxxYyy
#[sea_orm(table_name = "xxx_yyy", comment = "表描述")]
pub struct Model {
    /// ID
    #[sea_orm(primary_key)]
    pub id: i64,
    /// 用户ID
    #[sea_orm(indexed)]
    pub uid: i64,
    /// 字符串字段
    pub name: String,
    /// Text 类型字段
    #[sea_orm(column_type = "Text")]
    pub content: String,
    /// 指定长度的字符串
    #[sea_orm(column_type = "String(StringLen::N(500))")]
    pub remark: String,
    /// Decimal 类型字段
    #[sea_orm(column_type = "Decimal(Some((10, 2)))")]
    pub amount: Decimal,
    /// 创建时间
    pub created_at: i64,
    /// 更新时间
    pub updated_at: i64,
    /// 是否删除（indexed 表示单字段索引）
    #[sea_orm(indexed)]
    pub is_del: i16,
    /// 删除时间
    pub deleted_at: i64,
}

impl Model {
    /// 创建索引
    /// ai请注意,不要盲目创建联合索引,业务需要创建联合索引才创建
    /// 单字段索引请在模型定义时候的sea_orm属性中添加 indexed,唯一索引添加indexed后再添加unique属性
    pub async fn create_idxs<C: ConnectionTrait>(c: &C) -> Result<()> {
        // 联合索引创建示例
        let st = Self::create_index_statement(
            "idx_uid_name",
            vec![Column::Uid, Column::Name],
        );
        // 唯一索引需要: st.unique();
        if let Err(_) = Self::exec_idx(c, &st).await {}
        Ok(())
    }
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

### 6.5 联合主键实体示例

```rust
#[derive(Clone, Sea, schemars::JsonSchema, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(table_name = "xxx_union_pk", comment = "联合主键表")]
pub struct Model {
    /// 主键1
    #[sea_orm(primary_key, auto_increment = false)]
    pub pk_1: i64,
    /// 主键2
    #[sea_orm(primary_key, auto_increment = false)]
    pub pk_2: i64,
    // ... 其他字段
}
```

### 6.6 Cargo.toml 模板

```toml
[package]
name = "kx-ents-<ds>"
version.workspace = true
authors.workspace = true
edition.workspace = true
license.workspace = true
publish.workspace = true

[dependencies]
schemars = { workspace = true }
anyhow = { workspace = true }
chrono = { workspace = true, features = ["serde"] }
kx-sea-common = { workspace = true }
sea-orm = { workspace = true, features = ["macros", "runtime-tokio-rustls"] }
serde = { workspace = true }
# 如果使用 Decimal 类型
rust_decimal = { workspace = true }
# 如果使用 serde_with
serde_with = { workspace = true }

[features]
full = ["mysql", "postgres", "sqlite"]
mysql = ["sea-orm/sqlx-mysql"]
postgres = ["sea-orm/sqlx-postgres"]
sqlite = ["sea-orm/sqlx-sqlite"]
```

---

## 7) 常见问题与注意点

### 7.1 `kx_tools::cvt::Cvt` 找不到

**原因**：`kx-tools` 默认不启用 `cvt` feature。

**解决**：在业务模块的 `Cargo.toml` 中添加 feature：
```toml
kx-tools = { workspace = true, features = ["cvt"] }
```

### 7.2 `qry()` 的类型严格匹配问题

**问题**：`<T>::qry().is_del_eq(0)` 编译报错 `the trait bound i16: From<i32> is not satisfied`

**原因**：`qry()` 的条件方法对类型要求严格。如果字段是 `i16`，就必须传 `i16` 类型的值。

**解决**：
```rust
// 错误示例
GiftMember::qry().is_del_eq(0).one(c).await?

// 正确示例
GiftMember::qry().is_del_eq(0i16).one(c).await?
```

**建议**：如果只是简单查询，推荐使用 `sel()` 替代 `qry()`，`sel()` 对数值类型更宽松：
```rust
GiftMember::sel().is_del_eq(0).one(c).await?  // 这样也可以
```

### 7.3 未使用的 import 警告

如果 `use anyhow::{Result, anyhow}` 中 `anyhow` 未使用，改为：
```rust
use anyhow::Result;
```

### 7.4 索引创建注意事项

- **单字段索引**：在 `#[sea_orm(...)]` 属性中添加 `indexed`
- **唯一索引**：在 `indexed` 基础上添加 `unique` 属性
- **联合索引**：在 `impl Model` 的 `create_idxs` 方法中创建
- **不要盲目添加索引**：只在业务确实需要时创建
