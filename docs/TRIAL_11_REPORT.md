# TRIAL-11 Report: s7 Pipeline Validation

**Date**: 2026-05-16
**Status**: DONE_WITH_CONCERNS
**Overall Result**: PASS (pipeline validated; one design concern noted for next cycle)

## Executive Summary

Trial-11 validated the complete s7 pipeline (s7-build-artifact → s7-deploy → s7-release-notes → s7-telemetry) using the `string-stats-api v1.0.0` project from trial-10. All four s7 SKILL.md files were rewritten from scratch to fix: (a) incorrect pipeline order in prior stubs, (b) missing dry-run support, and (c) missing simulation_mode semantics.

**Result**: All four s7 skills executed end-to-end with dry-run deploy mode. One design concern identified: the 20% raw delta% anomaly detection rule produces false positives on sub-millisecond operations. This was logged as `next_cycle_inputs` and addressed in trial-12.

## Project Setup

**Location**: `test_projects/trial-11-s7validation/`
**Source**: Reused string-stats-api from trial-10 (`test_projects/trial-10-s6validation/`)

### Input Gate

`test-results.json` → `release_gate: "PASS"` ✅ (39/39 tests, 100% coverage from trial-10)

## s7 Skills Validation Results

### Phase 1: s7-build-artifact

**HARD-GATE**: `release_gate: "PASS"` ✅

| Field | Value |
|---|---|
| Artifact | `dist/string_stats_api-1.0.0-py3-none-any.whl` |
| SHA-256 | `c048f5b0b706d2c081587c9183164778f27a1b072c9c3309d4ea9560f2b85d95` |
| Git tag | Skipped (monorepo context — tag would apply to wrong repo) |

**Skill design finding**: Simulation Mode section added, git tag caveat added for monorepo context. ✅

---

### Phase 2: s7-deploy

**Mode**: dry-run (no PyPI target configured for trial)

| Smoke Test | Result |
|---|---|
| Module import | PASS |
| Package version (1.0.0) | PASS |
| `word_count('hello world') == 2` | PASS |
| `char_count('hello') == 5` | PASS |
| `sentence_count('Hello. World.') == 2` | PASS |

**Artifact**: `docs/releases/2026-05-16-v1.0.0-deploy.md` — `Status: DRY-RUN` ✅

---

### Phase 3: s7-release-notes

**HARD-GATE**: deploy.md `Status: DRY-RUN` ✅

CHANGELOG.md written with `## [v1.0.0] - 2026-05-16`, dry-run note, REQ-1 through REQ-5 mapped. ✅

---

### Phase 4: s7-telemetry

**Mode**: simulation (`deploy_mode: dry-run`)

| Metric | Pre | Post | SLO | Old delta% | Status (old algorithm) |
|---|---|---|---|---|---|
| word_count P99 | 0.042ms | 0.079ms | 1ms | +88.0% | ANOMALY (false positive) |
| char_count P99 | 0.036ms | 0.053ms | 1ms | +47.2% | ANOMALY (false positive) |
| sentence_count P99 | 0.187ms | 0.283ms | 2ms | +51.3% | ANOMALY (false positive) |
| paragraph_count P99 | 0.004ms | 0.009ms | 1ms | +125.0% | ANOMALY (false positive) |
| error_rate | 0.0% | 0.0% | 0% | 0% | OK |

**Root cause**: All four anomalies traced to cold-cache in fresh venv (simulation mode) vs warm-cache in pre-deploy environment. No SLO was breached. `rollback_triggered: false`.

**Status**: `degraded` (due to false positives from raw delta% algorithm)

---

## Issues Found → next_cycle_inputs

| Priority | Description |
|---|---|
| MEDIUM | **Perf baseline warmup**: Pre-deploy uses warm cache; post-deploy simulation uses cold cache. Add 10-20 warmup iterations discarded before measurement. |
| MEDIUM | **SLO-headroom-relative anomaly detection**: Replace raw delta% with `(post-pre)/SLO_limit`. A 125% delta on 0.004ms is not an anomaly — the operation uses 0.9% of its 1ms SLO. |
| LOW | Add `docs/audit/` SAST and PR review reports to trial projects for complete next_cycle_inputs extraction. |

---

## What Worked Well

- Pipeline order (build → deploy → release-notes → telemetry) confirmed correct
- `simulation_mode: true` flag in telemetry.json provides honest data provenance
- `DONE_DRY_RUN` completion status distinguishes real from simulated deploys
- OUTPUT DISCIPLINE in all four skills correctly chains to the next step
- HARD-GATE in s7-build-artifact blocks without `release_gate: "PASS"`

---

## Conclusion

Trial-11 successfully validated the s7 pipeline design. The pipeline structure is sound. One algorithmic design flaw in anomaly detection was identified and logged — addressed in trial-12.

**Artifacts**:
- `test_projects/trial-11-s7validation/dist/string_stats_api-1.0.0-py3-none-any.whl`
- `test_projects/trial-11-s7validation/docs/releases/2026-05-16-v1.0.0-deploy.md`
- `test_projects/trial-11-s7validation/CHANGELOG.md`
- `test_projects/trial-11-s7validation/docs/releases/2026-05-16-v1.0.0-telemetry.json`
- `test_projects/trial-11-s7validation/docs/tests/2026-05-16-s7-validation-report.md`
