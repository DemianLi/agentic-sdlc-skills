# Skill Eval — s3-breakdown-wbs — 2026-05-19

**File**: `skills/s3-breakdown-wbs/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 98: names `/s3-build-dag` as downstream dependency; line 4 names `/s3-design-arch` as upstream context |
| 2 | 雙向阻斷 | ✅ | Lines 73–80: "Red Flags" block with 3 concrete counter-examples (task boundary ambiguity, 5-min ceiling, incomplete work) |
| 3 | 輸入清洗 | ⚠️ | Lines 18–31: Role and task format defined, but no explicit user input specification; failure scenarios undefined |
| 4 | 漸進披露 | ✅ | Largest blocks: task format (lines 37–46, ~10 lines), Mermaid diagram (lines 102–124, ~23 lines); no block exceeds 50 lines |
| 5 | 優雅降級 | ✅ | Line 10: explicit git commit requirement; line 88: BLOCKED status defined; step 4 awaits user approval before proceeding |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` directory referenced anywhere in SKILL.md |

**Total**: 5/6 PASS — **NEAR-READY** — address Criterion 3 and Criterion 6 before shipping

## Defect Details

### ⚠️ WEAK — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Lines 18–91
- **Gap**: SKILL.md describes the role and workflow, but does not explicitly enumerate user inputs or define failure behavior for each. The skill operates by reading an artifact from `/s3-design-arch` (line 51), but:
  - No explicit check: "What if the design doc does not exist on disk?"
  - No explicit check: "What if the design doc is malformed (missing sections)?"
  - No explicit check: "What if the user provides feedback that contradicts atomic task principles?"
  - Step 4 (line 65) says "Wait for approval" but does not define what behavior follows if approval is denied or delayed.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: Entire file
- **Defect**: SKILL.md does not reference `tests/fixtures/` directory. No offline eval fixture set exists on disk to prevent skill drift as underlying models evolve.
- **Impact**: Without fixtures, there is no way to regression-test this skill's decomposition logic. Task atomicity criteria (Section "What Makes a Task Atomic?") are subjective; fixtures would operationalize them.

## Recommended Next Step

1. **Add input linting section** (lines 18–22) that explicitly lists:
   - Input: design doc path (must exist and be committed)
   - Input: user feedback on task list (must include approval signal)
   - Failure behavior: if design doc is missing, state BLOCKED and list exact file path needed
   - Failure behavior: if feedback is unclear, request clarification on specific task boundaries

2. **Create a fixture set** at `tests/fixtures/s3-breakdown-wbs/` with ≥1 example:
   - A minimal design.md file (from `/s3-design-arch`)
   - Expected WBS.md output (atomicity-validated task list)
   - This allows regression testing when the skill is retrained.
