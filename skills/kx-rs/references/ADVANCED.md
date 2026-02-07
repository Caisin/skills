# kx 高级功能参考

## kx 统一包 Feature 列表

通过 `kx = { version = "0.1", features = [...] }` 按需引入：

### 默认启用
- `axum` - Web 框架（aide + axum）
- `tools` - 工具集
- `sea-orm` - 数据库 ORM
- `cache` - 缓存

### Core
- `cst` - 常量定义
- `models` - 公共模型
- `sea-common` - SeaORM 公共类型（Sea derive 宏）

### Derives
- `codegen` - 代码生成
- `derive-sea` - `#[derive(Sea)]` 宏

### Entities
- `ents-base` - 基础实体（数据源管理等）
- `ents-log` - 日志实体

### Crates
- `ed` - 加解密
- `global` - 全局状态管理
- `cmds` - 命令行工具
- `certs` - 证书管理
- `geoip` - IP 地理位置
- `image` - 图片处理
- `svg` - SVG 处理
- `macros` - 通用宏
- `sql` - SQL 工具
- `tb` - 表格工具
- `ua` - User-Agent 解析
- `ips` - IP 工具
- `tracing` - 日志追踪
- `typst` - Typst 排版
- `novels` - 小说处理
- `doc-tool` - 文档工具
- `cron` - 定时任务
- `tk-pool` - Token 池
- `i18n` - 国际化
- `sysinfo` - 系统信息
- `route-per` - 路由权限
- `deamon` - 守护进程

### SDKs
- `sdk-core` - SDK 核心
- `acme` - ACME 证书
- `sdk-aws` - AWS SDK
- `sdk-volc` - 火山引擎 SDK
- `sdk-alibl` - 阿里云 SDK
- `sdk-wx-core` - 微信核心 SDK
- `sdk-wx-app` - 微信小程序 SDK
- `sdk-mayfly` - Mayfly SDK
- `sdk-dingtalk` - 钉钉 SDK

## #[derive(Sea)] 高级功能

### 历史表追踪

```rust
#[derive(Clone, Sea, Debug, PartialEq, DeriveEntityModel, Eq, Serialize, Deserialize, Default)]
#[sea_orm(table_name = "order", comment = "订单")]
#[kx(his_tb = "order_h")]  // 自动记录变更到 order_h 表
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub status: String,
    // ...
}

// 创建历史表
Model::create_h(&db).await?;
// 数据转换
let his_model: his::Model = order_model.into();
let order_model: Model = his_model.into();
```

### VxeTable 批量编辑

```rust
use kx_sea_orm::common::VxeSave;

let vxe_data = VxeSave {
    insert_records: Some(vec![new1, new2]),
    update_records: Some(vec![updated]),
    remove_records: Some(vec![deleted]),
    pending_records: None,
};
let result = MyModel::vxe_save(c, vxe_data).await?;
// result.insert_rows, result.update_rows, result.remove_rows
```

### 生成的完整方法列表

#### Model 方法
- `tb_name()` / `tb_name_h()` - 获取表名/历史表名
- `get(c, pk)` - 主键查询
- `del(c, pk)` - 物理删除
- `sel()` - 创建 EntitySelect（宽松类型）
- `qry()` - 创建 Query（严格类型）
- `m()` - 创建 ModifyModel
- `auto_migrate(c)` - 自动迁移表结构
- `create_table(c)` - 创建表
- `save_batch(c, vec)` - 批量保存
- `del_by_ids(c, ids)` - 批量删除
- `vxe_save(c, data)` - VxeTable 批量操作
- `save_batch_do_nothing(c, vec)` - 批量保存（冲突忽略）

#### Query 方法
- `*_eq()` / `*_ne()` / `*_like()` / `*_contains()` - 条件
- `*_gt()` / `*_lt()` / `*_gte()` / `*_lte()` - 比较
- `*_bt(min, max)` - BETWEEN
- `*_is_in(vec)` / `*_is_not_in(vec)` - IN/NOT IN
- `*_is_null()` / `*_is_not_null()` - NULL 判断
- `asc_*()` / `desc_*()` - 排序
- `has_order()` - 是否已设置排序
- `select()` - 转为 EntitySelect
- `page(c, paging)` - 分页查询
- `all(c)` / `one(c)` - 执行查询
- `delete_many(c)` - 批量删除
- `count(c)` - 计数
- `update_set(c, |m| { ... })` - 批量更新

#### ModifyModel 方法
- `set_*()` / `unset_*()` / `get_*()` - 字段操作
- `set_default()` - 设置默认值
- `get_pk_val()` - 获取主键值
- `save(c)` / `insert(c)` / `update(c)` - 持久化
- `to_owned()` - 转为 owned（链式调用 update 前需要）
- `exists(c)` - 检查是否存在
- `cols()` - 获取已修改的列

#### EntitySelect 方法
- 同 Query 的条件/排序方法
- `all(c)` / `one(c)` / `one_opt(c)` - 执行查询
- `count(c)` - 计数
- `exists(c)` - 检查存在性
- `page(c, paging)` - 分页
- `limit(n)` - 限制数量
