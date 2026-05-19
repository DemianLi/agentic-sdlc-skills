# Skill Eval — s5-sast-lint — 2026-05-19

**File**: `skills/s5-sast-lint/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | Line 126: Upstream "Stage 4 output" (unit tests GREEN). Line 127: Downstream `/s5-audit-rules` explicitly named. Distinction: this skill runs formatter/linter/SAST FIRST; /s5-audit-rules performs human audit after. Role described as "unforgiving machine" vs. peer reviewer. Clear semantic boundary. |
| 2 | 雙向阻斷 | ✅ PASS | Lines 8–14: HARD-GATE with "Do NOT hand off to `/s5-audit-rules` if there are CRITICAL linting errors, SAST findings (HIGH or CRITICAL severity), or formatting issues remaining." Lines 102–108: Red Flags table provides 3 concrete counter-examples: (1) WARNING is not ignorable, (2) CI reliance false security, (3) formatter is prerequisite. |
| 3 | 輸入清洗 | ✅ PASS | Inputs explicitly listed in Step 1 (line 24): `RULES.md` from Stage 1. Failure handling: line 118 completion state "NEEDS_CONTEXT — linter config not found in RULES.md; state what is missing." Step 4 (line 55) defines severity classification (CRITICAL/WARNING/INFO) with defined actions. All failure scenarios mapped. |
| 4 | 漸進披露 | ✅ PASS | Largest inline blocks: Steps 2–4 code examples (lines 31–49): ~19 lines total. Classification severity table (lines 54–59): 6 lines. Red Flags table (lines 102–108): 7 lines. Example report (lines 78–98): ~21 lines. All blocks ≪ 50 lines. No boilerplate embedded. |
| 5 | 優雅降級 | ✅ PASS | External dependencies: tool execution (formatter, linter, SAST), `RULES.md` read (all read-only). Completion states (lines 114–118) define 4 output paths: DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT. Missing `RULES.md` maps to "NEEDS_CONTEXT". All dependencies have defined fallback. |
| 6 | 漂移監控 | ✅ PASS | Line 164 explicitly references: "Fixtures located at `tests/fixtures/s5-sast-lint/cases.json`." Fixture verified on disk (3.1K). Purpose clearly stated: "Smoke test: sequentially verify skill output structure and expected_behavior alignment for each scenario." |

**Total**: 6/6 PASS — **PRODUCTION READY**

## Defect Details

None — all criteria met at production threshold.

## Recommended Next Step

This skill is production-ready. No fixes required. Monitor fixture coverage in future evaluation cycles to detect model drift in CRITICAL/WARNING classification accuracy and SAST finding detection.
