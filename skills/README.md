# 按需使用

`SKILL.md` 是自动发现入口，领域资料只在相关任务中读取。通用工程判断集中在 `karpathy-guidelines`，不叠加固定的调查、补丁、重构、迁移与验收流程。

以下原入口已改为同目录 `GUIDE.md`，脚本和参考资料原位保留，不自动触发：`cavecrew`、`caveman*`、`investigate-first`、`lean-build`、`migration`、`safe-refactor`、`surgical-patch`、`verify-and-stop`。它们仅供明确需要旧工作流或工具时参考，不覆盖当前用户目标或仓库约定。

设计资料仍通过 `design` 按交付物选择；业务开发通过 `write-entity`、`write-svc`、`write-ctl` 查真实框架契约。无需为普通任务加载所有 skill 或参考。
