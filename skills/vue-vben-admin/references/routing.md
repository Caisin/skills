# Routing, Menus & Access Control

## Table of Contents
- [Route Definition](#route-definition)
- [Route Meta Options](#route-meta-options)
- [Access Modes](#access-modes)
- [Route Guards](#route-guards)
- [Permission Directives](#permission-directives)

## Route Definition

Routes are defined in `src/router/routes/modules/*.ts`. Each file exports a `RouteRecordRaw[]`.

### Basic Route Example
```typescript
import type { RouteRecordRaw } from 'vue-router';
import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'lucide:layout-dashboard',
      order: -1,
      title: $t('page.dashboard.title'),
    },
    name: 'Dashboard',
    path: '/dashboard',
    children: [
      {
        name: 'Analytics',
        path: '/analytics',
        component: () => import('#/views/dashboard/analytics/index.vue'),
        meta: {
          affixTab: true,
          icon: 'lucide:area-chart',
          title: $t('page.dashboard.analytics'),
        },
      },
      {
        name: 'Workspace',
        path: '/workspace',
        component: () => import('#/views/dashboard/workspace/index.vue'),
        meta: {
          icon: 'carbon:workspace',
          title: $t('page.dashboard.workspace'),
        },
      },
    ],
  },
];
export default routes;
```

### Nested Route Example
```typescript
const routes: RouteRecordRaw[] = [
  {
    meta: { icon: 'ion:layers-outline', order: 1000, title: $t('examples.title') },
    name: 'Examples',
    path: '/examples',
    children: [
      {
        name: 'FormExample',
        path: '/examples/form',
        meta: { icon: 'mdi:form-select', title: $t('examples.form.title') },
        children: [
          {
            name: 'FormBasicExample',
            path: '/examples/form/basic',
            component: () => import('#/views/examples/form/basic.vue'),
            meta: { title: $t('examples.form.basic') },
          },
        ],
      },
    ],
  },
];
```

## Route Meta Options

| Property | Type | Description |
|----------|------|-------------|
| `title` | `string` | Menu/tab display title (supports i18n via `$t()`) |
| `icon` | `string` | Iconify icon name (e.g., `'lucide:area-chart'`) |
| `order` | `number` | Menu sort order (lower = higher priority) |
| `authority` | `string[]` | Required roles to access this route |
| `keepAlive` | `boolean` | Enable component keep-alive caching |
| `hideInMenu` | `boolean` | Hide from sidebar menu |
| `hideInTab` | `boolean` | Hide from tab bar |
| `hideInBreadcrumb` | `boolean` | Hide from breadcrumb |
| `affixTab` | `boolean` | Pin tab (cannot be closed) |
| `badge` | `string` | Badge text on menu item |
| `badgeType` | `'dot'\|'normal'` | Badge display type |
| `iframeSrc` | `string` | Embed external page via iframe |
| `link` | `string` | External link (opens in new tab) |
| `ignoreAccess` | `boolean` | Skip access control check |
| `menuVisibleWithForbidden` | `boolean` | Show in menu but redirect to 403 if no permission |
| `loaded` | `boolean` | (Auto-set) Whether page has been loaded before |

## Access Modes

### Frontend Access Mode
Routes are filtered on the frontend based on user roles. Define `authority` in route meta:

```typescript
{
  name: 'AdminPage',
  path: '/admin',
  component: () => import('#/views/admin/index.vue'),
  meta: {
    authority: ['admin', 'super'],  // Only admin/super roles can access
    title: 'Admin Page',
  },
}
```

### Backend Access Mode
Routes are fetched from the backend API. The `generateAccess` function in `src/router/access.ts` handles this:

```typescript
import { generateAccessible } from '@vben/access';

async function generateAccess(options: GenerateMenuAndRoutesOptions) {
  const pageMap: ComponentRecordType = import.meta.glob('../views/**/*.vue');
  const layoutMap: ComponentRecordType = { BasicLayout, IFrameView };

  return await generateAccessible(preferences.app.accessMode, {
    ...options,
    fetchMenuListAsync: async () => {
      return await getAllMenusApi();  // Fetch menus from backend
    },
    forbiddenComponent,
    layoutMap,
    pageMap,
  });
}
```

### Access Mode Configuration
Set in `preferences.ts`:
```typescript
export const overridesPreferences = defineOverridesPreferences({
  app: {
    accessMode: 'frontend', // or 'backend'
  },
});
```

## Route Guards

Route guards are configured in `src/router/guard.ts`:

```typescript
function createRouterGuard(router: Router) {
  setupCommonGuard(router);   // Progress bar, page load tracking
  setupAccessGuard(router);   // Authentication & authorization
}
```

### Access Guard Flow
1. Check if route is a core route (login, 404, etc.) → allow
2. Check `accessToken` → redirect to login if missing
3. Check if dynamic routes are generated → generate if not
4. Fetch user info and roles → generate accessible routes and menus
5. Store menus and routes in `accessStore`

## Permission Directives

### v-access Directive
Control element visibility based on access codes:

```vue
<!-- Show only if user has 'AC_100100' access code -->
<Button v-access:code="['AC_100100']">Super Admin Visible</Button>

<!-- Show only if user has 'admin' role -->
<Button v-access:role="['admin']">Admin Visible</Button>
```

### Programmatic Access Check
```typescript
import { useAccess } from '@vben/access';
const { hasAccessByCodes } = useAccess();
if (hasAccessByCodes(['AC_100100'])) {
  // User has permission
}
```

## 常见错误

```text
❌ 直接把这份参考当成最终回答，忽略用户当前具体问题
❌ 不做取舍，把整份长文照搬给用户
```

## 正确做法

```text
✅ 先提炼与当前问题最相关的片段
✅ 用最小必要内容回答，再按需引导用户查看更完整参考
```
