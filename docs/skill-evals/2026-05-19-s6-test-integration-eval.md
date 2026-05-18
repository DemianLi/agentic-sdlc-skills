# Skill Eval — s6-test-integration — 2026-05-19

**File**: `skills/s6-test-integration/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ⚠️ | Line 5 names `/s6-test-e2e` (downstream); upstream is "Stage 4 completed" but no adjacent skill named for comparison |
| 2 | 雙向阻斷 | ✅ | Lines 7–10, 45–51: HARD-GATE with 3 concrete counter-examples (local vs CI, single failing path, incomplete environment) |
| 3 | 輸入清洗 | ⚠️ | Step 0 (lines 22–35) validates branch merge status with BLOCKED behavior; Steps 1–7 outline workflow but missing input validation for missing/malformed `TASK_DAG.md`, requirements file |
| 4 | 漸進披露 | ✅ | DOT diagram (20 lines), bash snippet (3 lines), Red Flags table (4 rows); no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ | Step 1 reads `TASK_DAG.md` with no fallback; Step 3 runs test suite with BLOCKED if fail (line 56) but no fallback strategy for failures |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` in SKILL.md; no fixture directory on disk at `skills/s6-test-integration/tests/fixtures/` |

**Total**: 4/6 PASS — **DRAFT** (2 PARTIAL, 1 FAIL blocks production routing)

## Defect Details

### ⚠️ PARTIAL — Criterion 1: 衝突防禦 (Semantic Anti-Collision)
- **Location**: Line 5 (description)
- **Gap**: Downstream boundary clearly stated (`/s6-test-e2e`), but upstream boundary vague. Line 37 says "after Stage 4 is complete" but doesn't name the specific upstream skill (if any). For dozens of coexisting skills, "Stage 4" is ambiguous. Should be: "Use after /s5-<skill-name> to validate..." or explicitly state if this is the first test skill in the workflow.

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Step 0 (lines 22–35), Steps 1–7 (lines 37–42)
- **Gap**: Step 0 validates branch merge status with defined BLOCKED behavior. However, Steps 1–7 assume existence of `TASK_DAG.md` (line 37), requirements file (line 75), and test runner config without explicit validation. Error handling missing for: file not found, malformed YAML/JSON, missing test framework.

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Steps 1 and 3 (lines 37–42)
- **Gap**: Step 1 reads `TASK_DAG.md` file (external dependency) with no fallback if file missing. Step 3 runs test suite with no fallback for test failures — only BLOCKED status. If test runner crashes or CI environment incomplete, behavior undefined.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: No reference found in SKILL.md
- **Defect**: Skill has no `tests/fixtures/` reference and no fixture directory exists on disk. Cannot validate skill's routing quality across model updates.
- **Impact**: Integration test logic may silently become misaligned without offline eval fixtures for regression detection.

## Recommended Next Step

**Before shipping**: Add fixture directory `skills/s6-test-integration/tests/fixtures/` with ≥1 representative integration test result (e.g., sample TASK_DAG.md, mock requirements file, expected integration-results.md), then reference in SKILL.md. Also clarify upstream boundary: name the specific upstream skill or confirm this is the first test skill.

