# openapi-scan

用于“为什么扫描不到”“怎样保持 ctl/router 兼容”的场景。

## 最核心规则

要让 `kx-openapi-scan` 正常扫描，至少满足这些要求：

1. Router 函数在同一 `impl Xxx` 块内
2. Router 函数是非 async、无参数、返回 `Router`
3. Handler 也在同一 `impl Xxx` 块内
4. Handler 用 `Self::method`
5. 路由参数用 `{id}`，不要用 `:id`
6. 字段和接口尽量写 `///` 注释

## 推荐模板

```rust
pub struct XxxCtl;

impl XxxCtl {
    pub fn apis() -> Router {
        Router::new()
            .route("/", get(Self::page))
            .route("/", post(Self::save))
            .route("/{id}", get(Self::get))
    }

    /// 分页查询
    async fn page(...) -> Result<R<Page<Xxx>>, AxumErr> { ... }

    /// 保存
    async fn save(...) -> Result<R<Xxx>, AxumErr> { ... }
}
```

## 常见错误

```rust
// ❌ 错误：router 函数写到 impl 外
pub fn apis() -> Router { ... }

impl XxxCtl {
    // ❌ 错误：handler 分散在另一个 impl
}

Router::new().route(":id", get(Self::get)); // ❌ 错误：路径参数写成 :id
```

## 正确做法

```rust
// ✅ 正确：Router 与 handler 放在同一 impl 块
impl XxxCtl {
    pub fn apis() -> Router {
        Router::new().route("/{id}", get(Self::get))
    }

    async fn get(...) -> Result<R<Xxx>, AxumErr> { ... }
}
```

## build.rs 最小集成

```rust
println!("cargo:rerun-if-changed=src");
let scan_cfg = kx_openapi_scan::default_config(Some(&manifest_dir))?
    .with_output(&out)
    .with_openapi_info(title, description);
kx_openapi_scan::generate_with_config(scan_cfg)?;
```

## 何时回看 tools/openapi-scan

出现这些情况时，应回看扫描器实现或 README：

- 明明有路由，为什么没识别到
- 某种 handler 签名能不能被扫
- `target_bin`、`scan_dirs`、配置文件怎么影响结果
- 为什么某些应用只扫指定 `bins/<name>`
