# Skill Eval — s7-telemetry — 2026-05-19

**File**: `skills/s7-telemetry/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 4–5, 228–229: Names upstream dependencies `/s7-release-notes`, `/s7-deploy`, `/s6-test-perf` and downstream target "Product Manager / /s2-capture-vision"; clear boundary: telemetry phase is iteration closure, produces `next_cycle_inputs` |
| 2 | 雙向阻斷 | ✅ | Lines 8–14, 20, 212: 3+ negative triggers ("Do NOT produce telemetry.json until 3 dependencies exist", "Do NOT generate Stage 2 artifacts until user approves", "Never trigger rollback automatically") with concrete decision table (lines 119–126) |
| 3 | 輸入清洗 | ✅ | Lines 29–43: Inputs explicitly specified (deploy_mode from deploy.md, baseline from perf-baseline.json, CHANGELOG); each failure scenario has defined behavior (simulation_mode flag, re-run test suite, NEEDS_CONTEXT if missing) |
| 4 | 漸進披露 | ✅ | Largest code block: 32 lines (lines 155–188, telemetry.json example JSON structure); largest table: 8 rows (lines 271–278, next_cycle_inputs priority guide); both under 50-line threshold |
| 5 | 優雅降級 | ⚠️ | Lines 46–73: Live mode metric collection (Prometheus curl, lines 56–61) has no fallback if monitoring service is unavailable. Simulation mode re-run (lines 64–75) is defined but no retry if test suite fails. Anomaly detection formula (lines 84–103) is read-only, no fallback if perf-baseline.json metrics are incomplete. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` reference found in SKILL.md; no fixture directory exists for s7-telemetry |

**Total**: 4/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 46–103 (Step 2: Collect Post-Deploy Metrics, Step 3: Anomaly Detection)
- **Gap**: Live mode metric collection (lines 56–61) has no fallback if Prometheus is unreachable or returns empty series. If monitoring service is down, skill reports nothing. Simulation mode re-run (lines 64–75) assumes pytest succeeds — no retry logic if test suite fails or hangs. Anomaly detection formula (lines 84–103) assumes both `pre_deploy_baseline` and post-deploy metrics are complete; if any field is missing, the comparison will fail without a defined fallback (e.g., "skip comparison if baseline is incomplete").
- **Impact**: In production, unreachable monitoring or failed test re-run will block iteration closure with no path forward.

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: File-wide
- **Defect**: No reference to `tests/fixtures/` directory in SKILL.md. No fixture files exist for evaluating telemetry-phase correctness.
- **Impact**: Skill has no offline eval harness. Model drift in metric calculation or anomaly detection logic cannot be detected.

## Recommended Next Step

1. **Fix Criterion 5**: Add fallback behavior to lines 46–103. Example: "If Prometheus is unreachable, mark metrics as `source: 'unavailable'` and set `status: 'degraded'` rather than blocking. If test re-run fails, use pre-deploy baseline values as post-deploy estimates and note `estimated_metrics: true` in telemetry.json." Define a "minimum viable telemetry" output for each scenario.
2. **Fix Criterion 6**: Create `skills/s7-telemetry/tests/fixtures/` with ≥2 fixtures: (1) sample `perf-baseline.json` (2) sample `deploy.md` with live and dry-run variants. Reference in SKILL.md under "Validation" section.
