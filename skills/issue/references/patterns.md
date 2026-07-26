# Issue Patterns

用于编写可复现 bug report 与可讨论 feature proposal。

## Bug report

```text
标题
操作与最小复现
预期行为
实际行为（完整错误）
受影响 crate/feature
Rust、OS、数据库或外部服务版本
```

## Feature proposal

```text
当前问题
建议的公共 API/行为
替代方案与拒绝原因
影响范围与兼容性
是否需要设计文档
```

## 常见错误

```text
❌ 只有截图，没有可复制的错误或命令
❌ 把未经验证的根因写成结论
❌ 在 issue 中包含 token 或真实连接串
```

## 正确做法

```text
✅ 最小复现独立于业务私有代码
✅ 标明 feature flags 与外部环境
✅ 证据和推断分开书写
```
