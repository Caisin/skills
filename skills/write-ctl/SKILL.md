---
name: write-ctl
description: |
  Use when 编写或修改 kx-axum 的 DTO、controller、ApiRouter、ApiMeta、extractor、统一响应和接口安全策略。

  触发场景：
  - 编写 `src/dto/<subdomain>/*.rs` 或 `src/ctl/<subdomain>/*.rs`
  - 使用 `QsQuery`、`Paging`、`Path`、`Json`、`R<T>`、`AxumErr`
  - 通过 `ApiRouter` 注册路由、API code、summary、access、encryption 或 external callback
  - 按功能拆分 ctl/dto/router 并生成 `RegisteredRouter`

  触发词：ctl、controller、handler、DTO、router、ApiRouter、ApiMeta、R、AxumErr、QsQuery、Paging、Path、Json、接口、路由、API code、回调
---

# Write Ctl

负责 HTTP 协议适配和公开接口契约。ctl 保持薄，业务规则和事务全部交给 svc。

## 适用边界

### 适用

- request/response DTO、extractor、handler 和错误映射
- `ApiRouter`、`ApiMeta`、路由聚合和 catalog
- 公开、仅认证、受保护、明文、加密和第三方回调策略
- ctl/dto/router 按业务功能拆文件

### 不适用

- 数据库模型、字段、Schema 和索引：使用 `write-entity`
- 查询、事务、幂等、CAS 和多表组装：使用 `write-svc`
- Axum 框架核心行为修改：直接检查 `crates/axum`

## Reference Selection

- 写 DTO、handler、路由或安全策略时读 `references/patterns.md`
- 接口回归测试同时使用 `write-tests`

## 核心规则

1. ctl 只负责提取参数、调用 svc、转换统一响应；不直接开启事务或编排多表写入。
2. DTO 按接口契约定义，不直接暴露包含密文、token、内部 version 等字段的完整 entity。
3. 使用 `ApiRouter + ApiMeta + finish()` 注册 method、path、稳定 API code、summary 和策略。
4. 默认策略保持受保护且加密；公开、仅认证、明文和第三方回调必须显式声明。
5. 第三方回调同时要求 ingress 与明确 plaintext，不能因公开而跳过入口认证。
6. 不用裸 `axum::Router` 或 `into_unmanaged_router()` 绕过正常 catalog。
7. `ctl/`、`dto/` 按功能拆文件；`mod.rs` 只声明模块和稳定重导出。
8. 路由 path 使用 Axum 0.8 `{id}` 语法，不使用 `/:id`。
9. 分页 handler 分别使用 `QsQuery<查询条件>` 和 `QsQuery<Paging>`；查询 DTO 不重复定义 `page`、`page_size`、`size` 或 `paging()`。
10. 两个 `QsQuery` 都会解析完整 query string，分页查询 DTO 不使用 `deny_unknown_fields`，否则会把 `page/page_size/size` 误判为未知字段。

## 常见错误 vs 正确做法

```text
❌ 在 handler 中直接开启事务或编排多表写入
❌ 直接返回包含密文、token 或内部状态的完整 Model
❌ 用裸 Router 绕过 ApiCatalog，或让公开接口隐式变成明文
❌ 使用 `Query<PageQuery>`，或在业务查询 DTO 中重复定义 `page/page_size/size`
✅ ctl 只适配协议，业务规则交给 svc，安全策略显式登记
✅ `QsQuery(req): QsQuery<ItemQuery>` 与 `QsQuery(page): QsQuery<Paging>` 分别提取条件和分页
```

## 输出模板

```text
接口契约
DTO 与 handler
路由与安全策略
目录落点
验证方式
```

## 完整示例

**Input**

```text
给参数模块增加分页、详情、保存、删除和缓存刷新接口。
```

**Output direction**

- DTO、ctl 按参数功能拆文件。
- handler 只调用 `ParamSvc` 并返回 `R<T>`。
- `ApiRouter` 显式登记稳定 code 和 summary。
- 缓存刷新和写入一致性留在 svc。
