---
name: write-tests
description: |
  Use when 在当前 Rust workspace 中新增或修改单元测试、集成测试、doc test 或编译期测试。

  触发场景：
  - 为 bug 补回归测试
  - 为公共 API 或 crate 行为新增测试
  - 判断测试应放 inline module、crate tests/ 还是 doc test

  触发词：测试、回归测试、单元测试、集成测试、doc test、tokio::test、write tests、test first
---

# Writing kx-rs Tests

测试位置由行为边界决定：公共行为优先从 crate 外验证，复杂私有逻辑在相邻模块内验证，公共示例优先使用 doc test。

## 适用边界

### 适用

- 新增或修改 Rust 测试代码
- 为修复锁定失败行为
- 设计最小充分测试矩阵

### 不适用

- 只运行现有测试，应按目标 crate 直接执行
- 依赖数据库/Redis/网络环境的专项运行方式，应同时使用 `database-tests`

## Reference Selection

- 测试位置、结构和断言模式
  - 读 `references/patterns.md`
- 外部服务与数据库前置条件
  - 使用 `database-tests` skill
- 公共示例规范
  - 读 `../../../docs/src/rustdoc-guidelines.md`

## 核心规则

1. Bugfix 先写能在修改前失败的最小回归测试，再实现修复。
2. 公共 API/跨模块行为优先放 `<crate>/tests/`；私有算法与状态机放相邻 `#[cfg(test)] mod tests`。
3. derive/codegen 从生成代码的使用者视角测试；编译错误契约使用仓库已有的 UI/compile-test 模式，不新造框架。
4. 每个测试聚焦一个行为，复用与被测行为无关的 setup。
5. 不依赖执行顺序、共享全局状态或真实凭据；必须外部环境时显式隔离并说明前置条件。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 修复后才补一个无法证明回归的 happy-path 测试
❌ 为私有实现细节写脆弱断言
❌ 测试默认连接开发者本机数据库或外网
```

### 正确做法

```text
✅ 断言用户可观察的结果、错误或状态变化
✅ 用目标 crate 的既有 helper 与测试组织方式
✅ 先跑单个测试，再扩大到 crate 和 workspace
```

## 输出模板

```text
待锁定行为
测试位置
失败条件
断言与 fixture
运行命令
扩大验证条件
```

## 完整示例

**Input**

```text
这个查询条件反序列化有边界 bug，先补测试。
```

**Output direction**

```text
- 在现有 cond 测试模块补最小失败输入
- 同时覆盖预期结果与不应接受的输入
- 先运行目标测试，再运行目标 crate 测试
```
