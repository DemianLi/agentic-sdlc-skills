# Skill Eval — s6-verify-release — 2026-05-19

**File**: `skills/s6-verify-release/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 5: "after all Stage 6 tests pass"; line 161: upstream `/s6-test-perf`, downstream "Stage 7 Release Manager"; clear boundaries |
| 2 | 雙向阻斷 | ✅ | Lines 8–16, 140–146: HARD-GATE with 3 concrete counter-examples (manual JSON, coverage rounding, missing traceability) |
| 3 | 輸入清洗 | ✅ | Step 0 (lines 41–50): pre-flight check table with 4 explicit conditions and defined NEEDS_CONTEXT behavior for each failure mode |
| 4 | 漸進披露 | ✅ | Bash examples (11 lines), JSON schema (31 lines), DOT diagram (20 lines), table (7 rows); no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ✅ | Step 1 test execution (external dep) → NEEDS_CONTEXT if runner missing (line 47) or no test files (line 48); Step 3 traceability check → BLOCKER if AC unmapped (line 74); all external deps have defined fallback |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` in SKILL.md; no fixture directory on disk at `skills/s6-verify-release/tests/fixtures/` |

**Total**: 5/6 PASS — **NEAR READY** (0 PARTIAL, 1 FAIL — address Criterion 6 before shipping)

## Defect Details

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: No reference found in SKILL.md
- **Defect**: Skill has no `tests/fixtures/` reference and no fixture directory exists on disk. Cannot validate test-results.json schema, traceability matrix logic, or release gate decisions across model updates.
- **Impact**: Changes to gate logic, schema validation, or AC traceability mapping won't be caught by regression tests. Release gate decisions may become misaligned without offline eval fixtures.

## Recommended Next Step

**Before shipping**: Create `skills/s6-verify-release/tests/fixtures/` with ≥1 representative test-results.json artifact (sample output showing PASS and BLOCKED scenarios with full traceability matrix), then reference in SKILL.md as `Eval fixtures: see tests/fixtures/`. This enables offline validation of gate logic and schema conformance.

