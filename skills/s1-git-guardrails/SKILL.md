---
name: s1-git-guardrails
description: >
  Use when installing safety hooks to block destructive git commands. Outputs
  verification test confirming guardrails active. NOT for settings changes.
---

<HARD-GATE>
Do NOT declare this skill complete until the block script has been installed, the PreToolUse hook entry has been added to `.claude/settings.json`, and you have run the verification test showing the actual blocked output.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, report DONE with guardrails active.
This is a standalone setup utility — do NOT automatically route to a next skill.
Do NOT skip the verification output — the blocked terminal output must be visible before proceeding.
</HARD-GATE>

<what-to-do>

**Foundation Engineer (safety-rail mode)**: Ensure no destructive git command runs without explicit user awareness.

### 絕對不要觸發的情境

**Do NOT use this skill when:**

| 情境 | 改用 |
|------|------|
| 你只想修改 `settings.json` 中的模型或工具設定（非 hook） | `/update-config` — 通用設定修改，不涉及安全攔截 |
| 你想初始化整個 Stage 1 環境（CONTEXT.md、RULES.md） | `/s1-config-context` — 完整 Stage 1 初始化流程 |

---

## Blocked Commands

These patterns are intercepted before execution:

| Pattern | Risk |
|---------|------|
| `git push` (all variants) | Overwrites remote history, triggers CI/CD, notifies other developers |
| `git reset --hard` | Destroys all uncommitted local changes — unrecoverable |
| `git clean -f` / `-fd` | Deletes untracked files/directories — unrecoverable |
| `git branch -D` | Force-deletes branch, potentially losing commits not merged elsewhere |
| `git checkout .` / `git restore .` | Discards all working-tree changes — unrecoverable |

## Workflow

### Step 1 — Choose Scope
Ask: project-only (`.claude/settings.json`) or global (`~/.claude/settings.json`)? Re-prompt if invalid; default to project after 2 failed attempts.

### Step 2 — Install Script
Copy bundled script to `.claude/hooks/` (project) or `~/.claude/hooks/` (global), `chmod +x`. If mkdir/cp fails → BLOCKED with error.

### Step 3 — Add PreToolUse Hook
Merge into target `settings.json` under `hooks.PreToolUse[].matcher = "Bash"` entry pointing to installed script absolute path. If settings.json invalid JSON → BLOCKED.

### Step 4 — Verify
Run test: `echo '{"tool":"Bash","command":"git reset --hard"}' | <path>/block-dangerous-git.sh`. Expect exit code 2 (blocked). Exit code ≠ 2 → BLOCKED.

### Step 5 — Customize (optional)
Offer: add/remove blocked patterns? Edit `BLOCKED_PATTERNS` in script accordingly.

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| Hook 安裝了但沒執行驗證測試，可以宣告完成 | 沒有驗證輸出，你不知道 hook 是否真的生效。必須執行測試指令，看到 exit code 2，才能證明護欄有效 |
| 使用者沒有自訂封鎖模式的興趣，我可以跳過第 5 步 | 第 5 步是選擇性的，但必須詢問。使用者可能想添加或移除特定模式。沈默≠同意使用預設值 |
| settings.json 解析失敗，我可以告訴使用者「之後再修」| 不行。如果 hook 設定無效，護欄根本不會啟動。必須在此時修復，不能事後補救 |

## Completion Report

Report status using exactly one of:
- **DONE** — script installed, hook wired, verification test passed. Guardrails active.
- **DONE_WITH_CONCERNS** — active, but list any patterns the user chose to skip.
- **BLOCKED** — state the exact error (permissions, settings.json parse error, etc.).
- **NEEDS_CONTEXT** — state what is missing (e.g., skill-path not resolvable).

</what-to-do>

<supporting-info>

Outputs: script installed at `.claude/hooks/block-dangerous-git.sh` (or `~/.claude/hooks/`) + PreToolUse hook wired to `settings.json` + verification test showing exit code 2.

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: RULES.md
- **Writes**: `.claude/hooks/block-dangerous-git.sh` (or `~/.claude/hooks/`), `.claude/settings.json`

</supporting-info>
