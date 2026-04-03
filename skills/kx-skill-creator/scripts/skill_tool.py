#!/usr/bin/env python3
"""Skill scaffolding and validation helpers for repo-local skills."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[4]
SKILLS_DIR = ROOT / ".agents" / "skills"

PRESETS = {
    "generic": {
        "create_reference": True,
        "reference_name": "patterns.md",
        "skill_template": """---
name: {name}
description: |
  Use when {when}

  触发场景：
  - 场景 1
  - 场景 2
  - 场景 3

  触发词：关键词 1、关键词 2、关键词 3
---

# {title}

一句话说明这个 skill 的职责边界。

## 适用边界

### 适用

- 适用场景 1
- 适用场景 2
- 适用场景 3

### 不适用

- 不适用场景 1
- 不适用场景 2

## Reference Selection

按任务类型优先读取：

- 场景 A
  - 读 `references/patterns.md`

## 核心规则

1. 规则 1
2. 规则 2
3. 规则 3

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 错误 1
❌ 错误 2
```

### 正确做法

```text
✅ 正确做法 1
✅ 正确做法 2
```

## 输出模板

```text
问题归类
改动落点
关键约定
验证方式
下一步
```

## 完整示例

**Input**

```text
这里放一条真实用户说法
```

**Output direction**

```text
- 这里写期望的回答方向
```
""",
        "reference_template": """# {title} Patterns

用于 `{name}` 的补充 reference。

## 适用场景

- 场景 1
- 场景 2

## 推荐模板

```rust
// 在这里放最小可复用模板
```

## 常见错误

```text
❌ 错误 1
❌ 错误 2
```

## 正确做法

```text
✅ 正确做法 1
✅ 正确做法 2
```
""",
    },
    "entry": {
        "create_reference": False,
        "reference_name": None,
        "skill_template": """---
name: {name}
description: |
  Use when {when}

  触发场景：
  - 用户在问“该改哪里 / 放哪里 / 从哪开始”
  - 需要区分框架层与实践层
  - 需要判断该切到哪个 repo-local skill

  触发词：放哪里、改哪里、从哪开始、哪个目录、哪个模块、哪个 skill
---

# {title}

一句话说明这个入口 skill 的分流职责。

## 核心职责

1. 给出项目上下文
2. 判断层级与目录
3. 路由到更合适的 skill

## 路由规则

- 先判断是框架层、实践层，还是纯 Rust / 排障 / 规划问题
- 命中更专门 skill 时，明确 handoff
- 未命中时继续做仓库级分析

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 用户只是问“该放哪里”，却直接开始写实现代码
❌ 已命中更专门的 skill，还继续用入口 skill 含混展开
```

### 正确做法

```text
✅ 先判层，再给目录与后续 skill
✅ 入口 skill 负责分流，不负责完整实现手册
```

## 标准输出模板

```text
项目上下文
模块定位
建议 skill
下一步
```

## 完整示例

**Input**

```text
这个功能该放在哪个目录？
```

**Output direction**

```text
- 先说明当前任务属于哪一层
- 给最可能的目录与原因
- 如果已命中后续 skill，明确 handoff
```
""",
    },
    "practice": {
        "create_reference": True,
        "reference_name": "patterns.md",
        "skill_template": """---
name: {name}
description: |
  Use when {when}

  触发场景：
  - 讨论 bins/bizs/ents 的组织与 CRUD 落地
  - 在业务代码里使用 #[derive(Sea)]、qry/sel/update 等能力
  - 需要从实践层问题回溯框架源码入口

  触发词：bins、bizs、ents、CRUD、控制器、路由、Service、OpenAPI、derive(Sea)
---

# {title}

一句话说明这个实践层 skill 的职责边界。

## 适用边界

### 适用

- 实践层项目骨架
- CRUD、控制器、路由、服务落地
- openapi-scan 兼容与源码回溯

### 不适用

- 纯 Rust 编译问题
- 纯 SDK 接入问题

## Reference Selection

按任务类型优先读取：

- 项目骨架
  - 读 `references/patterns.md`
- CRUD / 分页 / 软删 / 事务
  - 读 `references/patterns.md`

## 最小落地顺序

1. 先判断是实践层落地还是实践层 + 源码回溯
2. 再给最短落地路径
3. 超出边界时 handoff

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 直接回退到大量手写 SeaORM 样板
❌ 分页不补稳定排序，软删不补默认过滤
```

### 正确做法

```text
✅ 优先用框架生成能力
✅ 先给最短落地路径，再补必须知道的边界
```

## 输出模板

```text
问题归类
推荐落点
操作步骤
关键约定
下一步
```

## 完整示例

**Input**

```text
我要在实践层加一个带软删分页的 CRUD，先怎么起手？
```

**Output direction**

```text
- 先说明这是实践层 CRUD 问题
- 给出实体 / svc / ctl / router 的最短顺序
- 强调软删过滤与稳定排序
```
""",
        "reference_template": """# {title} Patterns

用于 `{name}` 的实践层补充 reference。

## 适用场景

- 项目骨架
- CRUD / 分页 / 软删 / 事务

## 推荐模板

```rust
let mut qry = T::qry().is_del_eq(false);
if !qry.has_order() {{
    qry.desc_id();
}}
let page = qry.select().page(c, paging).await?;
```

## 常见错误

```text
❌ 回退到 Entity::find() / ActiveModel 手写整套 CRUD
❌ 忘了 is_del_eq(false) 或稳定排序
```

## 正确做法

```text
✅ 优先用 <T>::get / <T>::sel / <T>::qry / <T>::m()
✅ 事务边界集中在 svc，控制器保持薄
```
""",
    },
    "sdk": {
        "create_reference": True,
        "reference_name": "patterns.md",
        "skill_template": """---
name: {name}
description: |
  Use when {when}

  触发场景：
  - 新增或修改 sdks/<provider> crate
  - 设计第三方 API trait、请求/响应 DTO、token/cache 复用
  - 判断某项能力该落 sdks 还是 crates

  触发词：SDK、第三方接入、provider、token、cache、DTO、trait、reqwest、sdks
---

# {title}

一句话说明这个 SDK skill 的职责边界。

## 适用边界

### 适用

- 一般 `sdks/<provider>` 接口封装
- trait、DTO、宿主 SDK 组织
- `sdks/` 与 `crates/` 边界判断

### 不适用

- `sdks/aigc` 专门问题
- 纯 Rust 编译问题

## Reference Selection

按任务类型优先读取：

- 普通 provider SDK 扩展
  - 读 `references/patterns.md`
- 边界判断
  - 读 `references/patterns.md`

## 实现规则

1. 一个 trait 表达一组清晰能力
2. 异步接口统一返回 `impl Future`
3. 优先复用现有能力 trait

## 常见错误 vs 正确做法

### 常见错误

```text
❌ 在 trait 上直接引入 async_trait
❌ 每个接口都重复手写 token / header / JSON 解包样板
```

### 正确做法

```text
✅ 公共请求样板下沉到基础 trait
✅ DTO 与能力 trait 邻近组织
```

## 输出模板

```text
问题归类
推荐落点
trait 设计
公共能力复用
验证方式
下一步
```

## 完整示例

**Input**

```text
我要给某个 provider SDK 新增一个接口，怎么保持和现有风格一致？
```

**Output direction**

```text
- 先给 crate / 模块落点
- 再说明 trait、DTO、宿主 SDK 的组织方式
- 最后给最小必要验证命令
```
""",
        "reference_template": """# {title} Patterns

用于 `{name}` 的通用 SDK reference。

## 适用场景

- 一般 provider SDK 接口扩展
- `sdks/` 与 `crates/` 边界判断

## 推荐模板

```rust
pub trait FooApi: GetClient + GetAccessToken {{
    fn foo(&self) -> impl Future<Output = anyhow::Result<FooRet>> {{
        async move {{
            let token = self.access_token().await?;
            self.cli()
                .post("https://example.com/foo")
                .query(&json!({{"access_token": token}}))
                .to_ret()
                .await
        }}
    }}
}}
```

## 常见错误

```text
❌ 直接上 async_trait
❌ 重复手写公共请求样板
```

## 正确做法

```text
✅ trait 返回 impl Future
✅ 优先复用 GetClient / GetAccessToken / ToRet
```
""",
    },
    "aigc": {
        "create_reference": True,
        "reference_name": "patterns.md",
        "skill_template": """---
name: {name}
description: |
  Use when {when}

  触发场景：
  - 修改 src/sdk、src/auth、src/api/<platform>/{non_stream,stream}/
  - 调整 AigcStream(meta + raw)、SSE decode、proxy/observe、protocol + model 路由
  - 需要补 request_id / usage / attempt_no / provider_hint 等链路字段

  触发词：AigcAuth、AigcSdk、OpenAI、Gemini、Anthropic、DeepSeek、Vertex、Ollama、stream、SSE、proxy、observe
---

# {title}

一句话说明这个 `sdks/aigc` skill 的职责边界。

## 适用边界

### 适用

- `AigcAuth` / `AigcSdk` / provider host
- 平台级单 API trait / DTO
- streaming 与 proxy/observe

### 不适用

- 其它普通 `sdks/<provider>`
- 纯 Rust 编译问题

## Reference Selection

按任务类型优先读取：

- 平台 API / DTO
  - 读 `references/patterns.md`
- streaming / proxy / observe
  - 读 `references/patterns.md`

## 核心规则

1. API 目录按平台 + 单 HTTP API 拆分
2. streaming 发送层保持原始 `AigcStream`
3. proxy 第一阶段只做同协议原始透传

## 常见错误 vs 正确做法

### 常见错误

```text
❌ DTO 回退到 provider 聚合层
❌ proxy 里直接做跨协议翻译
❌ 在 observer 里提前生成 preview / summary / truncated
```

### 正确做法

```text
✅ DTO 紧邻 trait
✅ provider 差异优先收敛到 AigcSdk hook
✅ observer 默认 raw-only
```

## 输出模板

```text
问题归类
改动落点
关键约定
验证方式
下一步
```

## 完整示例

**Input**

```text
我要给 OpenAI 风格 provider 新增一个非流式 API，并保持 proxy 后续可复用，应该怎么组织？
```

**Output direction**

```text
- 先给 src/api/<platform>/non_stream/ 落点
- 说明 DTO 紧邻 trait，默认复用 get_ret/post_json_ret
- 如需 proxy 复用，再看是否补 AigcSdk hook
```
""",
        "reference_template": """# {title} Patterns

用于 `{name}` 的 AIGC SDK reference。

## 适用场景

- 平台 API / DTO
- streaming / proxy / observe

## 推荐模板

```rust
pub trait OpenAiFooApi: AigcSdkExt {{
    fn foo(
        &self,
        req: &OpenAiFooReq,
    ) -> impl std::future::Future<Output = anyhow::Result<OpenAiFooResp>> + Send {{
        self.post_json_ret("foo", req)
    }}
}}
```

## 常见错误

```text
❌ 在 proxy 第一阶段做跨协议翻译
❌ 发送层直接返回 provider 事件对象
```

## 正确做法

```text
✅ 单 HTTP API 一个 trait 文件
✅ streaming 保持 meta + raw
✅ proxy 继续只做同协议原始透传
```
""",
    },
}

EVALS_TEMPLATE = {
    "skill_name": None,
    "evals": [
        {
            "id": 1,
            "prompt": "这里放一条正向命中 prompt",
            "expected_output": "这里写期望的命中行为、输出方向或 handoff 结果",
            "files": [],
        },
        {
            "id": 2,
            "prompt": "这里放一条边界 / 误触发 prompt",
            "expected_output": "这里写边界情况下不该误触发或应 handoff 的行为",
            "files": [],
        },
    ],
}


class ValidationError(RuntimeError):
    pass


REQUIRED_SKILL_STRINGS = ["触发场景", "触发词", "## ", "# "]
REQUIRED_REFERENCE_SECTIONS = ["## ", "## 常见错误", "## 正确做法"]
REQUIRED_EVAL_KEYS = {"id", "prompt", "expected_output", "files"}
VALID_KINDS = tuple(PRESETS.keys())


def slug_to_title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-") if part)


def write_if_absent(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def render_evals_payload(name: str) -> str:
    payload = copy.deepcopy(EVALS_TEMPLATE)
    payload["skill_name"] = name
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def init_skill(name: str, when_to_use: str, kind: str) -> int:
    if not re.fullmatch(r"[a-z0-9-]+", name):
        print(f"error: invalid skill name: {name}", file=sys.stderr)
        return 2
    if kind not in PRESETS:
        print(f"error: invalid kind: {kind}", file=sys.stderr)
        return 2

    preset = PRESETS[kind]
    title = slug_to_title(name)
    skill_dir = SKILLS_DIR / name
    created: list[Path] = []

    if write_if_absent(
        skill_dir / "SKILL.md",
        preset["skill_template"].format(name=name, title=title, when=when_to_use),
    ):
        created.append(skill_dir / "SKILL.md")

    if write_if_absent(skill_dir / "evals" / "evals.json", render_evals_payload(name)):
        created.append(skill_dir / "evals" / "evals.json")

    if preset["create_reference"]:
        reference_path = skill_dir / "references" / str(preset["reference_name"])
        if write_if_absent(
            reference_path,
            preset["reference_template"].format(name=name, title=title),
        ):
            created.append(reference_path)

    if not created:
        print(f"no files created for {name}; skill directory already exists")
        return 0

    print(f"initialized skill: {name} ({kind})")
    for path in created:
        print(f"  created {path.relative_to(ROOT)}")
    return 0


def validate_skill_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError("missing frontmatter start")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValidationError("missing frontmatter end")
    frontmatter, body = parts
    if not re.search(r"^name:\s*[^\n]+", frontmatter, re.M):
        raise ValidationError("missing name")
    if not re.search(r"^description:\s*\|", frontmatter, re.M):
        raise ValidationError("description must use block scalar")
    if "Use when" not in frontmatter:
        raise ValidationError("description should start with Use when")
    for token in REQUIRED_SKILL_STRINGS:
        if token not in text:
            raise ValidationError(f"missing token: {token}")
    if "## 常见错误" not in text and "## 常见错误 vs 正确做法" not in text:
        raise ValidationError("missing common mistakes section")
    if "## 完整示例" not in text:
        raise ValidationError("missing complete example section")
    if not body.strip():
        raise ValidationError("empty body")


def validate_reference_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# "):
        raise ValidationError("reference must start with H1")
    for section in REQUIRED_REFERENCE_SECTIONS:
        if section not in text:
            raise ValidationError(f"missing section: {section}")


def validate_evals_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("skill_name"):
        raise ValidationError("missing skill_name")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        raise ValidationError("evals must be a non-empty list")
    if len(evals) < 2:
        raise ValidationError("evals should contain at least 2 cases (positive + boundary/handoff)")
    for idx, item in enumerate(evals, start=1):
        if not REQUIRED_EVAL_KEYS.issubset(item):
            missing = REQUIRED_EVAL_KEYS.difference(item)
            raise ValidationError(f"eval #{idx} missing keys: {sorted(missing)}")


def iter_skill_dirs(selected: Iterable[str] | None) -> Iterable[Path]:
    if selected:
        for name in selected:
            yield SKILLS_DIR / name
        return
    yield from sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())


def validate(selected: list[str] | None) -> int:
    errors: list[str] = []
    for skill_dir in iter_skill_dirs(selected):
        skill_name = skill_dir.name
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"{skill_name}: missing SKILL.md")
            continue
        try:
            validate_skill_file(skill_path)
            print(f"OK skill {skill_path.relative_to(ROOT)}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{skill_path.relative_to(ROOT)}: {exc}")

        for ref in sorted((skill_dir / "references").glob("*.md")):
            try:
                validate_reference_file(ref)
                print(f"OK ref   {ref.relative_to(ROOT)}")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{ref.relative_to(ROOT)}: {exc}")

        evals = skill_dir / "evals" / "evals.json"
        if evals.exists():
            try:
                validate_evals_file(evals)
                print(f"OK eval  {evals.relative_to(ROOT)}")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{evals.relative_to(ROOT)}: {exc}")

    if errors:
        print("\nvalidation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print("\nall skill artifacts validated")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scaffold and validate repo-local skills")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="initialize a new skill skeleton")
    init_parser.add_argument("name", help="skill slug, e.g. my-skill")
    init_parser.add_argument(
        "--when",
        default="这里描述这个 skill 应该在什么场景触发",
        help="value used in the YAML description's 'Use when ...' line",
    )
    init_parser.add_argument(
        "--kind",
        default="generic",
        choices=VALID_KINDS,
        help="preset kind used to scaffold the skill",
    )

    validate_parser = sub.add_parser("validate", help="validate existing skill artifacts")
    validate_parser.add_argument("skills", nargs="*", help="optional skill names to validate")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init":
        return init_skill(args.name, args.when, args.kind)
    if args.command == "validate":
        return validate(args.skills)
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
