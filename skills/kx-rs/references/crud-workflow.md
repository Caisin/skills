# CRUD Workflow

用于“日常业务 CRUD 开发”的场景。

## 适用场景

- 新增一个标准增删改查模块
- 需要同时落 `svc/ctl/router/install`
- 需要把实践层职责边界说明清楚

> 如果用户明确要的是 SeaORM 模型定义、迁移、`qry()/sel()/m()`、事务、多数据源或多表操作代码模板，请直接切到 `kx-sea-orm`，不要在本 reference 里重复展开。

## 推荐开发顺序

1. 先确认实体在哪个 `ents/<ds>/`
2. 再确定业务模块 `bizs/<biz>/`
3. 先写 `svc/`，再写 `ctl/`
4. 然后写 `router.rs`
5. 最后补 `install.rs` 和应用装配

不要一开始先写 controller，再倒推 service 和 entity。

## 落地关注点

### 1. `svc/`

- 放业务编排
- 放事务边界
- 放多表组装
- 放关联校验

### 2. `ctl/`

- 只收参
- 调用 service
- 返回统一结果

### 3. `router.rs`

- 收口 HTTP 路由
- 复用同一个 `impl XxxCtl` 下的 handler，便于集中维护

### 4. `install.rs`

- 做模块级装配
- 暴露给上层 `bins/*` 接入

## 常见错误

```text
❌ 只写 ctl，不补 svc 的业务编排与事务边界
❌ 把事务、多表组装、关联校验塞进 ctl/
❌ router、install、ctl 没分层，导致实践层结构发散
❌ 用户已经明确要 SeaORM 模板，还继续停留在本 reference 里兜圈子
```

## 正确做法

```text
✅ 先把 ents/bizs/bins 和 svc/ctl/router/install 的职责边界说清楚
✅ 控制器保持薄，业务逻辑收口到 svc/
✅ 路由与 handler 保持同一 impl 约定
✅ 需要实体/迁移/query/update/事务代码模板时，直接使用 kx-sea-orm
```

## 何时切去其他 reference

- 要新建 practice 层项目骨架
  - 看 `project-skeleton.md`
- 不确定该去哪个框架目录找源码
  - 看 `source-navigation.md`
- 明确要 SeaORM 模型 / 迁移 / CRUD / 事务模板
  - 直接切 `kx-sea-orm`
- 明确要 ctl/router/install、R/AxumErr、QsQuery、crud_api! 的接口层模板
  - 直接切 `kx-axum-web`
