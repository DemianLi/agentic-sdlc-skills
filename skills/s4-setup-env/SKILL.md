---
name: s4-setup-env
description: >
  Use at the start of each atomic task to verify the workspace is clean, the correct
  branch is checked out, and the dev environment is ready for implementation.
---
<HARD-GATE>
Do NOT start any implementation until:
1. Environment check passed and workspace is verified as clean.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s4-tdd (or /s4-impl-task if tests already exist).
Do NOT skip /s4-tdd’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>
You are the **Implementer**.
Your task is to prepare the development environment for a specific Atomic Task.
1. **Task Assignment**: Read `TASK_DAG.md` to identify the next task where all dependencies are marked `[DONE]`. Confirm with user: *"Next task is TASK-N: <title>. Starting this now — confirm?"*
2. **Branch Setup**: 選擇以下其中一種工作流：

   **標準模式**（單一工作目錄）：
   ```bash
   git checkout -b task-N-<slug>
   ```

   **Worktree 模式**（並行開發，多個 task 同時進行不需 stash 切換）：
   ```bash
   git worktree add ../task-N-<slug> -b task-N-<slug>
   cd ../task-N-<slug>
   ```
   Worktree 模式讓每個 task 在獨立目錄下開發，適合 DAG 中多條平行路徑同時推進的場景。
3. **Environment Validation**: Run the project's environment check to confirm all dependencies match Stage 1's locked versions:
   - `node --version` / `go version` / `python --version` — must match lock file
   - `npm ci` / `go mod download` — install from lock file, not latest
4. **Workspace Verification**: Confirm no uncommitted changes from prior task that might contaminate this one.

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
## Role Identity: Implementer
- **Mindset**: Clean workbench. You don't start coding until the tools are sharp and the environment is pristine.
- **Upstream Dependency**: Stage 3 (Task DAG).
- **Downstream Target**: `/s4-impl-task` & `/s4-tdd`.
## Process Flow

```dot
digraph setup_env {
    rankdir=TD;
    select   [label="1. Select Task\nfrom TASK_DAG.md", shape=box];
    branch   [label="2. Checkout\nfeature branch", shape=box];
    runtime  [label="Runtime matches\nRULES.md?", shape=diamond];
    install  [label="3. Install deps\n(pinned versions)", shape=box];
    clean    [label="Workspace clean?\n(no leftover state)", shape=diamond];
    ready    [label="4. Environment\nREADY", shape=box];
    done     [label="DONE → /s4-impl-task\n& /s4-tdd", shape=doublecircle];
    blocked  [label="BLOCKED\nfix runtime", shape=doublecircle];

    select -> branch;
    branch -> runtime;
    runtime -> install [label="yes"];
    runtime -> blocked [label="no — mismatch"];
    install -> clean;
    clean -> ready [label="yes"];
    clean -> install [label="no — clean first"];
    ready -> done;
}
```

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s4-setup-env/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: `TASK_DAG.md`, `RULES.md`
- **Writes**: feature branch (git), runtime environment setup

</supporting-info>
