# Uni-App Core Patterns

用于 `uni-app-core` 的核心 API 与兼容性问题。

## 适用场景

- 查询官方 API
- 排查平台兼容差异
- 说明 navigation / storage / file / keyboard 能力

## 推荐做法

```text
先回答平台边界
-> 再给最小 API 示例
-> 最后补官方参考文件
```

## 常见错误

```text
❌ 不区分 H5 / App / 小程序
❌ 把组件库问题混进核心 API 回答
```

## 正确做法

```text
✅ 回答时显式标注平台支持情况
✅ 具体 API 细节优先回看 references/api.md
✅ 组件问题 handoff 到具体组件库 skill
```
