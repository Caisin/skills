# svc-mgr Patterns

用于 `svc-mgr` 的最小接入与判断规则。

## 适用场景

- 想快速接入 `svc-mgr`
- 想区分本地执行 / dry-run / 远端执行
- 想知道什么时候该用 CLI，什么时候该用库 API

## 推荐模板

### 1. 常规本地安装

```rust
use svc_mgr::{ServiceBuilder, ServiceManager, TypedServiceManager};

fn main() -> svc_mgr::Result<()> {
    let config = ServiceBuilder::new("com.example.myapp")?
        .program("/usr/bin/myapp")
        .args(["--port", "8080"])
        .working_directory("/opt/myapp")
        .env("RUST_LOG", "info")
        .description("My Application Service")
        .autostart(true)
        .restart_on_failure(5, 3)
        .build()?;

    let manager = TypedServiceManager::native()?;
    manager.install(&config)?.exec()?;
    manager.start(&config.label)?.exec()?;
    Ok(())
}
```

### 2. 远端动作生成

```rust
use svc_mgr::{CmdOutput, ServiceBuilder, ServiceManager, ServiceManagerKind, TypedServiceManager};

let config = ServiceBuilder::new("com.example.myapp")?
    .program("/usr/bin/myapp")
    .build()?;

let manager = TypedServiceManager::target(ServiceManagerKind::Systemd)?;
let action = manager.install(&config)?;
let preview = action.commands();

let parsed = action.parse(&[CmdOutput {
    exit_code: Some(0),
    stdout: String::new(),
    stderr: String::new(),
}])?;
```

## 常见错误

```text
❌ 开发机是 macOS，就直接用 native() 生成 systemd 远端命令
❌ 以为 log / username / environment 在所有后端都有完全一致的表现
❌ 已经需要 contents/raw template 了，还继续试图只靠 CLI 参数表达
```

## 正确做法

```text
✅ 远端目标后端用 target(kind)
✅ 高度可定制场景优先使用库 API，而不是硬塞进 rsvc
✅ 讨论字段行为时，始终带上具体后端上下文
```
