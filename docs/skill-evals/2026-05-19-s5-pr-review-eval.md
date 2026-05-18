# Skill Eval — s5-pr-review — 2026-05-19

**File**: `skills/s5-pr-review/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 150–155: `<supporting-info>` names upstream `/s5-audit-rules` and downstream `/s5-fix-optimize`, explains role as "peer review mode" with "constructive critic" mindset distinct from SAST auditor |
| 2 | 雙向阻斷 | ✅ | Line 8–19: `<HARD-GATE>` with "Do NOT proceed to `/s5-fix-optimize` if ANY CRITICAL issue remains unresolved"; Red Flags table (line 130–136) provides 3 concrete counter-examples (test pass ≠ code quality, small changes ≠ low risk, checklist skipping) |
| 3 | 輸入清洗 | ✅ | Inputs explicitly listed (line 45–48): `git diff`, `TASK_DAG.md`, commit messages, design doc, `CONTEXT.md`. Failure scenarios defined: line 146 "NEEDS_CONTEXT — design doc not found; cannot validate scope; state what is missing." All failure cases mapped to completion states. |
| 4 | 漸進披露 | ✅ | Largest inline block: Step 2 checklist (line 60–69): 10 lines. Red Flags table: 7 lines. Code example block (line 79–106): 28 lines, <50 limit. Hotfix report template (line 110–123): 14 lines. Process flow diagram externalized (line 158–182). All blocks under 50 lines. |
| 5 | 優雅降級 | ⚠️ | External dependencies: `TASK_DAG.md` read, git operations (read-only), design doc read. No explicit fallback for missing `TASK_DAG.md`. Line 45 "Read `TASK_DAG.md`" has no BLOCKED label if file missing. Completion state "NEEDS_CONTEXT" (line 146) exists but workflow step has no early BLOCKED check. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md. No fixture samples, example PRs, or test case set mentioned. Criterion 6 FAIL. |

**Total**: 4/6 PASS — DRAFT

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Line 45–48 (Step 1 in workflow)
- **Gap**: "Read `TASK_DAG.md`" (line 45) assumes file exists. "Read commit messages" via `git log` (line 46) assumes git history exists. No fallback if `TASK_DAG.md` is missing. Completion state "NEEDS_CONTEXT" (line 146) exists but no early BLOCKED check in workflow.
- **Impact**: If `TASK_DAG.md` is missing, Step 1 fails silently or produces invalid scope comparison. Should BLOCKED immediately with clear message if `TASK_DAG.md` not found.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory. No example PRs, scope drift samples, or test case set mentioned for drift monitoring.
- **Impact**: Cannot verify skill consistency. Skill's peer review logic changes silently with model updates; no offline eval set exists to detect regressions in scope drift detection, CRITICAL identification, or security spot-checks.

## Recommended Next Step

Create `tests/fixtures/` directory with example PRs, `TASK_DAG.md` samples, and expected review reports (e.g., `tests/fixtures/2026-05-19-pr-samples/`) for drift monitoring. Add explicit BLOCKED check at Step 1 if `TASK_DAG.md` is not found or cannot be read.
