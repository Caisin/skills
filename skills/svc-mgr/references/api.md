# svc-mgr API Reference

## 适用场景

- 需要快速确认 `svc-mgr` 的公开 API 与执行模型
- 需要判断库 API 与 CLI 的能力边界
- 需要确认字段与后端之间的映射关系

## 推荐模板

### `ServiceBuilder`

```rust
ServiceBuilder::new("com.example.myapp")?
    .program("/usr/bin/myapp")
    .args(["--port", "8080"])
    .working_directory("/opt/myapp")
    .env("KEY", "VALUE")
    .username("myapp")
    .description("My App")
    .autostart(true)
    .restart_policy(RestartPolicy::Always { delay_secs: Some(5) })
    .restart_on_failure(5, 3)
    .log("/var/log/app.log")
    .stdout_file("/var/log/app.out.log")
    .stderr_file("/var/log/app.err.log")
    .contents("raw service file content")
    .build()?
```

规则：

- `program(...)` 必填
- `log(path)` 会同时设置 `stdout_file` 与 `stderr_file`
- 若未显式设置 `stdout_file` 且存在 `working_directory`，默认补 `logs/{label.to_script_name()}.log`
- `contents(...)` 会跳过平台模板生成

### `ServiceAction`

- `.exec()`：本地执行
- `.commands()`：命令预览
- `.parse(outputs)`：远端执行后解析

常用 step / helper：

- `write_file(path, data, mode)`
- `remove_file(path)`
- `read_dir(path, extension)`
- `read_file(path)`
- `cmd(program, args)`
- `cmd_ignore_error(program, args)`
- `with_parser(...)`
- `merge(other)`
- `steps()`
- `commands()`

### `TypedServiceManager` / `ServiceManagerKind`

```rust
let native = TypedServiceManager::native()?;
let systemd = TypedServiceManager::target(ServiceManagerKind::Systemd)?;
```

规则：

- `target(kind)`：显式目标后端，可跨平台生成动作
- `native()`：只探测当前机器本机后端
- Windows `native()`：优先 `WinSw`，找不到再回退 `Sc`
- Linux `native()`：优先 `Systemd`，再尝试 `OpenRc`

### `ServiceLabel`

| 输入 | `to_qualified_name()` | `to_script_name()` |
|------|-----------------------|--------------------|
| `"myapp"` | `myapp` | `myapp` |
| `"example.myapp"` | `example.myapp` | `example-myapp` |
| `"com.example.myapp"` | `com.example.myapp` | `example-myapp` |

## 常见错误

```text
❌ 把 target(kind) 和 native() 混为一谈
❌ 以为 contents 会和平台模板字段自动合并
❌ 忽略后端差异，假设所有字段在所有后端等价生效
```

## 正确做法

```text
✅ 远端/跨平台场景优先 target(kind)
✅ 原始模板透传时明确走 contents，而不是期待模板与 raw content 双向合并
✅ 讨论字段行为时显式带上后端上下文
```

## 补充说明

- 库层支持 `contents`、`enable/disable`、`available()`、`reset_after_secs` 等更细粒度能力
- `rsvc` 更偏常见生命周期操作
- launchd / systemd：字段承载最完整
- openrc / rc.d：以脚本为主，会向脚本语义降级
- sc.exe：没有配置文件模型，核心是 create/config 命令参数
- winsw：通过 XML 承载大部分字段，但仍会按 WinSW 能力映射/降级
