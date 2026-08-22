---
name: kx-design
description: |
  Use when 为 KX 仓库新增或修改非平凡功能的设计文档，需要明确公共契约、数据一致性、兼容性与验证计划。

  触发场景：
  - 新增或破坏性修改公共 API
  - 调整 Schema、迁移、事务、安全或第三方协议边界
  - 进行跨 crate 架构设计或评审设计文档
  - 需要区分仓库工程设计与 UI / 品牌视觉设计

  触发词：KX 设计文档、kx-design、design doc、架构设计、API 设计、Schema 设计、迁移方案、兼容性方案
---

# KX Design Documents

设计文档位于 `docs/dev/design/`，用于约束非平凡变更的可观察行为和长期边界。UI、品牌、Logo 和视觉资产设计继续使用 `design`；KX 工程契约设计使用本 skill。

## 适用边界

### 适用

- 公共 API、derive/codegen 契约或 workspace 架构变化
- 数据库 Schema、迁移、事务、多数据源或缓存一致性变化
- 安全、密钥、认证或第三方协议边界变化
- 跨 crate 依赖、兼容性和分阶段迁移设计

### 不适用

- 品牌、Logo、设计系统、Banner 或 UI 视觉设计：使用 `design`
- 不改变行为的局部重构
- 单点 bug 修复、测试补充或文字纠错

## Reference Selection

- 章节顺序与内容要求
  - 读 `../../../docs/dev/design/_template.md`
- 生命周期与适用条件
  - 读 `../../../docs/dev/design/README.md`
- 写作风格
  - 使用 `prose` skill，并读 `../../../docs/dev/WRITING.md`
- 设计检查清单
  - 读 `references/patterns.md`

## 核心规则

1. 从模板创建 `docs/dev/design/<feature-name>.md`；大型迁移可使用主目录和分步骤设计文档，但必须有一个总览入口。
2. 先写用户可观察行为，再写会约束正确性的实现边界；不把源码目录清单当设计。
3. 数据、事务、安全和兼容性必须显式判断；不适用时说明原因。
4. 设计示例是示意代码，不加 doctest 隐藏样板；公共文档中的稳定示例仍优先可执行。
5. 实现完成后更新状态、偏差和验证证据，并提炼长期知识。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 只列要修改的文件，没有定义行为和兼容性
❌ 把开放问题藏在实现阶段
❌ 为了填模板保留空章节
❌ 公共 API / Schema 设计误用 UIRO 的视觉 design skill
```

### 正确做法

```text
✅ 用调用示例、错误语义和迁移方式定义契约
✅ 明确事务、并发、Schema 与安全边界
✅ 记录被拒绝方案，减少重复推导
✅ 工程设计使用 kx-design，视觉设计使用 design
```

## 输出模板

```text
设计文档路径
用户可观察变化
关键边界
开放问题
验证计划
```

## 完整示例

**Input**

```text
给多数据源 alias 的重连语义写一份 KX 设计文档。
```

**Output direction**

```text
- 从模板创建文档
- 定义 alias 是否复用 ModelSet、连接何时发布、remove/unregister 差异
- 覆盖并发、一致性、兼容性与回归测试
```
