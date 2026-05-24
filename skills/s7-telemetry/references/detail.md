# s7-telemetry: Extended Reference

## Role Identity: Release Manager (Telemetry & Iteration Close)
- **Mindset**: Production sentinel and archaeologist. Confirm the ship is seaworthy, surface what should feed the next iteration.
- **Upstream Dependency**: `/s7-release-notes` (CHANGELOG committed) + `/s7-deploy` (deploy.md) + `/s6-test-perf` (perf-baseline.json).
- **Downstream Target**: `next_cycle_inputs` array → Product Manager's seed for `/s2-capture-vision`.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-telemetry/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Pipeline Position

```
[s7-build-artifact] → dist/<artifact>, git tag v<version>
        ↓
[s7-deploy] → docs/releases/.../deploy.md
        ↓
[s7-release-notes] → CHANGELOG.md
        ↓
[s7-telemetry] → docs/releases/.../telemetry.json   ← final artifact
```

## Simulation Mode Behavior

When `deploy_mode: "dry-run"` (no real production):
- Post-deploy metrics = re-run perf test suite on locally installed artifact
- `simulation_mode: true` in telemetry.json
- `status` field still uses `"healthy"` / `"degraded"` / `"rolled_back"` based on simulated metrics
- Anomaly detection threshold unchanged (20% rule still applies)
- `rollback_triggered` = `false` in dry-run (no live deployment to roll back)

## Process Flow

```
deploy.md (DEPLOYED/DRY-RUN) + CHANGELOG.md + perf-baseline.json
   ↓ All three exist?
   ├── NO → NEEDS_CONTEXT
   └── YES
        ↓
   Determine simulation_mode (from deploy.md)
        ↓
   Collect post-deploy metrics (live or re-run perf suite)
        ↓
   Compare pre vs post (20% rule per metric)
        ↓
   Any metric > 2× baseline?
   ├── YES (live mode) → present rollback decision to user → BLOCKED
   └── NO → log anomalies, continue
        ↓
   Extract next_cycle_inputs from audit/SAST/PR review/CHANGELOG
        ↓
   Write docs/releases/.../telemetry.json
        ↓
   git commit
        ↓
   "Stage 7 complete. next_cycle_inputs ready."
        ↓
   Await approval to close iteration
```
