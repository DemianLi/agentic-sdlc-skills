# Skill Eval — s3-build-dag — 2026-05-19

**File**: `skills/s3-build-dag/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 122: names `/s3-breakdown-wbs` as upstream; lines 123–124 name downstream "Stage 4 Implementer" with explicit purpose (task execution ordering) |
| 2 | 雙向阻斷 | ✅ | Lines 98–105: "Red Flags" block with 3 concrete counter-examples (cycle detection, fuzzy dependencies, over-long critical path) |
| 3 | 輸入清洗 | ⚠️ | Lines 26–28: workflow loads tasks from WBS.md, but no explicit input validation; missing: "What if WBS.md has circular dependencies?" |
| 4 | 漸進披露 | ✅ | Mermaid example (lines 37–52, ~16 lines), markdown template (lines 71–92, ~22 lines); no block exceeds 50 lines |
| 5 | 優雅降級 | ✅ | Line 10: explicit git commit requirement; line 143: cycle detection → BLOCKED path defined; step 5 awaits user approval (line 94) |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md |

**Total**: 5/6 PASS — **NEAR READY** — address Criterion 3 and Criterion 6 before shipping

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Lines 20–95
- **Gap**: Workflow reads `docs/arch/YYYY-MM-DD-<topic>-wbs.md` (line 27) but does not validate input before processing:
  - No explicit check: "What if WBS.md does not exist on disk?"
  - No explicit check: "What if a TASK has a circular dependency in its 'Blocked by' field?"
  - No explicit check: "What if TASK complexity estimates are missing or malformed?"
  - Step 5 mentions user approval (line 94) but no timeout or escalation defined if approval is not received.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire file
- **Defect**: SKILL.md does not reference `tests/fixtures/` directory. No offline eval fixture set exists on disk.
- **Impact**: Without fixtures, DAG construction logic cannot be regression-tested. Topological sort behavior, critical path calculation, and parallelism detection are all subject to drift.

## Recommended Next Step

1. **Add input validation section** (after line 20) that explicitly lists:
   - Input: WBS.md path (must exist and contain TASK-N items)
   - Input: each TASK's "Blocked by" field (must be valid TASK-M references or "none")
   - Failure behavior: if WBS.md is missing, state BLOCKED and list path needed
   - Failure behavior: if cycle detected, state BLOCKED and enumerate cycle (already documented at line 143 but needs explicit check before Step 2)

2. **Create a fixture set** at `tests/fixtures/s3-build-dag/` with ≥1 example:
   - A minimal WBS.md (from `/s3-breakdown-wbs`)
   - Expected TASK_DAG.md output (with Mermaid, critical path, parallelism)
   - A malformed WBS.md that triggers cycle detection (for regression)
