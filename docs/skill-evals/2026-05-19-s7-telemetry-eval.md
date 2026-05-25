# Skill Eval — s7-telemetry — 2026-05-19

**File**: `skills/s7-telemetry/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ PASS | Line 229: Upstream dependencies named (`/s7-release-notes` + `/s7-deploy` + `/s6-test-perf`); Line 243–253: Pipeline shows final artifact role |
| 2 | 雙向阻斷 | ✅ PASS | Line 8–14: `<HARD-GATE>` with 3 concrete DO NOT conditions (deploy.md missing, CHANGELOG missing, perf baseline missing); Line 205–212: Red Flags table with 4 counter-examples |
| 3 | 輸入清洗 | ✅ PASS | Line 29–42: Simulation vs Live mode explicitly defined; Line 46–52: Pre-Deploy Baseline inputs listed (4 metrics); Line 54–77: Post-Deploy collection split into live/dry-run branches with warmup parity requirement (Line 75) |
| 4 | 漸進披露 | ✅ PASS | Longest JSON template: Line 155–187 (32 lines); longest table: Line 119–126 (7 lines); all ≪ 50 lines |
| 5 | 優雅降級 | ✅ PASS | Line 122–128: Rollback Decision table with explicit "never trigger automatically" (Line 128); Line 125: Simulation mode fallback ("no live deployment to roll back"); Line 100–103: SLO-headroom-relative anomaly detection prevents cold-cache false positives |
| 6 | 漂移監控 | ✅ PASS | Line 232–237: References `tests/fixtures/s7-telemetry/cases.json`; fixture verified on disk |

**Total**: 6/6 PASS — **READY**

## Defect Details

None. All 6 criteria met at PASS level.

## Recommended Next Step

Ship to production. No fixes required.
