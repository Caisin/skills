# Vben 应用迁移验收清单

本清单用于迁移审计和提交前验证。每一项应标记为通过、不适用或已知缺口。

## 仓库与所有权

- [ ] `apps/<product>` 位于 Vben 仓库内部，不是父仓重复目录。
- [ ] 父仓只提交 submodule 配置、gitlink 和父仓文档。
- [ ] fork 与 upstream remote 已核实，没有覆盖用户已有 remote。
- [ ] 自有 app 只提交到 fork；官方 PR 分支基于干净 upstream。
- [ ] 框架公共包中没有为旧页面新增的兼容重载、旧导出或条件分支。

## 业务完整性

- [ ] 旧路由、菜单和 `pageMap` 已逐项映射为迁移、废弃或延期。
- [ ] 每个保留页面的静态和动态 import 都已进入闭包清单。
- [ ] API path、method、请求 DTO、分页和响应解包与后端一致。
- [ ] 权限 code、路由 meta、按钮权限和登录守卫已核对。
- [ ] 资源选项、字典、枚举、树选择和级联数据源未遗漏。
- [ ] 上传、下载、导入、导出、编辑器和富文本扩展可用。
- [ ] 弹窗和抽屉的数据传递、关闭、重载流程可用。
- [ ] 明确记录未迁移模块及其原因，不能用删除页面隐藏缺口。

## API 适配与类型

- [ ] `useVbenModal<TData>` / `useVbenDrawer<TData>` 在创建处声明数据类型。
- [ ] `getData()` 的可空返回已由业务页面显式保护。
- [ ] 删除的属性和改名图标已按目标版本 API 修正。
- [ ] 没有新增 `any`、`@ts-ignore`、宽泛模块声明或关闭类型检查。
- [ ] Vue 与 `@vue/compiler-sfc` 保持单版本，未出现重复 VNode/Router 类型。
- [ ] 新依赖复用 catalog 或按 app 私有边界声明，lockfile 已更新。

## 自动验证

根据实际 package name 替换 `<app-package>`：

```bash
pnpm --filter <app-package> typecheck
pnpm exec vitest run apps/<product>/src
pnpm --filter <app-package> build
```

- [ ] typecheck 无错误。
- [ ] 目标单元/组件测试通过；无测试时已记录缺口。
- [ ] production build 成功。
- [ ] 依赖可在 CI 模式下按 lockfile 安装。

## 浏览器烟测

- [ ] 使用目标项目支持的 Node/pnpm 版本启动 dev server。
- [ ] 桌面视口下登录页、主布局、菜单和首屏无重叠或空白。
- [ ] 每个迁移业务域至少打开一个列表页和一个详情/编辑流程。
- [ ] 列表查询、分页、刷新、空状态和错误状态正常。
- [ ] 新增/编辑/删除等写操作与权限限制正常。
- [ ] 上传、富文本或复杂表单等高风险页面已单独检查。
- [ ] 浏览器 console 无未处理异常，关键请求无意外 404/500。
- [ ] 保存 Playwright 截图或等价证据，并记录未覆盖场景。

## 上游更新回归

- [ ] 合并最新 upstream 后重新运行 typecheck、测试和 build。
- [ ] 检查 `git diff upstream/main -- packages/`，确认没有业务兼容代码泄漏到框架包。
- [ ] 检查自有 app 与 workspace 配置的冲突解决没有丢失业务文件。
- [ ] 官方 PR diff 不包含 `apps/<product>`、产品配置或私有资产。

## 常见错误

```text
❌ 只记录 typecheck 和 build 成功，不核对页面、API 与权限清单
❌ 浏览器只打开登录页，没有检查迁移业务域的关键流程
❌ 合并 upstream 后只检查 Git 冲突，不重新运行 app 验证
✅ 自动验证与桌面烟测都留证据，并明确标记不适用项和已知缺口
```

## 正确做法

```text
✅ 清单项逐项标记通过、不适用或已知缺口
✅ typecheck、测试、build、浏览器烟测分别提供新鲜证据
✅ 将旧应用反查结果与迁移清单对照，明确延期和废弃项
✅ 合并 upstream 后完整重跑验证，而不是沿用合并前结果
```
