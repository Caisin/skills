# Vue Vben Admin Architecture

## Table of Contents
- [Project Overview](#project-overview)
- [Monorepo Structure](#monorepo-structure)
- [Application Bootstrap Flow](#application-bootstrap-flow)
- [Component Adapter Pattern](#component-adapter-pattern)
- [Package Architecture](#package-architecture)
- [Environment Configuration](#environment-configuration)

## Project Overview

Vue Vben Admin v5 is a Vue 3 + Vite + TypeScript enterprise admin framework. It is a **pnpm monorepo** managed by **TurboRepo**, supporting multiple UI libraries: Ant Design Vue, Element Plus, Naive UI, TDesign.

**Requirements:** Node.js >= 20.19.0, pnpm >= 10.0.0

**Tech Stack:** Vue 3.5, Vite 7, TypeScript 5.9, Pinia 3, Vue Router 4, Tailwind CSS 3, Axios, Zod, VXE Table 4, vue-i18n 11, Iconify/Lucide icons, Nitro (mock server), Vitest + Playwright.

## Monorepo Structure

```
vue-vben-admin/
├── apps/                    # Application projects
│   ├── backend-mock/        # Nitro mock backend (@vben/backend-mock)
│   ├── web-antd/            # Ant Design Vue app (@vben/web-antd)
│   ├── web-ele/             # Element Plus app (@vben/web-ele)
│   ├── web-naive/           # Naive UI app (@vben/web-naive)
│   └── web-tdesign/         # TDesign app (@vben/web-tdesign)
├── docs/                    # VitePress documentation site
├── internal/                # Internal build/lint tooling
│   ├── lint-configs/        # ESLint, Prettier, Stylelint, Commitlint
│   ├── node-utils/          # Node.js utilities
│   ├── tailwind-config/     # Shared Tailwind config
│   ├── tsconfig/            # Shared TypeScript configs
│   └── vite-config/         # Shared Vite config
├── packages/                # Core framework packages
│   ├── @core/               # Low-level core (@vben-core/*)
│   │   ├── base/design/     # Design tokens, CSS variables
│   │   ├── base/icons/      # Icon components
│   │   ├── base/shared/     # Shared utilities
│   │   ├── base/typings/    # Core TypeScript types
│   │   ├── composables/     # Vue composables
│   │   ├── preferences/     # Core preference system
│   │   └── ui-kit/          # UI components (form-ui, layout-ui, menu-ui, popup-ui, shadcn-ui, tabs-ui)
│   └── effects/             # Higher-level packages (@vben/*)
│       ├── access/          # Access control, permission directives
│       ├── common-ui/       # Common UI (Form, Modal, Drawer, VxeTable, etc.)
│       ├── hooks/           # Vue hooks
│       ├── layouts/         # Layout components
│       ├── plugins/         # Third-party plugin integrations
│       └── request/         # HTTP request client
├── packages/constants/      # Shared constants
├── packages/icons/          # Icon re-exports
├── packages/locales/        # i18n locale files
├── packages/preferences/    # Preference management
├── packages/stores/         # Pinia stores
├── packages/styles/         # Global styles
├── packages/types/          # Shared TypeScript types
├── packages/utils/          # Utility functions
├── playground/              # Full-featured demo app (Ant Design Vue)
└── scripts/                 # Build/clean scripts
```

## Application Bootstrap Flow

Every app follows this initialization sequence:

### 1. main.ts - Entry Point
```typescript
import { initPreferences } from '@vben/preferences';
import { unmountGlobalLoading } from '@vben/utils';
import { overridesPreferences } from './preferences';

async function initApplication() {
  const env = import.meta.env.PROD ? 'prod' : 'dev';
  const appVersion = import.meta.env.VITE_APP_VERSION;
  const namespace = `${import.meta.env.VITE_APP_NAMESPACE}-${appVersion}-${env}`;
  await initPreferences({ namespace, overrides: overridesPreferences });
  const { bootstrap } = await import('./bootstrap');
  await bootstrap(namespace);
  unmountGlobalLoading();
}
initApplication();
```

### 2. bootstrap.ts - App Setup
```typescript
async function bootstrap(namespace: string) {
  await initComponentAdapter();    // 1. Register UI component adapter
  await initSetupVbenForm();       // 2. Setup form system
  const app = createApp(App);
  registerLoadingDirective(app);   // 3. Register v-loading directive
  await setupI18n(app);            // 4. i18n
  await initStores(app, { namespace }); // 5. Pinia stores
  registerAccessDirective(app);    // 6. Permission directives (v-access)
  app.use(router);                 // 7. Router
  app.mount('#app');
}
```

### 3. preferences.ts - App Preferences
```typescript
import { defineOverridesPreferences } from '@vben/preferences';
export const overridesPreferences = defineOverridesPreferences({
  app: {
    name: import.meta.env.VITE_APP_TITLE,
    // accessMode: 'frontend' | 'backend',
    // apiSecurity: false,       // API 加密开关
    // defaultHomePath: '/dashboard',
    // enableConsole: false,     // 控制台开关
    // enableRefreshToken: true,
    // locale: 'zh-CN',
    // loginExpiredMode: 'modal' | 'page',
  },
});
```

## Component Adapter Pattern

The framework is **UI-library agnostic**. Each app defines an adapter that maps abstract component types to concrete UI library components.

### adapter/component/index.ts
```typescript
import { globalShareState } from '@vben/common-ui';

export type ComponentType =
  | 'Input' | 'Select' | 'DatePicker' | 'Switch' | 'Upload'
  | 'ApiSelect' | 'ApiTreeSelect' | 'ApiCascader'
  | 'Checkbox' | 'CheckboxGroup' | 'Radio' | 'RadioGroup'
  | 'InputNumber' | 'InputPassword' | 'Textarea' | 'Mentions'
  | 'TimePicker' | 'RangePicker' | 'TreeSelect' | 'Cascader'
  | 'Rate' | 'IconPicker' | 'AutoComplete' | 'Divider'
  | 'DefaultButton' | 'PrimaryButton' | 'Space'
  | BaseFormComponentType;

async function initComponentAdapter() {
  const components: Partial<Record<ComponentType, Component>> = {
    Input: withDefaultPlaceholder(Input, 'input'),
    Select: withDefaultPlaceholder(Select, 'select'),
    // ... map all components
  };
  globalShareState.setComponents(components);
}
```

### adapter/form.ts
```typescript
import { setupVbenForm, useVbenForm as useForm, z } from '@vben/common-ui';
async function initSetupVbenForm() {
  setupVbenForm<ComponentType>({
    config: {
      baseModelPropName: 'value',  // Ant Design Vue uses v-model:value
      modelPropNameMap: {
        Checkbox: 'checked', Radio: 'checked',
        Switch: 'checked', Upload: 'fileList',
      },
    },
    defineRules: {
      required: (value, _params, ctx) => {
        if (value === undefined || value === null || value.length === 0)
          return $t('ui.formRules.required', [ctx.label]);
        return true;
      },
      selectRequired: (value, _params, ctx) => {
        if (value === undefined || value === null)
          return $t('ui.formRules.selectRequired', [ctx.label]);
        return true;
      },
    },
  });
}
const useVbenForm = useForm<ComponentType>;
export { useVbenForm, z };
export type VbenFormSchema = FormSchema<ComponentType>;
```

### adapter/vxe-table.ts
```typescript
import { setupVbenVxeTable, useVbenVxeGrid as useGrid } from '@vben/plugins/vxe-table';
setupVbenVxeTable({
  configVxeTable: (vxeUI) => {
    vxeUI.setConfig({ grid: { align: 'center', border: false, size: 'small', ... } });
    // Register custom cell renderers: CellImage, CellLink, CellTag, CellSwitch, CellOperation
  },
  useVbenForm,
});
export const useVbenVxeGrid = <T>(...rest) => useGrid<T, ComponentType>(...rest);
```

## Package Architecture

### Core Stores (@vben/stores)
- `useAccessStore` - Token, permissions, access codes, login state
- `useUserStore` - User info (roles, avatar, name)
- `useTabbarStore` - Tab management
- `resetAllStores()` - Reset all stores on logout

### App-Level Store
- `useAuthStore` - Login/logout logic, fetch user info (defined in each app's `src/store/auth.ts`)

### Key Packages
| Package | Purpose |
|---------|---------|
| `@vben/access` | Access control, `v-access` directive, route generation |
| `@vben/common-ui` | Form, Modal, Drawer, VxeTable, Alert, EllipsisText, etc. |
| `@vben/hooks` | useRefresh, useWatermark, useAppConfig |
| `@vben/layouts` | BasicLayout, AuthLayout, LockScreen, Notification |
| `@vben/request` | RequestClient (Axios wrapper with interceptors) |
| `@vben/preferences` | Theme, locale, layout preferences |
| `@vben/locales` | i18n setup and locale files |
| `@vben/utils` | Utility functions |
| `@vben/types` | Shared TypeScript types |

## Environment Configuration

### .env
```
VITE_APP_TITLE=Vben Admin
VITE_APP_NAMESPACE=vben-web-antd
```

### .env.development
```
VITE_PORT=5555
VITE_GLOB_API_URL=/api
VITE_NITRO_MOCK=true
VITE_DEVTOOLS=true
```

### Path Alias
`#/*` maps to `./src/*` via Node.js subpath imports (configured in package.json `imports` field).

### NPM Scripts
| Command | Description |
|---------|-------------|
| `pnpm dev:antd` | Dev server for Ant Design Vue app |
| `pnpm dev:ele` | Dev server for Element Plus app |
| `pnpm dev:play` | Dev server for playground |
| `pnpm dev:docs` | Dev server for documentation |
| `pnpm build:antd` | Build Ant Design Vue app |
| `pnpm lint` | Lint code |
| `pnpm test:unit` | Run unit tests |
