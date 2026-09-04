---
name: write-ctl
description: |
  Use when 编写 kx-axum DTO、handler、ApiRouter、ApiMeta、响应和接口安全策略。
  触发词：ctl、controller、handler、DTO、router、ApiRouter、ApiMeta、接口、回调
---

# Write Ctl

controller 只做 HTTP 协议适配；查询、校验、事务和多表编排进入 service。

## Reference Selection

- DTO、路由与安全策略：读 `references/patterns.md`。
- 接口回归：同时使用 `write-tests`。

## 核心规则

1. 使用 `ApiRouter + ApiMeta + finish()`，登记稳定 method、path、API code、summary 和访问策略。
2. 默认保持受保护且加密；公开、仅认证、明文和第三方回调必须显式声明，回调仍需 ingress。
3. DTO 不直接暴露密文、token、内部 version 等实体字段。
4. 分页分别提取 `QsQuery<条件>` 与 `QsQuery<Paging>`；过滤 DTO 不重复分页字段，也不使用 `deny_unknown_fields` 排斥另一组 query 参数。
5. 单表公开字段可直接使用生成 Query；有别名、组合条件或隐藏字段时定义协议 DTO，由 svc 映射。
6. 路径使用 Axum 0.8 `{id}`；不使用裸 `Router` 绕过 catalog。
7. 单个业务实现文件不超过 1000 行；按功能拆到 `ctl/<domain>.rs`，`mod.rs` 只声明和重导出，禁止 `include!`。

## 验证

运行路由 catalog、DTO 反序列化和目标 crate 测试；安全策略变更必须覆盖未登录、无权限和正常路径。
