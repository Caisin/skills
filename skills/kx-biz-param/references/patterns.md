# KX Biz Param Patterns

用于 `kx-biz-param` 的模块级 reference，聚焦 `kx-biz-param` 作为“参数业务统一封装包”时，如何被业务项目复用，以及其内部已有的业务分层、缓存失效和事务边界。

## 适用场景

- 在 kx-rs 业务项目里复用参数业务统一能力
- 给参数模块补接口
- 给字典模块补保存 / 删除 / 批量替换 / 排序逻辑
- 给国际化模块补 locale 或 key/lang 维度接口
- 需要确认某段逻辑该放 ctl、svc 还是 cache

## 先记住这几条

1. `SeaOrms::param()` 是默认数据源。
2. 对外优先复用 `ParamRouter::apis()` 与 `ParamInstall::migrate()`，先减少业务侧重复代码。
3. 纯读查询可以留在 ctl；写入、缓存失效、事务控制优先放 svc 或 cache。
4. `param` 与 `dic` 的写路径都带缓存语义，不能只改库不清缓存。
5. `kx-biz-param` 核心表更常见的是 `state` 启用态，不要机械套 `is_del_eq(false)`。
6. `i18n` 与 `key_i18n` 是两套存储模型：前者是 locale->JSON，后者是 key+lang->value。

---

## 业务项目接入优先顺序

### 0. 其他项目依赖写法

```toml
[dependencies]
kx-biz-param = { version = "0.1", registry = "hekx" }
```

> 注意：字段名应为 `registry`。

### 1. 统一路由接入

```rust
use kx_biz_param::router::ParamRouter;

let app = Router::new().nest("/param", ParamRouter::apis());
```

### 2. 统一迁移接入

```rust
use kx_biz_param::install::ParamInstall;

ParamInstall::migrate().await?;
```

### 3. 只有现有能力不够时再扩展 crate 内部

```text
- 现有路由和服务够用：直接接入
- 现有语义差一点：优先在 kx-biz-param 内补通用能力
- 明显只是某个业务项目私有需求：再决定是否放业务侧
```

---

## 下游项目完整接入模板

### Cargo.toml

```toml
[dependencies]
kx-biz-param = { version = "0.1", registry = "hekx" }
```

### 安装入口

```rust
use anyhow::Result;
use kx_biz_param::install::ParamInstall;

pub async fn install_bizs() -> Result<()> {
    ParamInstall::migrate().await?;
    Ok(())
}
```

### 路由入口

```rust
use kx_axum::axum::Router;
use kx_biz_param::router::ParamRouter;

pub fn apis() -> Router {
    Router::new().nest("/param", ParamRouter::apis())
}
```

### 接入顺序

```text
1. 先引入依赖
2. 再跑 ParamInstall::migrate()
3. 再挂 ParamRouter::apis()
4. 最后按需复用 param / dic / i18n / key_i18n
```

---

## 子域到文件的落点表

| 子域 | 入口 ctl | 主要 svc/cache | 主要实体 | 何时优先用它 |
| --- | --- | --- | --- | --- |
| param | `src/ctl/param.rs` | `src/svc/param_svc.rs` + `src/cache/param_cache.rs` | `KxParam` | 管理系统参数、JSON 参数值、`sys_setting` |
| dic | `src/ctl/dic.rs` | `src/svc/dic_svc.rs` + `src/cache/dic_cache.rs` | `DicCode` / `DicData` | 管理字典编码、字典项、排序、批量替换 |
| i18n | `src/ctl/i18n.rs` | `src/svc/i18n_svc.rs` | `KxI18n` | 某语言整棵 JSON 国际化树 |
| key_i18n | `src/ctl/key_i18n.rs` | `src/svc/key_i18n_svc.rs` | `KxKeyI18n` | 按 key/lang 维护单条翻译 |

---

## 参数模块常用模板

### 读取参数值

```rust
pub async fn get(Path(code): Path<String>) -> Result<R<Value>, AxumErr> {
    let ret = ParamSvc::get_param_value(&code).await?;
    Ok(ret.into())
}
```

### 写入参数值后刷新缓存

```rust
pub async fn save(mut req: KxParamModify) -> Result<()> {
    let db = &mut SeaOrms::param().await?;
    let code = req.get_param_code()?;
    match KxParam::get(db, code.clone()).await {
        Ok(_) => req.update(db).await?,
        Err(_) => {
            req.set_default();
            req.insert(db).await?;
        }
    }
    KxParam::refresh_cache(&code).await?;
    Ok(())
}
```

### 手工刷新缓存

```rust
pub async fn refresh_cache(code: &str) -> Result<()> {
    KxParam::refresh_cache(code).await?;
    Ok(())
}
```

关键点：

```text
- 参数值本体放在 kx_param.param_value（JSON）。
- save / del 后都要 refresh_cache。
- 简单读接口可以保持 ctl -> svc 的薄转发。
```

---

## 字典模块常用模板

### 读取字典缓存

```rust
pub async fn get_dic(Path(code): Path<String>) -> Result<R<Vec<DicData>>, AxumErr> {
    let ret = DicCache::get_by_code(&code).await?;
    Ok(ret.into())
}
```

### 保存单条字典数据并清缓存

```rust
pub async fn save_data(mut data: DicDataModify) -> Result<()> {
    let c = &mut SeaOrms::param().await?;
    if data.id.is_none() {
        let sort_no = match DicData::sel()
            .dic_code_eq(data.get_dic_code()?)
            .desc_sort_no()
            .one(c)
            .await
        {
            Ok(v) => v.sort_no,
            Err(_) => 0,
        };
        data.set_sort_no(sort_no + 1)
            .set_created_at(times::sys_time_ts())
            .set_default()
            .unset_id();
    }
    let data = data.upsert(c).await?;
    Rds::del(&format!("dic_data:{}", data.dic_code)).await?;
    Ok(())
}
```

### 批量替换字典数据

```text
- 先收集保留的 id
- 删掉当前 dic_code 下不在保留集里的旧数据
- 依次重写 sort_no
- 新数据补 created_at / set_default / unset_id
- 最后统一删缓存 key
```

### 拖拽排序

```text
- 先读原始 sort_no
- 根据上移 / 下移批量调整区间内 sort_no
- 再更新当前项 sort_no
- 这个过程必须放事务里
```

关键点：

```text
- 字典展示顺序以 sort_no 为准。
- 批量替换、排序、级联删除优先使用事务。
- `DicSvc::del_dic` 删除字典编码时，要同时删除关联 DicData。
```

---

## 国际化模块常用模板

### locale -> JSON 文案树

```rust
pub async fn locale(Path(locale): Path<String>) -> Result<R<Value>, AxumErr> {
    let ret = I18nSvc::get_locale(locale).await?;
    Ok(ret.into())
}
```

```rust
pub async fn save(req: I18nSaveData) -> Result<()> {
    let db = &mut SeaOrms::param().await?;
    let data = req.get_data();

    match KxI18n::get(db, &req.locale).await {
        Ok(mut v) => {
            v.data.merge(data);
            v.upsert(db).await?;
        }
        Err(_) => {
            KxI18n::m()
                .set_locale(&req.locale)
                .set_created_at(times::sys_time_ts())
                .set_name(&req.locale)
                .set_data(data)
                .set_default()
                .to_owned()
                .insert(db)
                .await?;
        }
    }
    Ok(())
}
```

### key + lang -> 扁平翻译

```text
- 分页与保存入口在 key_i18n ctl
- 聚合输出完整多语言 JSON 时，调用 KeyI18nSvc::get_i18n_data()
- 这个子域更适合“翻译管理后台”场景
```

关键点：

```text
- `i18n` 关注 locale 维度的整包文案。
- `key_i18n` 关注单条翻译键值。
- 除非需求明确要求同步，不要强行把两套表模型绑成一个写路径。
```

---

## 常见错误

```text
❌ 明明已经有统一封装包，却在业务项目里重复写参数 / 字典 / 国际化路由
❌ 给 kx-biz-param 回答时只讲通用 CRUD，不讲缓存失效
❌ 看到 page/list 就默认补软删过滤，但这里很多表只有 state
❌ 把所有查询都强行塞进 svc，违背模块现有风格
❌ 需要级联删除或排序调整时不用事务
❌ 把 i18n 和 key_i18n 当成一回事
```

## 正确做法

```text
✅ 先回答“能否直接复用这个 crate 简化业务代码”，再回答“内部要改哪里”
✅ 先判断子域，再给具体文件落点
✅ 每次写操作都检查是否伴随缓存清理
✅ 涉及排序 / 批量替换 / 级联删除时，先确认事务边界
✅ 回答时沿用模块现有风格，而不是生搬硬套仓库级抽象
```
