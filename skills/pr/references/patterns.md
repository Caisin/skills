# Pull Request Patterns

用于从 base branch 到 `HEAD` 的完整 diff 编写 PR。

## 取证顺序

```bash
rtk git branch --show-current
rtk git diff <base>...HEAD
rtk git log --oneline <base>..HEAD
```

## 推荐模板

```text
## 变更
- 解决的问题
- 净改动与原因

## 验证
- `rtk cargo test -p <crate>`：通过

## 影响
- 公共 API / 配置 / Schema / 安全 / 文档

## Review 重点
- 需要确认的边界或剩余风险
```

## 常见错误

```text
❌ 从最后一个 commit 推导整个 PR
❌ 写计划而不是已完成的净改动
❌ 用“全部通过”代替实际命令
```

## 正确做法

```text
✅ title 能成为 squash commit subject
✅ 验证项逐条对应真实输出
✅ 未验证项与原因可见
```
