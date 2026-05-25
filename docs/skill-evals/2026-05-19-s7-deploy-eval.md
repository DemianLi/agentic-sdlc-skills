# Skill Eval — s7-deploy — 2026-05-19

**File**: `skills/s7-deploy/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | Line 178: Upstream `/s7-build-artifact` named; Line 202–212: Pipeline diagram with next skill `/s7-release-notes` |
| 2 | 雙向阻斷 | ✅ PASS | Line 8–17: `<HARD-GATE>` with 2 concrete DO NOT conditions (artifact missing, no deploy target); Line 156–162: Red Flags table with 3 counter-examples |
| 3 | 輸入清洗 | ✅ PASS | Line 24–31: Deploy Mode Selection table defines 3 modes; Line 24 explicit: "Ask the user if unclear"; Line 41–51 confirms artifact via bash verification |
| 4 | 漸進披露 | ✅ PASS | Longest code block: Line 58–70 (12 lines); markdown template Line 111–148 (37 lines); all ≪ 50 lines |
| 5 | 優雅降級 | ✅ PASS | Step 2 branches to live/dry-run with explicit actions; Step 3 smoke tests with binary PASS/FAIL; Line 169 fallback behavior for test failure (BLOCKED status) |
| 6 | 漂移監控 | ✅ PASS | Line 182–187: References `tests/fixtures/s7-deploy/cases.json`; fixture verified on disk |

**Total**: 6/6 PASS — **READY**

## Defect Details

None. All 6 criteria met at PASS level.

## Recommended Next Step

Ship to production. No fixes required.
