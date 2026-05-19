# Skill Eval — s6-test-e2e — 2026-05-19

**File**: `skills/s6-test-e2e/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | Line 4: Upstream `/s6-test-integration` explicitly named. Line 4: Downstream `/s6-test-perf` explicitly named. Role: "QA Engineer" validates full user flows. Distinction clear: integration tests module boundaries; E2E tests full user journeys. |
| 2 | 雙向阻斷 | ✅ PASS | Lines 7–10: HARD-GATE with "Do NOT proceed to `/s6-test-perf` if any E2E test covering a main user flow fails." Lines 43–48: Red Flags section provides 3 concrete counter-examples: (1) flaky tests must be fixed here, (2) screenshots ≠ complete suite, (3) secondary failures deferred = 100x cost increase. |
| 3 | 輸入清洗 | ✅ PASS | Step 0 (lines 22–31): Input validation table explicitly lists 4 required preconditions with defined failure behaviors. Lines 28–30 specify BLOCKED and NEEDS_CONTEXT paths for missing framework, context snapshot, and environment access. All failure scenarios have defined behavior. |
| 4 | 漸進披露 | ✅ PASS | Largest inline blocks: Input validation table (lines 22–31): 10 rows. Red Flags table (lines 43–48): 4 rows. Process flow diagram (lines 86–107): ~22 lines. All blocks ≪ 50 lines. Reference external: "Artifact Standard" (lines 57–64). No boilerplate embedded. |
| 5 | 優雅降級 | ✅ PASS | External dependencies: E2E test framework (Playwright/Cypress/Selenium), `CONTEXT_SNAPSHOT.md` read, test environment access. Step 0 (lines 22–31) maps each dependency to explicit fallback: BLOCKED if framework missing, NEEDS_CONTEXT if context missing, BLOCKED if environment inaccessible, DONE_WITH_CONCERNS if tests timeout mid-run. All covered. |
| 6 | 漂移監控 | ✅ PASS | Line 73: "Fixtures located at `tests/fixtures/s6-test-e2e/cases.json`." Fixture verified on disk (3.1K). Purpose stated: "Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario." |

**Total**: 6/6 PASS — **PRODUCTION READY**

## Defect Details

None — all criteria met at production threshold.

## Recommended Next Step

This skill is production-ready. No fixes required. Monitor fixture coverage in future evaluation cycles to detect model drift in flaky test detection and main-flow identification accuracy.

