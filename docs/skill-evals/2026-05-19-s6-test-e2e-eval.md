# Skill Eval — s6-test-e2e — 2026-05-19

**File**: `skills/s6-test-e2e/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 4–14: Clear upstream (`/s6-test-integration`) and downstream (`/s6-test-perf`) boundaries with role context |
| 2 | 雙向阻斷 | ✅ | Lines 7–11, 28–34: HARD-GATE with 3 concrete negative triggers (flaky tests, screenshot validation, secondary deferral) |
| 3 | 輸入清洗 | ⚠️ | Line 21 reads `CONTEXT_SNAPSHOT.md` and line 40 defines NEEDS_CONTEXT fallback, but no explicit spec for valid E2E environment setup |
| 4 | 漸進披露 | ✅ | DOT diagram (22 lines), Red Flags table (4 rows), no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ⚠️ | Step 3 external dependency (run tests) lacks explicit fallback; NEEDS_CONTEXT at line 40 covers only environment setup, not test execution failures |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` in SKILL.md; no fixture directory on disk at `skills/s6-test-e2e/tests/fixtures/` |

**Total**: 4/6 PASS — **DRAFT** (2 PARTIAL, 1 FAIL blocks production routing)

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Line 21 (`CONTEXT_SNAPSHOT.md` read), line 40 (NEEDS_CONTEXT fallback)
- **Gap**: Skill reads external artifact but does not specify validation criteria. What constitutes a valid E2E setup? Missing: checklist of required files, test framework configuration, environment variables. Error handling defined only for missing context, not for malformed input.

### ⚠️ PARTIAL — Criterion 5: 優雅降級 (Graceful Degradation)
- **Location**: Step 3 (line 18–20), line 40 (fallback)
- **Gap**: Test execution has external dependency (run Playwright/Cypress/Selenium) but no fallback for execution failures. Line 40 NEEDS_CONTEXT only covers environment setup, not runtime failures (flaky test detection, timeout handling, partial results). If tests timeout or crash mid-run, behavior is undefined.

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: No reference found in SKILL.md
- **Defect**: Skill has no `tests/fixtures/` reference and no fixture directory exists on disk. Cannot monitor performance drift of the skill itself without offline eval fixtures.
- **Impact**: Model improvements cannot be validated against this skill's routing quality. Skill may silently drift out of bounds without detection.

## Recommended Next Step

**Before shipping**: Add fixture directory `skills/s6-test-e2e/tests/fixtures/` with ≥1 representative E2E test case (e.g., sample test suite output, real CONTEXT_SNAPSHOT.md, expected test-results artifact), then reference in SKILL.md as `Eval fixtures: see tests/fixtures/`.

