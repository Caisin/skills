# openapi-scan 扫描规则

`kx-openapi-scan` 是静态源码扫描器，在 `build.rs` 编译期自动解析路由/Handler/结构体，生成 OpenAPI 3.1 JSON，供 swagger-ui 使用。

## 扫描识别规则

### 1. Router 函数识别

扫描器识别 `impl Xxx` 块中**非 async、无参数、返回 `Router`** 的函数：

```rust
pub struct DemoCtl;
impl DemoCtl {
    // ✅ 会被识别为路由函数
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/{id}", get(Self::get))
            .route("/{id}", delete(Self::del))
    }
}
```

支持的路由方法：`.route(path, get/post/put/delete/patch(handler))`、`.nest(prefix, Xxx::fn())`、`.merge(Xxx::fn())`。

### 2. Handler 签名识别

扫描器识别 `impl` 块中的 `async fn`，提取：
- **Query 参数**：`QsQuery<T>` 或 `Query<T>` → 展开为 query parameters
- **Body 参数**：`Json<T>` → 生成 requestBody schema
- **Multipart**：参数含 `Multipart` → multipart/form-data
- **返回类型**：`Result<R<T>, AxumErr>` → 提取 `T` 生成 response schema
- **文档注释**：`///` 注释 → OpenAPI summary/description

```rust
impl DemoCtl {
    /// 分页查询笔记
    async fn page(
        QsQuery(req): QsQuery<DemoNoteQry>,   // → query params
        QsQuery(page): QsQuery<Paging>,        // → query params
    ) -> Result<R<Page<DemoNote>>, AxumErr> {   // → response schema
        // ...
    }

    /// 保存笔记
    async fn save(
        Json(req): Json<DemoNoteModify>,       // → requestBody
    ) -> Result<R<DemoNote>, AxumErr> {
        // ...
    }
}
```

### 3. 结构体/实体识别

- **普通 struct**：扫描 `pub struct Xxx { pub field: Type }` 及 `/// doc` 注释
- **SeaORM Entity**：识别 `#[sea_orm(table_name = "xxx")]` 的 `pub struct Model`，自动以 `table_name` 转大驼峰作为别名
- **字段文档**：`/// xxx` 注释 → schema description

### 4. 关键要求（生成代码必须遵守）

1. **ctl 中 Router 函数必须在 `impl Xxx` 块内**，不能是独立 `pub fn`
2. **Handler 必须是 `async fn`**，且在同一 `impl` 块中
3. **返回类型必须包含 `R<T>`**（或 `NR`），扫描器从中提取响应 schema
4. **DTO/实体 struct 字段必须写 `/// doc` 注释**，扫描器从注释生成 schema description
5. **使用 `axum::Router`**（非 `ApiRouter`），路由用 `.route()` 注册
6. **路由路径参数用 `{id}` 格式**（非 `:id`）
7. **Handler 引用用 `Self::method`**，扫描器通过 `StructName::method` 关联

### 5. build.rs 集成

```rust
use std::path::PathBuf;

fn main() -> anyhow::Result<()> {
    println!("cargo:rerun-if-changed=src");
    let manifest_dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?);
    let title = "项目名";
    let description = "API 文档描述";
    let out = manifest_dir.join("openapi.json");
    let scan_cfg = kx_openapi_scan::default_config(Some(&manifest_dir))?
        .with_output(&out)
        .with_openapi_info(title, description);
    kx_openapi_scan::generate_with_config(scan_cfg)?;
    Ok(())
}
```

Cargo.toml 需添加：
```toml
[build-dependencies]
anyhow = { workspace = true }
kx-openapi-scan = { workspace = true }
```

### 6. 提供 openapi.json 路由

在根 Router 中挂载：
```rust
.route("/openapi.json", get(|| async { include_str!("../openapi.json") }))
```

### 7. 公开路由（免授权）

在 `cfg.toml` 中配置 `routes` 数组，匹配的路由在文档中标记 `security: []`：
```toml
routes = [
    "/login",
    "/register;POST",
    "/public/**",
]
```
