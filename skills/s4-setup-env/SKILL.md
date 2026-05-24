---
name: s4-setup-env
description: >
  Use when preparing environment for an atomic task. Outputs branch setup and
  verified runtime environment. NOT without TASK_DAG.md and dependency validation.
---
<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s4-setup-env`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT start any implementation until:
1. Environment check passed and workspace is verified as clean.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s4-tdd (or /s4-impl-task if tests already exist).
Do NOT skip /s4-tdd’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Implementer**. Prepare the development environment for an atomic task.

### Step 0 — Input Validation
**BLOCKED if**: TASK_DAG.md missing; task dependencies unmarked [DONE]; runtime version mismatched; workspace unclean; lock file unreadable.

### Step 1 — Select Task
Read `TASK_DAG.md` for next task with all dependencies [DONE]. Confirm: *"Next task is TASK-N: <title>. Confirm?"*

### Step 2 — Branch Setup
**Standard mode**: `git checkout -b task-N-<slug>`
**Worktree mode** (parallel): `git worktree add ../task-N-<slug> -b task-N-<slug>`

### Step 3 — Validate Environment
Check: `node --version` / `go version` / `python --version` must match lock file. Run: `npm ci` / `go mod download` (pinned, not latest).

### Step 4 — Verify Workspace
Confirm no uncommitted changes from prior tasks.

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| "我之前用過這個環境，應該可以跳過版本檢查，直接開始" | 「之前用過」的環境可能已過期或被污染；每個任務的起點必須乾淨 |
| "TASK_DAG.md 裡的下一個任務依賴複雜，但先開始設置，實現時再補" | 設置 ≠ 實現；你現在必須選定具體的 TASK-N，否則分支名無法確定 |
| "測試通過了，說明環境是對的，可以開始寫代碼" | 環境檢查只驗證運行時和依賴版本；不保證沒有前一任務遺留的孤立檔案；必須手動檢查 git status |

---

## Completion Report
Report status using exactly one of:
- **DONE** — task confirmed, branch created, environment validated. Ready to begin `/s4-tdd`.
- **BLOCKED** — all remaining tasks have unmet dependencies; state which tasks and what they are waiting on.
- **NEEDS_CONTEXT** — state what environment information is missing.
</what-to-do>
<supporting-info>

## Artifact Dependencies
- **Reads**: TASK_DAG.md, RULES.md
- **Writes**: feature branch (git), runtime environment setup

→ Full reference: `references/detail.md`

</supporting-info>
