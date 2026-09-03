#!/usr/bin/env python3
"""Scaffold and validate concise repo-local skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILLS_DIR = ROOT / ".agents" / "skills"
MAX_SKILL_LINES = 160
VALID_KINDS = ("generic", "entry", "practice", "sdk", "aigc")

KIND_RULES = {
    "generic": ["说明职责边界", "列出不可破坏规则", "给出最小验证"],
    "entry": ["只做定位和 handoff", "不重复专用 skill", "给出下一步"],
    "practice": ["优先框架生成能力", "按 entity -> svc -> ctl 分层", "先跑目标验证"],
    "sdk": ["DTO 与 API trait 邻近", "复用认证和请求样板", "隔离真实网络测试"],
    "aigc": ["单 HTTP API 一个 trait", "stream 保留 meta + raw", "proxy 默认同协议透传"],
}

SKILL_TEMPLATE = """---
name: {name}
description: |
  Use when {when}
  触发词：请替换为稳定关键词
---

# {title}

一句话说明职责，不复制其它 skill 或 AGENTS 的规则。

## Reference Selection

详细模板与长清单放在 `references/patterns.md`，只在命中场景时读取。

## 核心规则

{rules}

## 验证

写明能证明任务完成的最小命令或可观察结果。
"""

REFERENCE_TEMPLATE = """# {title} Patterns

只保存主 skill 不适合常驻上下文的模板和细节。

## 模板

```text
在这里放可直接复用的最小模板。
```
"""

EVALS_TEMPLATE = {
    "skill_name": None,
    "evals": [
        {
            "id": 1,
            "prompt": "正向命中场景",
            "expected_output": "应命中该 skill 并遵守核心边界",
            "files": [],
        },
        {
            "id": 2,
            "prompt": "相邻但不属于该 skill 的场景",
            "expected_output": "应 handoff 到更合适的 skill",
            "files": [],
        },
    ],
}


class ValidationError(RuntimeError):
    pass


def slug_to_title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-") if part)


def write_if_absent(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def init_skill(name: str, when: str, kind: str) -> int:
    if not re.fullmatch(r"[a-z0-9-]+", name):
        print(f"error: invalid skill name: {name}", file=sys.stderr)
        return 2
    if kind not in VALID_KINDS:
        print(f"error: invalid kind: {kind}", file=sys.stderr)
        return 2

    rules = "\n".join(
        f"{index}. {rule}" for index, rule in enumerate(KIND_RULES[kind], start=1)
    )
    skill_dir = SKILLS_DIR / name
    created = []
    if write_if_absent(
        skill_dir / "SKILL.md",
        SKILL_TEMPLATE.format(
            name=name,
            title=slug_to_title(name),
            when=when,
            rules=rules,
        ),
    ):
        created.append(skill_dir / "SKILL.md")

    payload = dict(EVALS_TEMPLATE)
    payload["skill_name"] = name
    if write_if_absent(
        skill_dir / "evals" / "evals.json",
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    ):
        created.append(skill_dir / "evals" / "evals.json")
    if kind != "entry" and write_if_absent(
        skill_dir / "references" / "patterns.md",
        REFERENCE_TEMPLATE.format(title=slug_to_title(name)),
    ):
        created.append(skill_dir / "references" / "patterns.md")

    if not created:
        print(f"no files created for {name}; skill directory already exists")
        return 0
    print(f"initialized skill: {name} ({kind})")
    for path in created:
        print(f"  created {path.relative_to(ROOT)}")
    return 0


def validate_skill(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        raise ValidationError(f"{len(lines)} lines exceeds {MAX_SKILL_LINES}-line budget")
    if not text.startswith("---\n") or "\n---\n" not in text:
        raise ValidationError("invalid frontmatter boundary")
    frontmatter, body = text.split("\n---\n", 1)
    if not re.search(r"^name:\s*[a-z0-9-]+\s*$", frontmatter, re.M):
        raise ValidationError("missing or invalid name")
    if not re.search(r"^description:\s*(?:\||\S)", frontmatter, re.M):
        raise ValidationError("missing description")
    if not re.search(r"^#\s+\S", body, re.M):
        raise ValidationError("missing H1")
    if not re.search(r"^##\s+\S", body, re.M):
        raise ValidationError("missing H2")
    placeholders = ["场景 1", "规则 1", "请替换为稳定关键词"]
    if any(marker in text for marker in placeholders):
        raise ValidationError("contains scaffold placeholder")


def validate_reference(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValidationError("reference is empty")
    if any(marker in text for marker in ["场景 1", "错误 1", "正确做法 1"]):
        raise ValidationError("reference contains scaffold placeholder")


def validate_evals(path: Path, skill_name: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("skill_name") != skill_name:
        raise ValidationError("skill_name does not match directory")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 2:
        raise ValidationError("requires at least positive and boundary evals")
    required = {"id", "prompt", "expected_output", "files"}
    for index, item in enumerate(evals, start=1):
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValidationError(f"eval #{index} is incomplete")


def validate(selected: list[str] | None) -> int:
    names = selected or sorted(path.name for path in SKILLS_DIR.iterdir() if path.is_dir())
    errors = []
    for name in names:
        skill_dir = SKILLS_DIR / name
        try:
            validate_skill(skill_dir / "SKILL.md")
            evals = skill_dir / "evals" / "evals.json"
            if not evals.is_file():
                raise ValidationError("missing evals/evals.json")
            validate_evals(evals, name)
            for reference in sorted((skill_dir / "references").glob("*.md")):
                validate_reference(reference)
            print(f"OK {name}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    if errors:
        print("validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"all {len(names)} skill artifacts validated")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("name")
    init.add_argument("--kind", choices=VALID_KINDS, default="generic")
    init.add_argument("--when", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("skills", nargs="*")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "init":
        return init_skill(args.name, args.when, args.kind)
    return validate(args.skills or None)


if __name__ == "__main__":
    raise SystemExit(main())
