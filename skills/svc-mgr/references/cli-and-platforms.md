# svc-mgr CLI And Platforms

## 适用场景

- 需要查看 `rsvc` CLI 的选项与行为
- 需要确认各平台后端的配置载体、user 级支持与关键差异
- 需要判断某件事该走 CLI 还是直接走库 API

## 推荐模板

### `rsvc` 全局选项

```text
--user
--backend <launchd|systemd|openrc|rcd|sc|winsw>
--dry-run
```

- 全局选项可放在子命令前后
- `--backend` 会直接选择目标后端生成动作，不依赖当前开发机 OS
- 省略 `--backend` 时才会调用 `TypedServiceManager::native()`
- `--user` 仅对 launchd / systemd 有意义
- `--dry-run` 只打印 `ServiceAction::commands()`
- `rsvc install --env` 遇到非法 `KEY=VALUE` 会忽略该项并打印提示，不会直接失败

### `rsvc` 子命令

```text
rsvc install <LABEL> --program <PATH> [OPTIONS]
rsvc uninstall <LABEL>
rsvc start <LABEL>
rsvc stop <LABEL>
rsvc restart <LABEL>
rsvc status <LABEL>
rsvc info <LABEL>
rsvc edit <LABEL>
rsvc list
```

### 平台后端矩阵

| 平台 | 后端 | 配置载体 | User 级别 | 备注 |
|------|------|----------|----------|------|
| macOS | launchd | plist | 支持 | 使用 `qualified_name + .plist` |
| Linux | systemd | unit file | 支持 | 使用 `script_name + .service` |
| Linux | openrc | script | 不支持 | 使用 `script_name` |
| BSD | rc.d | script | 不支持 | 使用 `script_name` |
| Windows | sc.exe | 无单独配置文件 | 不支持 | 安装/查询基于 `sc.exe` |
| Windows | winsw | XML | 不支持 | 使用 `qualified_name + .xml` |

## 常见错误

```text
❌ 以为 rsvc 覆盖了全部库层能力
❌ 在 sc.exe 后端里期待 edit 打开配置文件
❌ 把 --user 用在 openrc / rc.d / sc.exe / winsw 上
```

## 正确做法

```text
✅ rsvc 适合常见生命周期操作，细粒度能力直接走库 API
✅ 遇到 sc.exe 时明确说明它没有配置文件模型
✅ user 级服务仅在 launchd / systemd 语义下讨论
```

## 补充说明

- launchd：`install + autostart` 会尝试 `launchctl bootstrap`
- systemd：`install` 后会 `daemon-reload`，user 模式会补 `--user`
- openrc / rc.d：脚本型后端，不支持 user 级
- sc.exe：`enable/disable` 走 `sc.exe config`
- winsw：通过 XML 安装，`enable/disable()` 当前为空动作
