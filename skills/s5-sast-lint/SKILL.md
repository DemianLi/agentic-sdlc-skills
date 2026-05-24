---
name: s5-sast-lint
description: >
  Use when running linting, formatting, and SAST checks — auto-fixes safe issues,
  blocks critical findings. Outputs scan report. NOT for human code review.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s5-sast-lint`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT hand off to `/s5-audit-rules` if there are CRITICAL linting errors, SAST findings (HIGH or CRITICAL severity), or formatting issues remaining.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s5-audit-rules.
Do NOT skip /s5-audit-rules’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Code Auditor** — the unforgiving machine. You trust no one and verify everything against the rules. Code that doesn't pass static analysis never reaches human review.

## Workflow

### Step 1 — Load Rules
Read `RULES.md` from Stage 1. Identify:
- The linter(s) and their config files (e.g., `.eslintrc`, `ruff.toml`, `.golangci.yml`)
- The formatter (e.g., Prettier, Black, `gofmt`)
- Any SAST tool defined (e.g., `semgrep`, `gosec`, `bandit`)
- The zero-tolerance forbidden patterns (e.g., "no `any` in TypeScript")

### Step 2 — Run Formatter

Use command from RULES.md (Prettier / Black / gofmt). **Formatting is mandatory before linting.**

### Step 3 — Run Linter

Use command from RULES.md with strict flags (e.g., `--max-warnings 0`).

### Step 4 — Classify Results

| Severity | Action |
|---|---|
| 🔴 CRITICAL | Blocks handoff — must fix |
| 🟡 WARNING | Fix if auto-fixable |
| 🟢 INFO | Auto-fix only |

### Step 5 — Auto-Fix Safe Issues

Run auto-fix for non-behavioral changes only. **Never auto-fix runtime changes.**

### Step 6 — Run SAST

If configured in RULES.md, run **semgrep** (or gosec/bandit). Any HIGH/CRITICAL finding blocks handoff.

### Step 7 — Report

Output status (PASS/BLOCKED) with:
- CRITICAL issues (must fix)
- WARNING issues (non-blocking)
- Auto-fixed count
- Zero violations checklist

---

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| 掃出的只是警告，可以忽略或留到下次修 | WARNING 不阻斷，但 CRITICAL 會。勿混淆。你的職責是分類準確，而不是判斷「哪些警告能容忍」。 |
| CI 會自動捕獲這些問題，不用我手動掃 | Stage 5 就是「代碼進人工審查之前的最後一道機械防線」。如果格式/linter/SAST 在這裡沒有運行，問題會漏掉。 |
| 我們只需要 linting，不需要 formatter | 格式化是先決條件。未格式化的代碼導致 linter 結果不可靠（混淆式變化 vs 實質變化）。必須先格式，再 lint。 |

---

## Completion Report

Report status using exactly one of:
- **DONE** — zero CRITICAL issues; formatter ran; SAST clean. Proceeding to `/s5-audit-rules`.
- **DONE_WITH_CONCERNS** — CRITICAL issues were fixed; note any WARNING items that were not auto-fixable and require human decision.
- **BLOCKED** — CRITICAL issue cannot be auto-fixed and requires architectural decision; state the finding.
- **NEEDS_CONTEXT** — linter config not found in RULES.md; state what is missing.

</what-to-do>

<supporting-info>

**Reads**: source files, RULES.md  
**Writes**: `docs/audit/YYYY-MM-DD-<branch>-sast.md`

→ Full reference: `references/detail.md`

</supporting-info>
