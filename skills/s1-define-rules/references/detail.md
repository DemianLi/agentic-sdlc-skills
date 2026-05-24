# s1-define-rules: Detailed Reference

## Role Identity: Foundation Engineer
- **Mindset**: You are a pedantic, forward-thinking systems governor. You care about long-term maintainability, zero-tolerance for code smells, and strict architectural boundaries.
- **Upstream Dependency**: None. You are the beginning of the DAG.
- **Downstream Target**: Your output (`RULES.md`) will be heavily consumed by the Code Auditor in Stage 5.

## Semantic Boundary

| Skill | 用途 | 差別 |
|-------|------|------|
| `s1-define-rules` | 定義編碼規範、lint 規則、禁止模式、架構準則 | 輸出 RULES.md；關注「能寫什麼、不能寫什麼」 |
| `s1-config-context` | 初始化 CONTEXT.md 與 AI 角色邊界 | 管理 project 元資料與 AI 指引；不寫規範文件 |
| `s1-lock-tech-stack` | 鎖定框架版本與依賴 | 鎖定「用什麼工具」；不定義工具的使用規範 |
| `s1-git-guardrails` | 安裝 PreToolUse hook 攔截破壞性 git 命令 | 防止危險 git 操作；不涉及編碼規範 |

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s1-define-rules/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Toolchain Mapping Reference

| Rule Type | Enforcement Tool |
|-----------|-----------------|
| Formatting | Add to `pyproject.toml [tool.ruff]` / `.prettierrc` |
| Forbidden pattern | Add to SAST config — `/s5-sast-lint` will consume this |
| File length limit | Linter rule (e.g., `max-module-lines` in Ruff) |
| Architecture boundary | Import linter (e.g., `import-linter`, `deptrac`) |
