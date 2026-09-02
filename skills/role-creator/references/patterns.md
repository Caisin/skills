# Role Creator Patterns

## 权限矩阵

实施前先填写最小矩阵：

| 角色 | 页面权限 | 按钮权限 | 弹层依赖 API | 直接 API | 必须拒绝 |
|---|---|---|---|---|---|
| `<domain>_admin` | 全部业务页面 | 全部管理动作 | 详情、选项、共享选择器 | 仅无权限节点承载的例外 | 其它业务域 |
| `<domain>_readonly` | 全部只读页面 | 下载/预览等只读动作 | 详情、选项 | 通常为空 | create/update/delete/action |

同一 API 可以绑定多个权限节点。例如设备页的卡槽弹窗读取 SIM 短信时，`msg.sim.messages` 可以同时绑定 SIM 页面和设备页面。

## 权限种子

```rust
PermissionSeedSpec::menu(
    "Domain",
    "DomainItems",
    "对象列表",
    1,
    "/domain/items",
    "/domain/items/list",
    "lucide:list",
    &["domain.item.page", "domain.item.detail", "domain.item.options"],
),
PermissionSeedSpec::button(
    "DomainItems",
    "DomainItemsManage",
    "管理对象",
    10,
    "domain_items:manage",
    &["domain.item.create", "domain.item.update", "domain.item.delete"],
),
```

不要把同时包含查询和写入的 `domain.item.*` 绑定到菜单。

## 内置角色迁移

迁移顺序：

```text
同步 ApiCatalog
-> 创建/更新权限节点
-> 必要时删除旧 au_api_perm
-> 按新 specs 重建绑定
-> 校验 home permission 属于角色权限
-> 插入角色
-> 插入 au_role_perm
-> 仅在确有例外时插入 au_role_api
```

父目录不必直接写入 `au_role_perm`；`PermissionSvc::current_in` 会为菜单展示补齐祖先。

## 角色复制

推荐接口：

```text
POST /auth/role/{source_role_id}/copy
ApiMeta code: auth.role.copy
body: { role_id, role_name }
```

复制在 Auth 单库事务中读取源角色、`au_role_perm`、`au_role_api`，插入目标角色并写入两组授权。复制首页、启用状态、排序和备注；目标 `role_id`、`role_name` 使用请求值，`created_at` 使用当前时间。目标已存在返回稳定错误，任何一步失败不保留目标角色。

## 前端闭环

- 列表行“复制”按钮使用独立 auth code。
- 弹窗默认生成可编辑的新角色编码和“原名称副本”。
- 提交成功关闭弹窗、刷新列表；失败保留输入。
- 复制完成后允许从列表进入现有角色编辑 Drawer 调整权限。
- 只读角色看不到管理按钮；服务端授权仍是最终边界。

## 常见错误

```text
❌ 用业务 API 通配符同时承载页面读取和管理写入
❌ 只记录弹窗提交 API，遗漏打开弹窗所需的详情、选项和共享选择器 API
❌ 修改权限 patterns 后不删除已有数据库中的旧 au_api_perm
❌ 把公共/auth_only API重复授予某个角色，制造不存在的角色依赖
❌ 复制角色跨多次独立写入，失败后留下只有部分权限的新角色
```

## 正确做法

```text
✅ 页面、按钮、弹层依赖和拒绝集合在同一权限矩阵中审计
✅ 管理角色和只读角色都用有效授权正反例验证
✅ 角色复制在 Auth 单库事务中完成并保持源角色不变
```

## 验证清单

```text
[ ] 管理角色可进入全部目标页面并调用全部管理动作
[ ] 只读角色可调用列表、详情、筛选、弹层只读依赖
[ ] 只读角色拒绝 create/update/delete/action 代表 API
[ ] 公共/auth_only API 未重复扩权
[ ] 角色首页属于直接权限集合
[ ] 父目录仅用于菜单展示，没有直接宽泛授权
[ ] 复制角色 permission_ids/api_ids 与源角色集合相等
[ ] 复制失败不产生半成品
[ ] 前端按钮 auth code 与权限种子一致
[ ] 首次安装和前向迁移都通过
```
