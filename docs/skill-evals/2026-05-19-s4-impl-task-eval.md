# Skill Eval — s4-impl-task — 2026-05-19

**File**: `skills/s4-impl-task/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Lines 44–48: `<supporting-info>` names `/s4-tdd` (upstream) and `/s4-local-debug` (downstream) with explicit role identity as "Implementer" |
| 2 | 雙向阻斷 | ✅ | Lines 7–15: `<HARD-GATE>` block with 1 hard condition; Lines 27–34 "Red Flags" table provides 3 concrete anti-patterns (code style refactor, out-of-scope modifications, premature implementation) |
| 3 | 輸入清洗 | ⚠️ | Lines 17–26 list inputs (test files, TASK_DAG.md) but failure scenarios (missing tests, ambiguous AC, locked branch) have no explicit behavior defined beyond "STOP and invoke /s4-tdd" |
| 4 | 漸進披露 | ✅ | Lines 27–34 "Red Flags" inline table is 8 rows (~30 lines); Step list (lines 20–25) is procedural, not repetitive boilerplate; no inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ | Lines 20–25 step 2 says "Do not touch files outside File Scope" but no fallback if File Scope is unclear; Step 5 writes to TASK_DAG.md with no error path if update fails (write-dependent, high blast-radius) |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` or any offline eval fixture directory in SKILL.md |

**Total**: 3.5/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗
- **Location**: Lines 17–26
- **Gap**: Task inputs (test files, TASK_DAG.md, RULES.md) are listed, but failure scenarios lack defined behavior:
  - If test file doesn't exist → Step 1 says "STOP and invoke /s4-tdd first" but doesn't specify BLOCKED vs. PARTIAL
  - If TASK_DAG.md entry is incomplete → no guidance on which AC field is required
  - If RULES.md conflicts with implementation → Step 3 says "raise it" but no escalation path defined
- **Impact**: Implementer may proceed with incomplete information without clear understanding of required vs. optional inputs

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 20–25 (Step 2), Line 25 (Step 5)
- **Gap**: 
  - Step 2 references "File Scope declared in this task's `TASK_DAG.md` entry" but provides no fallback if File Scope is ambiguous or missing
  - Step 5 writes to `TASK_DAG.md` (checkpoint operation) with no error handling if the file is locked, corrupted, or unwritable
- **Impact**: High blast-radius write without fallback means silent failure to mark task complete, breaking DAG tracking

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: Entire SKILL.md
- **Defect**: No reference to `tests/fixtures/` directory; no offline test cases provided for drift monitoring as model versions evolve
- **Impact**: Cannot verify skill behavior remains stable across Claude versions; drift undetectable

## Recommended Next Step

**Action**: Add ≥1 fixture directory reference + define fallback for missing/ambiguous inputs
1. Add to `<what-to-do>` (after Step 1): explicit BLOCKED condition for missing test files
2. Add `<supporting-info>` note: "Drift monitoring via `tests/fixtures/s4-impl-task/` (example cases: duplicate implementation, over-engineered code, file scope violation)"
3. For Step 5: wrap TASK_DAG.md update in error handling note

