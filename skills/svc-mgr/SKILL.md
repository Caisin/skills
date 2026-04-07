---
name: svc-mgr
description: |
  Use when 需要在 Rust 项目中接入、复用或维护 `svc-mgr` 这个跨平台服务管理 crate，处理 `ServiceBuilder` / `ServiceManager` / `TypedServiceManager` / `rsvc` CLI 的用法，或排查 launchd、systemd、openrc、rc.d、sc.exe、winsw 等后端行为差异。

  触发场景：
  - 需要把程序安装成系统服务，且希望一套代码覆盖多平台
  - 需要生成远端可执行命令，而不是立即在本机执行
  - 需要维护 `rsvc` CLI、平台模板或 `ServiceAction` 执行模型
  - 需要判断某个字段或重启策略在不同后端是否真的生效

  触发词：svc-mgr、rsvc、ServiceBuilder、ServiceAction、TypedServiceManager、launchd、systemd、openrc、winsw、系统服务、服务管理、跨平台服务
---

# svc-mgr

`svc-mgr` 的核心不是“直接帮你启动服务”，而是先构造 `ServiceAction`，再决定本地执行、命令预览，还是远端执行后回传解析。

## 适用边界

### 适用

- 在业务项目里接入 `svc-mgr` 管理系统服务
- 维护 `ServiceBuilder` / `ServiceConfig` / `ServiceManager` / `TypedServiceManager`
- 使用 `rsvc` 做 install / start / stop / restart / status / info / edit / list
- 判断不同后端对字段、日志、配置文件、user 级服务的支持差异
- 处理 SSH / agent / 控制面这类“生成动作给远端执行”的场景

### 不适用

- 只想管理环境变量
  - 看 `renv` 风格能力，不属于本 skill 主体
- 只想做 ratatui 终端交互界面
  - 看 `rtui` 相关 skill/实现
- 只是一般 Rust 编译错误、trait bound、生命周期问题
  - 交给通用 Rust / debugging 类 skill

## Reference Selection

按任务类型优先读取：

- 想快速知道该 crate 怎么接入、如何理解执行模型
  - 先读 `references/patterns.md`
- 想确认 Builder / Action / Label / probe / API 边界
  - 读 `references/api.md`
- 想确认 `rsvc` CLI 选项、平台矩阵、后端行为差异
  - 读 `references/cli-and-platforms.md`

## 核心规则

1. **先分清 `target(kind)` 还是 `native()`**
   - `target(kind)`：为目标后端生成动作，可跨 OS
   - `native()`：只探测当前机器本机后端
2. **先分清 `.exec()` / `.commands()` / `.parse()`**
   - 本地执行：`.exec()`
   - dry-run / 远端下发前审查：`.commands()`
   - 远端执行后解析：`.parse()`
3. **不要假设统一字段在所有后端都等价生效**
   - `openrc` / `rc.d` 更偏脚本降级
   - `sc.exe` 不走配置文件模型
   - `winsw` 会按 XML / WinSW 能力映射字段
4. **trait 能力大于 CLI 能力**
   - 库层有 `enable/disable/available/contents/reset_after_secs` 等粒度
   - `rsvc` 只覆盖常见生命周期操作
5. **只有 launchd / systemd 支持 `ServiceLevel::User`**
   - 其它后端只支持 system 级

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 把 `native()` 当成“目标服务器后端探测”
❌ 以为 `ServiceConfig` 的每个字段在所有后端都完整生效
❌ 想用 `rsvc` 覆盖所有库层能力，忽略 API/CLI 边界
❌ 远端执行场景里直接 `.exec()`，而不是先 `.commands()`
```

### 正确做法

```text
✅ 远端/跨平台命令生成优先 `TypedServiceManager::target(...)`
✅ 先确认是本地执行、预览命令还是远端解析三种模式中的哪一种
✅ 讨论字段行为时，明确后端差异与降级约定
✅ 复杂配置、原始模板透传、细粒度控制优先直接使用库 API
```

## 输出模板

```text
问题归类
建议入口（crate API / rsvc CLI / 后端实现）
关键边界或降级约定
验证方式
下一步
```

## 完整示例

**Input**

```text
我想在 Rust 项目里把程序安装成 systemd 服务，但开发机是 macOS，还想先把命令生出来给远端执行，应该怎么做？
```

**Output direction**

```text
- 命中 svc-mgr
- 先强调 `TypedServiceManager::target(ServiceManagerKind::Systemd)`，不要用 native()
- 再强调 install() 返回 ServiceAction，可先 commands() 审查再给远端执行
- 如需结果解析，再介绍 parse(CmdOutput)
- 如需更多字段/CLI 细节，指向 references/api.md 与 references/cli-and-platforms.md
```
