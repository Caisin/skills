# SeaORM 2.0 稳定版能力与 KX 边界

当前 workspace 统一使用 `sea-orm 2.0.2`，最低 Rust 版本为 1.94。`kx-sea-orm` 在 crate 根重导出 SeaORM，因此下游不需要绕过 KX 封装才能使用正式版 API。

## 可直接采用的能力

- `require_one`：在 `Select`、`Selector` 等查询上要求恰好返回一条记录，无记录时返回 `DbErr::RecordNotFound`。
- `raw_sql!`：需要原始 SQL 时使用参数注入宏，避免手工拼接值。
- 嵌套 partial model：复杂读取可只选择所需字段，并嵌套完整 Model 或 partial model。
- `ActiveModel::from_json`：允许缺少未提交字段，生成部分填充的 ActiveModel。
- `insert_many` 新语义：空输入和 `last_insert_id: Option<_>` 不再依赖易 panic 的旧流程。
- `#[sea_orm::model]`：使用 dense entity，并生成 `ModelEx`、`ActiveModelEx` 和 relation 元数据。
- `SchemaBuilder::sync`：补齐缺失表、列和索引；KX 的 `auto_migrate` 直接使用该实验 API。
- `DeriveIntoActiveModel`：KX 的 `ModifyModel` 直接派生 DTO 到 ActiveModel 的转换。
- async transaction helper、连接池 `before_acquire` hook、`Paginator::set_page`。
- `date_time_default_now`、`timestamp_default_now`、`timestamp_with_time_zone_default_now` Schema helper。

## KX 采用边界

- 允许在 dense entity 中直接声明 `belongs_to` / `has_one` / `has_many`，供 JOIN、loader 与 Seaography 使用。
- 禁止数据库外键；实际拥有外键字段的 `belongs_to` 必须声明 `skip_fk`。
- relation 不提供引用完整性保证；继续使用普通 ID 字段、service 校验和事务。
- 不因上游提供 RBAC `RestrictedConnection` 就替换现有认证/授权体系。
- 不为每个上游 helper 增加一层同名 KX wrapper；能稳定重导出的 API 直接使用。
- KX 冲突更新使用 `upsert` / `upsert_many`，不遮蔽 SeaORM 原生 `ActiveModelTrait::save`。
- schema sync 只新增缺失对象；类型修改、约束调整和删除继续使用显式 migration。
- PostgreSQL schema 与时区通过 `ConnectOptions` 配置，不自行构造 SQLx pool。

## 常见错误

```text
❌ `belongs_to` 不写 `skip_fk`，把 relation 误变成数据库外键
❌ 使用普通 `Option<Entity>` / `Vec<Entity>` 代替当前 2.0.2 的 BelongsTo / HasOne / HasMany 包装类型
❌ 为每个上游新 helper 再包装一个同名 KX API
❌ 升级依赖后假设数据库 Schema 会自动变化
❌ 把 schema sync 当成能修改列类型或删除字段的完整迁移系统
❌ 手写空 Relation，或把 Sea derive 放进普通 derive 列表使 ModelEx 重复生成 KX API
❌ 继续用 save 表达数据库级冲突更新
❌ 使用 raw_sql! 时忽略结果类型、权限和事务边界
```

## 正确做法

```text
✅ 直接使用 kx-sea-orm 重导出的稳定上游 API
✅ require_one 用于业务上必须存在的单行读取
✅ 实体使用 #[sea_orm::model] + model_attrs(derive(Sea))
✅ relation 字段使用 BelongsTo / HasOne / HasMany，belongs_to 必须 skip_fk
✅ 非破坏性补齐使用 auto_migrate，破坏性变更使用显式 migration
✅ 冲突更新使用 upsert，原生 save 保持 SeaORM insert/update 语义
✅ 继续使用普通 ID 字段、service 校验和事务维护关联一致性
```

## 版本证据

- crates.io：`sea-orm 2.0.2`
- 上游发布说明：2.0.2 新增 `require_one` 和时间默认值 helper，并修复 CLI 保留用户修改时的重复 import。
- 详细设计：`docs/dev/design/sea-orm-2-0-2-upgrade.md`
