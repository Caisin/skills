---
name: vue-vben-admin
description: >
  Vue Vben Admin v5 企业级后台管理框架开发指南。基于 Vue 3 + Vite + TypeScript 的 pnpm Monorepo 架构，
  支持 Ant Design Vue、Element Plus、Naive UI、TDesign 多 UI 库切换。
  Use when: (1) 在 vue-vben-admin 项目中开发新页面、组件或功能
  (2) 使用 VbenForm 表单、VxeTable 表格、VbenModal 弹窗、VbenDrawer 抽屉等框架组件
  (3) 配置路由、菜单、权限控制
  (4) 配置 HTTP 请求、API 接口
  (5) 处理主题、国际化、偏好设置
  (6) 理解框架架构、Monorepo 结构、适配器模式
  (7) 创建新的应用模板或扩展框架功能
---

# Vue Vben Admin v5 开发指南

Vue Vben Admin 是基于 Vue 3 + Vite + TypeScript 的企业级后台管理框架，采用 pnpm Monorepo + TurboRepo 架构。

## 核心概念

- **Monorepo 架构**: `apps/` (应用) + `packages/` (共享包) + `internal/` (内部工具)
- **UI 库无关**: 通过 `adapter/component/` 适配器模式支持多 UI 库
- **路径别名**: `#/*` 映射到 `./src/*`

## 应用启动流程

```
main.ts → initPreferences() → bootstrap()
  → initComponentAdapter()  // 注册 UI 组件适配器
  → initSetupVbenForm()     // 初始化表单系统
  → createApp() → setupI18n → initStores → registerDirectives → router → mount
```

## 新建页面快速流程

1. **创建视图**: `src/views/your-module/index.vue`
2. **定义路由**: `src/router/routes/modules/your-module.ts`
3. **添加 API**: `src/api/your-module.ts`
4. **添加国际化**: `src/locales/langs/zh-CN.json` / `en-US.json`

### 路由定义模板
```typescript
import type { RouteRecordRaw } from 'vue-router';
import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: { icon: 'lucide:icon-name', order: 100, title: $t('module.title') },
    name: 'ModuleName',
    path: '/module',
    children: [
      {
        name: 'SubPage',
        path: '/module/sub',
        component: () => import('#/views/module/sub/index.vue'),
        meta: { title: $t('module.sub.title'), icon: 'lucide:icon' },
      },
    ],
  },
];
export default routes;
```

### 视图模板 (CRUD 页面)
```vue
<script lang="ts" setup>
import type { VxeGridProps } from '#/adapter/vxe-table';
import { Page, useVbenModal } from '@vben/common-ui';
import { Button, message } from 'ant-design-vue';
import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { getListApi, deleteApi } from '#/api/module';
import EditModal from './edit-modal.vue';

const [Modal, modalApi] = useVbenModal({ connectedComponent: EditModal });

const gridOptions: VxeGridProps = {
  columns: [
    { type: 'seq', width: 50 },
    { field: 'name', title: '名称' },
    { field: 'status', title: '状态', cellRender: { name: 'CellTag' } },
    {
      title: '操作', width: 160,
      cellRender: {
        name: 'CellOperation',
        options: ['edit', 'delete'],
        attrs: { onClick: onAction },
      },
    },
  ],
  proxyConfig: {
    ajax: {
      query: async ({ page }) => {
        const formValues = gridApi.formApi.form.values;
        return await getListApi({
          ...formValues,
          pageNo: page.currentPage,
          pageSize: page.pageSize,
        });
      },
    },
  },
};

const [Grid, gridApi] = useVbenVxeGrid({ gridOptions });

function onAction({ code, row }) {
  if (code === 'edit') modalApi.setData({ values: row }).open();
  if (code === 'delete') deleteApi(row.id).then(() => gridApi.reload());
}
</script>

<template>
  <Page title="模块管理">
    <Modal @success="gridApi.reload()" />
    <Grid>
      <template #toolbar-tools>
        <Button type="primary" @click="modalApi.open()">新增</Button>
      </template>
    </Grid>
  </Page>
</template>
```

## 详细参考文档

根据需要查阅以下参考文件：

- **框架架构**: [references/architecture.md](references/architecture.md) — Monorepo 结构、启动流程、适配器模式、包架构、环境配置
- **路由与权限**: [references/routing.md](references/routing.md) — 路由定义、meta 选项、前端/后端权限模式、路由守卫、权限指令
- **组件使用**: [references/components.md](references/components.md) — 组件索引，各组件文档见 `references/components/` 目录
- **请求与 API**: [references/request.md](references/request.md) — RequestClient 配置、API 定义模式、Auth Store、Mock 后端

## 关键文件位置 (以 playground 为例)

| 文件 | 用途 |
|------|------|
| `src/main.ts` | 应用入口 |
| `src/bootstrap.ts` | 应用启动配置 |
| `src/preferences.ts` | 偏好设置覆盖 |
| `src/adapter/component/index.ts` | UI 组件适配器 |
| `src/adapter/form.ts` | 表单适配器 |
| `src/adapter/vxe-table.ts` | 表格适配器 |
| `src/api/request.ts` | HTTP 请求客户端 |
| `src/api/core/` | 核心 API (auth, user, menu) |
| `src/router/routes/modules/` | 路由模块定义 |
| `src/router/access.ts` | 动态路由生成 |
| `src/router/guard.ts` | 路由守卫 |
| `src/store/auth.ts` | 认证 Store |
| `src/locales/` | 国际化文件 |
| `src/views/` | 页面视图 |

## 常用命令

```bash
pnpm dev:antd    # 启动 Ant Design Vue 应用
pnpm dev:ele     # 启动 Element Plus 应用
pnpm dev:play    # 启动 Playground
pnpm dev:docs    # 启动文档站
pnpm build:antd  # 构建 Ant Design Vue 应用
pnpm lint        # 代码检查
pnpm test:unit   # 单元测试
```
