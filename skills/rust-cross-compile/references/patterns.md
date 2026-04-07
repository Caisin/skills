# Rust Cross Compile Patterns

用于 `rust-cross-compile` 的最小可复用参考。

## 适用场景

- 需要从 macOS ARM64 编到 Linux / Windows
- 需要选 Linux glibc 版本
- 需要补多平台验证命令

## 推荐模板

### 工具准备

```bash
brew install zig
cargo install cargo-zigbuild
rustup target add x86_64-unknown-linux-gnu
rustup target add x86_64-pc-windows-gnu
rustup target add aarch64-unknown-linux-gnu
```

### 常用命令

```bash
cargo zigbuild --release --target x86_64-unknown-linux-gnu.2.35
cargo zigbuild --release --target x86_64-pc-windows-gnu
cargo zigbuild --release --target aarch64-unknown-linux-gnu.2.35
```

### glibc 选择速查

```text
Ubuntu 22.04 -> x86_64-unknown-linux-gnu.2.35
Ubuntu 20.04 / Debian 11 -> x86_64-unknown-linux-gnu.2.31
Ubuntu 18.04 -> x86_64-unknown-linux-gnu.2.27
CentOS 7 -> 更保守版本或改用 musl
```

## 常见错误

```text
❌ 不确认目标机 glibc，就直接拿高版本 triple 构建
❌ 只做 cargo build，不做多平台最小验证
❌ CI 用一套 target，本地手工验证又是另一套
```

## 正确做法

```text
✅ 目标机先跑 ldd --version 确认 glibc
✅ 本地、CI、发布脚本共用同一批 target 约定
✅ Linux 需要更强可移植性时考虑 x86_64-unknown-linux-musl
```
