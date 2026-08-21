---
name: migrate-vben-app
description: |
  Use when 将旧版 Vben PC 管理端应用或业务模块迁移到新版 vue-vben-admin 的 `apps/<product>`，同时保持业务代码、框架代码、fork 与 upstream 的边界。

  触发场景：
  - 从旧 Vben / Vue 管理端迁移页面、路由、API、权限和共享组件
  - 在 Vben monorepo 中新增独立 `apps/<product>` 业务应用
  - 排查迁移后的页面、API、资源选项、编辑器、上传或权限能力是否遗漏
  - 处理 Vben 上游合并、fork 自有应用和官方 PR 分支隔离
  - 修复 `useVbenModal`、`useVbenDrawer`、图标、Vue 单例或 catalog 版本差异

  触发词：Vben、vue-vben-admin、PC 管理端、后台管理、apps、页面迁移、上游合并、upstream、useVbenModal、useVbenDrawer、pageMap
---

# Migrate Vben App

把旧 PC 管理端的业务能力迁入新版 Vben 应用，并让后续上游升级仍可正常合并。迁移目标是业务行为完整、框架零兼容补丁、依赖边界清晰。

## 适用边界

### 适用

- 在 Vben monorepo 的 `apps/<product>` 新增或迁移独立业务应用
- 迁移页面、路由、菜单、API、权限、上传、编辑器和业务共享组件
- 把旧组件调用改成目标 Vben 当前公开 API
- 维护父仓 submodule、Vben fork 和官方 upstream 的协作边界
- 审计迁移遗漏、依赖冲突和上游可合并性

### 不适用

- 设计或迁移 Rust 后端接口：按任务使用 `write-entity`、`write-svc`、`write-ctl`
- 单纯重做视觉体系：使用 UI / UX 相关 skill
- 修改 Vben 公共框架能力：先确认这是独立、可复用的新需求，不能以兼容旧业务页面为理由修改框架

## Reference Selection

- 规划目录、分支、页面和依赖迁移时，读 `references/patterns.md`
- 做遗漏审计、验收或提交前检查时，读 `references/verification-checklist.md`

## 不可违反的规则

1. `apps/` 属于 Vben 仓库内部；父仓只维护 Vben submodule 的 gitlink，不在父仓根目录重复创建同名应用。
2. 旧页面不兼容新版 API 时，修改业务页面；禁止给 `packages/@core`、`packages/effects` 等框架包添加旧 API 重载或兼容分支。
3. 迁移范围以业务能力闭包为准，不以“已复制页面目录”为准。路由页面引用到的 API、资源选项、共享组件、编辑器、上传、权限和类型必须一并核对。
4. 先建立页面清单和 API 清单，再复制和裁剪。不能先批量删除旧目录，再凭编译错误恢复依赖。
5. 应用私有共享代码放在应用内；只有两个以上应用确实复用且生命周期一致时，才提升为 Vben workspace 公共包。
6. 新依赖优先复用 workspace catalog；Vue、`@vue/compiler-sfc` 等运行时关键包保持单例和同版本，不能通过重复安装掩盖类型分裂。
7. fork 可长期保存自有 `apps/<product>`；面向官方的 PR 必须从干净的 `upstream/main` 建分支，不包含自有应用和产品配置。
8. 完成标准至少包含 typecheck、目标测试、生产构建和桌面端页面烟测；存在已知错误时不能宣称迁移完成。

## 最小迁移顺序

1. 确认仓库拓扑、remotes、目标 app 和所有权边界。
2. 生成页面、路由、API、共享依赖和 npm 依赖清单。
3. 基于目标 Vben 当前 app 结构建立 `apps/<product>`，再迁入业务代码。
4. 按目标框架 API 修正业务代码，逐域通过 typecheck。
5. 用闭包清单审计遗漏，运行测试、构建和浏览器烟测。
6. 分别提交 Vben fork、父仓 gitlink 和迁移文档；官方贡献使用独立干净分支。

## 常见错误 vs 正确做法

```text
❌ 为旧页面恢复 getData<T>() 等框架兼容重载
❌ 只按路由目录复制页面，遗漏 resource-options、上传、编辑器或权限辅助代码
❌ 在父仓根目录创建 apps/<product>，同时又把 Vben 作为 submodule
❌ 为解决 Vue 类型错误同时安装两个 patch 版本
✅ 把类型参数放到 useVbenModal<TData> / useVbenDrawer<TData>，并处理 getData() 的 undefined
✅ 以“页面 -> import -> API -> 权限 -> 资源”的闭包清单确认迁移完整性
✅ 自有应用留在 fork，官方 PR 从 upstream/main 建立且不携带业务代码
```

## 输出模板

```text
仓库与分支边界
业务迁移清单
框架 API 适配
依赖与共享代码
验证证据
遗漏与剩余风险
```

## 完整示例

**Input**

```text
把旧后台的订单模块迁到新版 Vben，后续还要能合并官方更新。
```

**Output direction**

- 先确认 Vben 仓库、父仓 submodule、fork 和 upstream 的关系。
- 从订单路由出发建立页面、API、权限、资源选项和共享组件闭包清单。
- 在 `apps/<product>` 修改旧业务代码适配新版组件 API，不修改框架包兼容旧调用。
- 统一 workspace 依赖后运行 typecheck、测试、build 和订单关键流程桌面烟测。
- 自有应用提交到 fork；若要给官方贡献修复，另从 `upstream/main` 建干净分支。
