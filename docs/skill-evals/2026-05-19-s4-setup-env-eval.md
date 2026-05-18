# Skill Eval — s4-setup-env — 2026-05-19

**File**: `skills/s4-setup-env/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Lines 55–59: `<supporting-info>` names "Stage 3 (Task DAG)" (upstream) and `/s4-impl-task` & `/s4-tdd` (downstream) with explicit "Implementer" identity |
| 2 | 雙向阻斷 | ✅ | Lines 7–15: `<HARD-GATE>` block with 1 hard condition; Lines 39–46: "Red Flags" table with 3 concrete anti-patterns (skipping version check, starting without task selection, trusting old environment) |
| 3 | 輸入清洗 | ⚠️ | Lines 17–37 list steps (TASK_DAG.md, branch setup, environment validation) but failure scenarios lack explicit behavior: missing TASK_DAG.md, no unmet dependencies, version mismatch responses undefined |
| 4 | 漸進披露 | ✅ | Step list (lines 17–37) is ~30 lines of procedural text; bash examples at lines 24–32 are ~9 lines; dot graph (lines 62–83) is external reference; no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ | Lines 34–36 say "Run the project's environment check" and "npm ci / go mod download" but provide no fallback if version mismatch detected or dependencies unavailable; Step 4 workspace verification has no error path |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` or offline eval fixture directory in SKILL.md |

**Total**: 3.5/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗
- **Location**: Lines 17–46
- **Gap**:
  - Step 1: "Read TASK_DAG.md to identify next task" — no defined behavior if TASK_DAG.md doesn't exist or is malformed
  - Step 1: "all dependencies are marked [DONE]" — no guidance on what "unmet dependencies" means in artifact context
  - Step 3: "must match lock file" — no explicit BLOCKED response if version mismatch detected; suggestion to "install from lock file" but no fallback if lock file is corrupted
  - Step 4: "no uncommitted changes" — no defined behavior if dirty workspace found; does it BLOCKED or PARTIAL?
- **Impact**: Implementer may fail silently or with unclear error state; validation steps lack decision trees

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 34–37
- **Gap**:
  - Step 3: Environment validation references external checks (node/go/python version) but provides no fallback if mismatch detected — suggests "install from lock file" but if lock file is unavailable or corrupted, step fails with no recovery path
  - Step 4: Workspace verification ("no uncommitted changes") has no error recovery — is workspace cleaned, or is skill BLOCKED until user intervenes?
- **Impact**: High-risk environment setup can fail without clear recovery guidance; users stuck in failed state

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory; no offline test cases for environment setup validation (e.g., missing node_modules, version mismatch scenarios, dirty workspace states)
- **Impact**: Cannot verify environment validation logic remains consistent; skill behavior may drift across Claude versions

## Recommended Next Step

**Action**: Add explicit failure handling + fixture reference
1. Add to Step 1: "If TASK_DAG.md missing → BLOCKED: user must define task list"
2. Add to Step 3: "If version mismatch detected → BLOCKED: (show mismatch); user must resolve before proceeding"
3. Add to Step 4: "If workspace dirty → BLOCKED: commit or stash changes; state which files are uncommitted"
4. Add `<supporting-info>`: "Drift monitoring via `tests/fixtures/s4-setup-env/` (example cases: missing lock file, version mismatch, dirty workspace, unmet dependencies)"

