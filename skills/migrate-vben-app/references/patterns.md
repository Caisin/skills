# Vben 应用迁移模式

本 reference 说明如何把旧 Vben 管理端迁移为新版 monorepo 中的独立业务 app。示例中的 `<product>`、`<old-app>` 和 remote 名称都应替换为目标仓库的真实值。

## 1. 先确认三层仓库边界

常见拓扑：

```text
父仓
└── web/                     # Vben Git submodule
    ├── apps/<product>/      # 自有 PC 管理端
    ├── packages/            # Vben 公共框架包
    └── pnpm-workspace.yaml
```

- 父仓提交 `.gitmodules` 和 `web` gitlink。
- Vben fork 提交 `apps/<product>`、必要的 workspace 配置和 lockfile。
- `upstream` 指向官方 Vben，`origin` 指向可写 fork。
- 先读取 `git remote -v`，不要假设 remote 名称或覆盖已有 remote。

## 2. 迁移前建立闭包清单

不要直接复制整个旧应用。先从以下入口生成清单：

1. 路由、菜单、`pageMap` 或动态组件映射中的页面。
2. 页面静态 import、动态 import 和别名 import。
3. 页面调用的 API client、DTO、权限 code 和字典/资源选项。
4. 表格、表单、弹窗、抽屉、编辑器、上传、图标和富文本扩展。
5. 应用启动、认证、路由守卫、错误处理、国际化和主题覆盖。
6. `package.json` 中旧应用直接使用的 npm 包。

建议按业务域记录：

```text
业务域 | 路由/页面 | API | 权限 | 共享组件 | npm 依赖 | 状态
```

删除旧域前，确认它不在上述任一清单中。被保留页面引用的共享文件应最小恢复，不必恢复整个已废弃产品域。

## 3. 建立目标 app

- 优先参考当前 upstream 中结构最接近的 app，复用其启动、配置、路由和构建模式。
- app package name 必须唯一，脚本直接调用当前 workspace 的标准命令。
- 业务私有 package 可放在 `apps/<product>/packages/<name>` 并用 workspace 支持的本地依赖协议引用。
- 不要因为旧项目有一套框架封装，就把它直接塞进 Vben 的 `packages/@core`。

## 4. 业务代码适配当前 Vben API

迁移以目标版本的类型定义和现有 app 用法为准，不以旧项目编译通过为准。

### Modal / Drawer 数据类型

类型参数放到 hook 创建处：

```ts
type DetailData = {
  id: string;
};

const [Modal, modalApi] = useVbenModal<DetailData>({
  onOpenChange(open) {
    if (!open) return;
    const data = modalApi.getData();
    if (!data) return;
    loadDetail(data.id);
  },
});
```

```ts
const [Drawer, drawerApi] = useVbenDrawer<DetailData>({
  onOpenChange(open) {
    if (!open) return;
    const data = drawerApi.getData();
    if (!data) return;
    loadDetail(data.id);
  },
});
```

禁止在框架层新增 `getData<T>()` 重载。目标 API 返回可空值时，业务页面必须显式处理未传数据的状态。

### 删除或改名的属性与图标

- 属性不存在时，先查目标版本类型和当前 app 示例；删除无效旧配置或改成新版公开能力。
- 图标不存在时，从当前 `@vben/icons` 已导出的图标中选语义相近项，不在框架包里恢复旧导出。
- 不用 `any`、`@ts-ignore` 或宽泛模块声明掩盖迁移错误。

## 5. API、路由和权限必须一起迁移

每个页面至少核对：

- route name/path/component/meta
- menu、权限 code、按钮级权限
- API path、method、query/body、分页字段和响应解包
- 详情/编辑弹窗传入数据
- 文件上传、下载、导入、导出
- 字典、枚举、资源树和级联选择数据源
- 认证过期、业务错误和空状态

前后端 API 暂时不一致时，应记录显式差异，不得悄悄删除按钮或页面来让 typecheck 通过。

## 6. workspace 依赖规则

- 先查 `pnpm-workspace.yaml` 的 catalog 和已有 workspace package。
- 多 app 共用的第三方版本写入 catalog；app 私有依赖保留在 app package。
- Vue、`@vue/compiler-sfc`、router 和关键 UI runtime 发生类型分裂时，用 `pnpm why` 检查解析树。
- Vue runtime 与 compiler 保持同版本单例；修正 workspace override 或 lockfile，不通过复制类型、降级检查或 `skipLibCheck` 回避。
- 更新依赖后提交 lockfile，并在 CI 模式下验证可重装。

## 7. fork 与 upstream 协作

```text
fork 主分支
  = upstream 历史 + 自有 apps/<product> + 必要 workspace 配置

官方 PR 分支
  = 从 upstream/main 新建 + 可独立复用的框架修复
```

- 定期 fetch upstream，并在 fork 分支合并或变基官方更新。
- 自有 app 不进入官方 PR。
- 只有不依赖自有业务、对所有 Vben 用户成立的修复，才适合向 upstream 提交。
- 合并 upstream 后重新运行 app 的完整验证矩阵，不能只确认 Git 无冲突。

## 8. 推荐迭代方式

1. 先让 app 骨架启动。
2. 每次迁移一个业务域及其依赖闭包。
3. 每个业务域完成后运行 typecheck 和目标测试。
4. 全域完成后运行生产 build。
5. 启动 dev server，用桌面浏览器验证登录、导航和关键 CRUD 流程。
6. 最后用遗漏清单反查旧应用，不以“构建成功”等价于“业务完整”。

## 9. 组件导出边界

应用私有组件按目录维护：

- `components/<module>/index.ts` 导出模块内组件、类型和工具。
- `components/index.ts` 只做各模块的汇总 `export *`。
- 不创建 `components/<module>.ts` 去重复转出 `components/<module>/`，避免同一模块出现两套导入入口。

## 常见错误

```text
❌ 先复制和删除目录，再依赖 typecheck 错误推断遗漏文件
❌ 修改 Vben 公共包，让旧业务调用继续编译
❌ 把 fork 自有 app 混入面向 upstream 的官方 PR
❌ 用多个 Vue 版本、any 或 skipLibCheck 掩盖依赖和类型分裂
✅ 先建立业务闭包清单，再逐域迁移、适配和验证
✅ 业务页面遵循目标 Vben 当前公开 API，框架保持可直接合并 upstream
```

## 正确做法

```text
✅ 先核实仓库与 remote，再建立迁移清单
✅ 以业务域为单位迁移完整依赖闭包，并逐域运行 typecheck
✅ 将版本适配留在业务 app，将通用框架包保持为 upstream 可合并状态
✅ 自动验证通过后再做桌面浏览器烟测和反向遗漏审计
```
