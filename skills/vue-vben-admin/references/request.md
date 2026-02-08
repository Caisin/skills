# HTTP Request & API Patterns

## Table of Contents
- [Request Client Setup](#request-client-setup)
- [API Definition Patterns](#api-definition-patterns)
- [Auth Store Pattern](#auth-store-pattern)
- [Mock Backend](#mock-backend)

## Request Client Setup

The request layer is configured in `src/api/request.ts`:

```typescript
import {
  authenticateResponseInterceptor,
  defaultResponseInterceptor,
  errorMessageResponseInterceptor,
  RequestClient,
} from '@vben/request';

function createRequestClient(baseURL: string) {
  const client = new RequestClient({ baseURL });

  // 1. Request interceptor: add auth token and locale
  client.addRequestInterceptor({
    fulfilled: async (config) => {
      const accessStore = useAccessStore();
      config.headers.Authorization = `Bearer ${accessStore.accessToken}`;
      config.headers['Accept-Language'] = preferences.app.locale;
      return config;
    },
  });

  // 2. Response interceptor: extract data field
  client.addResponseInterceptor(
    defaultResponseInterceptor({
      codeField: 'code',
      dataField: 'data',
      successCode: 0,
    }),
  );

  // 3. Token refresh interceptor
  client.addResponseInterceptor(
    authenticateResponseInterceptor({
      client,
      doReAuthenticate,   // Logout or show login modal
      doRefreshToken,     // Refresh token API call
      enableRefreshToken: preferences.app.enableRefreshToken,
      formatToken: (token) => token ? `Bearer ${token}` : null,
    }),
  );

  // 4. Error message interceptor
  client.addResponseInterceptor(
    errorMessageResponseInterceptor((msg, error) => {
      const errorMessage = error?.response?.data?.error ?? error?.response?.data?.message ?? '';
      message.error(errorMessage || msg);
    }),
  );

  return client;
}

export const requestClient = createRequestClient(apiURL, { responseReturn: 'data' });
```

### RequestClient Utility Methods
```typescript
// Get the base URL
const baseUrl = requestClient.getBaseUrl();

// Get full URL (baseURL + path)
const fullUrl = requestClient.getFullUrl('/api/user/info');
// e.g., "http://localhost:5555/api/user/info"
```

## API Definition Patterns

### Basic CRUD API
```typescript
// src/api/system/role.ts
import { requestClient } from '#/api/request';

export namespace RoleApi {
  export interface RoleRecord {
    id: number;
    name: string;
    value: string;
    status: number;
    remark?: string;
  }
}

// List
export async function getRoleListApi(params?: any) {
  return requestClient.get('/system/role/list', { params });
}

// Detail
export async function getRoleDetailApi(id: number) {
  return requestClient.get(`/system/role/${id}`);
}

// Create
export async function createRoleApi(data: RoleApi.RoleRecord) {
  return requestClient.post('/system/role', data);
}

// Update
export async function updateRoleApi(data: RoleApi.RoleRecord) {
  return requestClient.put('/system/role', data);
}

// Delete
export async function deleteRoleApi(id: number) {
  return requestClient.delete(`/system/role/${id}`);
}
```

### Auth API
```typescript
// src/api/core/auth.ts
import { baseRequestClient, requestClient } from '#/api/request';

export namespace AuthApi {
  export interface LoginParams { password: string; username: string; }
  export interface LoginResult { accessToken: string; }
  export interface RefreshTokenResult { data: string; status: number; }
}

export async function loginApi(data: AuthApi.LoginParams) {
  return requestClient.post<AuthApi.LoginResult>('/auth/login', data);
}

export async function refreshTokenApi() {
  return baseRequestClient.post<AuthApi.RefreshTokenResult>('/auth/refresh', {
    withCredentials: true,
  });
}

export async function logoutApi() {
  return requestClient.post('/auth/logout');
}

export async function getAccessCodesApi() {
  return requestClient.get<string[]>('/auth/codes');
}
```

### Table List API with Pagination
```typescript
import type { PageFetchParams } from '#/api/request';

export async function getTableListApi(params?: PageFetchParams) {
  return requestClient.get('/table/list', { params });
}
// Response format: { items: T[], total: number }
```

### File Upload API
The upload method accepts `Blob | File | string` as the file parameter:
```typescript
export function upload_file(params: Record<string, any>) {
  const formData = new FormData();
  formData.append('file', params.file);
  return requestClient.upload('/upload', formData, {
    onUploadProgress: params.onProgress,
  }).then((res) => {
    params.onSuccess(res);
  }).catch((err) => {
    params.onError(err);
  });
}
```

## Auth Store Pattern

The auth store (`src/store/auth.ts`) handles login/logout:

```typescript
import { defineStore } from 'pinia';
import { resetAllStores, useAccessStore, useUserStore } from '@vben/stores';

export const useAuthStore = defineStore('auth', () => {
  const loginLoading = ref(false);

  async function authLogin(params: Recordable<any>, onSuccess?: () => void) {
    loginLoading.value = true;
    try {
      const { accessToken } = await loginApi(params);
      if (accessToken) {
        accessStore.setAccessToken(accessToken);
        const [userInfo, accessCodes] = await Promise.all([
          fetchUserInfo(),
          getAccessCodesApi(),
        ]);
        userStore.setUserInfo(userInfo);
        accessStore.setAccessCodes(accessCodes);
        onSuccess?.() ?? await router.push(userInfo.homePath || preferences.app.defaultHomePath);
      }
    } finally {
      loginLoading.value = false;
    }
  }

  async function logout(redirect = true) {
    try { await logoutApi(); } catch {}
    resetAllStores();
    await router.replace({
      path: LOGIN_PATH,
      query: redirect ? { redirect: encodeURIComponent(router.currentRoute.value.fullPath) } : {},
    });
  }

  async function fetchUserInfo() {
    const userInfo = await getUserInfoApi();
    userStore.setUserInfo(userInfo);
    return userInfo;
  }

  return { authLogin, fetchUserInfo, loginLoading, logout };
});
```

## Mock Backend

The mock backend is in `apps/backend-mock/` using Nitro. API routes are in `apps/backend-mock/api/`.

### Mock API Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/login` | Login, returns accessToken + sets refreshToken cookie |
| `POST /api/auth/refresh` | Refresh token |
| `POST /api/auth/logout` | Logout |
| `GET /api/auth/codes` | Get access codes |
| `GET /api/user/info` | Get user info |
| `GET /api/menu/all` | Get all menus |
| `GET /api/table/list` | Get table data (paginated) |
| `POST /api/upload` | File upload |
| `GET /api/system/dept/list` | Department list |
| `GET /api/system/menu/list` | Menu management list |
| `GET /api/system/role/list` | Role management list |

### Running Mock Server
The mock server starts automatically with `VITE_NITRO_MOCK=true` in `.env.development`.
