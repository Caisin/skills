---
name: sync-docs
description: |
  Use when 根据代码变更或 Git 历史同步当前仓库的 mdBook、rustdoc、README、设计记录和长期记忆。

  触发场景：
  - 更新、同步、审计或补齐项目文档
  - 检查近期公共行为变化是否已进入文档
  - 修正文档与源码、Cargo features 或目录结构的漂移

  触发词：同步文档、更新文档、文档审计、sync docs、rustdoc、mdBook、长期记忆
---

# Sync kx-rs Documentation

同步文档时先确定变更范围，再逐层修正受影响的规范源，不做无依据的整库重写。

## 适用边界

### 适用

- 根据 commit 范围同步公共文档
- 修正 mdBook、rustdoc、README、设计记录或长期记忆
- 检查 crate 清单与文档索引漂移

### 不适用

- 只改一处已明确的错别字
- 没有代码或历史依据的全面文案重写

## Reference Selection

- 文档表面、规范源和验证矩阵
  - 读 `../../../docs/dev/README.md`
- 文档措辞
  - 使用 `prose` skill
- 扫描和映射模式
  - 读 `references/patterns.md`

## 核心规则

1. 用户给定 commit/date 时使用该范围；否则比较各文档表面的最近变更，选择可解释的下界。
2. 只把用户可观察行为、公共 API、默认值、feature、Schema/迁移、安全和外部协议变化列入同步清单。
3. 写新内容前先搜索并修正已经失效的旧结论。
4. mdBook 负责认知地图，rustdoc 负责 API 真相，设计文档负责决策记录，长期记忆负责跨任务稳定边界。
5. 文档更新后运行对应验证，并明确没有运行的项。

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 看到新 API 就只追加一段，不检查旧描述
❌ 把 docs/book/ 生成物当源文件修改
❌ 用 cargo build 代替 mdBook 链接验证
```

### 正确做法

```text
✅ 先列“commit/变更 -> 文档表面”映射
✅ 在 docs/src/ 与源码 rustdoc 中修改规范源
✅ 将新的稳定边界提炼到 long-term-memory
```

## 输出模板

```text
扫描范围
用户可观察变化
受影响文档
已修正的旧结论
验证结果
剩余缺口
```

## 完整示例

**Input**

```text
同步最近两周的公共 API 文档。
```

**Output direction**

```text
- 扫描两周内提交并筛选公共行为变化
- 映射到 docs/src、rustdoc、README 和长期记忆
- 运行 mdbook、cargo doc 与相关 doc tests
```
