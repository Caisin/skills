---
name: rust-cross-compile
description: |
  Use when 需要在 Rust 项目中做跨平台交叉编译、选择 `cargo zigbuild` 目标、确认 glibc 版本、补齐多平台构建校验，或维护 CI / 发布脚本中的 Linux、Windows、macOS 构建链路。

  触发场景：
  - 从 macOS ARM64 交叉编译到 Linux / Windows
  - 需要选择合适的 glibc target triple
  - 本地出现 `GLIBC_X.XX not found`、链接失败或目标平台运行失败
  - 需要更新 CI、pre-commit 或 release 脚本中的多平台构建步骤

  触发词：cross compile、zigbuild、cargo-zigbuild、glibc、target triple、交叉编译、跨平台编译、linux target、windows target
---

# rust-cross-compile

这个 skill 的重点不是“能不能编”，而是**如何为目标平台选对 target、把验证链路补完整，并避免 glibc/链接器坑。**

## 适用边界

### 适用

- 用 `cargo zigbuild` 交叉编译 Linux / Windows 目标
- 需要根据目标系统 glibc 版本选择 triple
- 需要维护多平台 CI / 发布脚本
- 需要给 Rust 项目补 macOS / Linux / Windows 的构建校验

### 不适用

- 只是普通 `cargo build` / `cargo test` 用法
- 只是单个平台 Rust 编译错误，不涉及跨平台 target / linker / glibc

## Reference Selection

按任务类型优先读取：

- 想快速知道工具准备、常用命令、target 选择
  - 读 `references/patterns.md`

## 核心规则

1. **Linux 目标优先明确 glibc 版本**
   - 不要默认用一个过高版本，导致目标机运行失败
2. **把“能编过”和“能部署运行”区分开**
   - 编译成功不等于目标环境一定可运行
3. **跨平台校验不要只看 build**
   - 需要同时考虑 lint、测试或至少最小执行验证
4. **优先用 `cargo-zigbuild` 简化 Linux/Windows 交叉编译**
   - 比手工配 linker 更稳定

## 常见错误 vs 正确做法

### 常见错误

```text
❌ Linux 目标直接用默认 triple，不核对目标机 glibc
❌ 只在本机 build 一次，就宣称支持多平台
❌ 把 CI 的 target 写对了，但没同步更新本地验证命令
```

### 正确做法

```text
✅ 先确认目标机器 glibc 版本，再选 x86_64-unknown-linux-gnu.<version>
✅ 提交前至少明确 macOS / Linux / Windows 三类验证命令
✅ 将 cargo-zigbuild、target add、CI target 配置保持一致
```

## 输出模板

```text
问题归类
建议 target / 工具链
建议验证命令
可能风险
下一步
```

## 完整示例

**Input**

```text
我在 M 系列 Mac 上要给 Linux x86_64 和 Windows x86_64 出包，怎么选 zigbuild target，怎么避免 glibc 坑？
```

**Output direction**

```text
- 命中 rust-cross-compile
- 先给出 cargo-zigbuild + rustup target add 的最小工具准备
- 再给出 Linux/Windows 常用 target
- 强调 Linux 要先确认 glibc 版本
- 最后补最小验证链路与常见错误
```
