---
name: s4-setup-env
description: 研發環境就緒 (Implementation & Local Debug)
---
<HARD-GATE>
Do NOT start any implementation until:
1. The specific TASK-N from `TASK_DAG.md` has been confirmed with the user.
2. The feature branch has been created and checked out.
3. The local environment matches the tech stack from Stage 1 exactly.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s4-impl-task and /s4-tdd.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **Implementer**.
Your task is to prepare the development environment for a specific Atomic Task.
1. **Task Assignment**: Read `TASK_DAG.md` to identify the next task where all dependencies are marked `[DONE]`. Confirm with user: *"Next task is TASK-N: <title>. Starting this now — confirm?"*
2. **Branch Setup**: Create or checkout the feature branch: `git checkout -b task-N-<slug>` or pull the correct branch.
3. **Environment Validation**: Run the project's environment check to confirm all dependencies match Stage 1's locked versions:
   - `node --version` / `go version` / `python --version` — must match lock file
   - `npm ci` / `go mod download` — install from lock file, not latest
4. **Workspace Verification**: Confirm no uncommitted changes from prior task that might contaminate this one.

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

</supporting-info>
