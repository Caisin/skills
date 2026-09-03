---
name: kx-skill-creator
description: |
  Use when 创建、维护、精简或批量校验 `.agents/skills/*` 的 SKILL、references 与 evals。
  触发词：创建 skill、维护 skill、精简 skill、SKILL.md、evals.json、skill_tool
---

# kx-skill-creator

负责 repo-local skill 资产；通用提示词设计仍使用全局 `skill-creator`。

## Reference Selection

结构、crate 视角和命令见 `references/patterns.md`。

## 核心规则

1. 主 `SKILL.md` 只保留触发边界、不可破坏规则、reference 导航和验证；模板与明细放 `references/`。
2. 避免重复维护 AGENTS、长期记忆和其它 skill 已有规则；用 handoff 或相对路径引用事实源。
3. crate 型 skill 优先说明 crate 名、Cargo 引入和公共入口，再说明内部目录。
4. 不写个人绝对路径、运行态记忆或只能在当前机器成立的事实。
5. 修改 skill 时同步 evals 和相关 references；所有 skill 必须通过长度与结构校验。

## 命令

```bash
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py init <name> --kind generic --when "触发场景"
python3 .agents/skills/kx-skill-creator/scripts/skill_tool.py validate
```
