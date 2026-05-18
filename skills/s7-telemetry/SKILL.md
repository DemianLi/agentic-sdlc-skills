---
name: s7-telemetry
description: >
  Use after /s7-release-notes to compare pre/post deploy performance metrics, detect
  anomalies, and extract next_cycle_inputs for the next iteration.
---

<HARD-GATE>
Do NOT produce `telemetry.json` until ALL of the following exist:
1. `docs/releases/YYYY-MM-DD-<version>-deploy.md` with `Status: DEPLOYED` or `Status: DRY-RUN`
2. `CHANGELOG.md` with the current version block (`## [vN.N.N]`)
3. `docs/tests/YYYY-MM-DD-perf-baseline.json` with `slo_gate: "PASS"` (pre-deploy baseline)

Missing any of these means Stage 7 is incomplete — report `NEEDS_CONTEXT` and halt.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After writing `docs/releases/YYYY-MM-DD-<version>-telemetry.json`, your message MUST end with exactly:
  "Stage 7 complete. next_cycle_inputs have been written to telemetry.json. Awaiting your approval to close this iteration."
Do NOT generate Stage 2 artifacts or begin the next iteration until the user explicitly approves.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the telemetry and iteration close phase.
Your task is to compare pre-deploy and post-deploy metrics, detect anomalies, and produce
the handoff artifact that seeds the next Product Manager session.

## Simulation Mode vs Live Mode

**Determine mode first** by reading `docs/releases/YYYY-MM-DD-<version>-deploy.md`:
- If `deploy_mode: "dry-run"` → **simulation mode**
- If `deploy_mode: "live"` → **live mode**

| Mode | Post-deploy metrics source | `simulation_mode` in telemetry.json |
|---|---|---|
| live | Real production monitoring (Prometheus, Datadog, CloudWatch) | `false` |
| dry-run | Re-run perf test suite on the locally installed artifact | `true` |

In simulation mode, post-deploy metrics come from running the perf test suite
against the newly installed artifact. This is an honest approximation — set
`simulation_mode: true` so downstream readers know the data source.

## Workflow

### Step 1 — Collect Pre-Deploy Baseline

Read `docs/tests/YYYY-MM-DD-perf-baseline.json`. Extract:
- `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`
- `error_rate_pct`
- `throughput_rps`
- `memory_leak_detected`

### Step 2 — Collect Post-Deploy Metrics

#### Live Mode
Query production monitoring for the same metrics over the first 30 minutes post-deploy:
```bash
# Example: Prometheus query
curl -s 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))'
```

#### Simulation Mode (dry-run)
Re-run the performance test suite against the installed package:
```bash
# Install the newly built artifact (if not already installed)
pip install dist/<artifact>.whl

# Re-run perf tests — IMPORTANT: match warmup_iterations from perf-baseline.json
cd tests/perf
pytest test_perf.py -v --json-report --json-report-file=perf-post-deploy.json
```

**Warmup parity**: Read `warmup_iterations` from `perf-baseline.json` and use the same value when re-running the post-deploy suite. If the pre-deploy baseline used 10 warmup iterations, the post-deploy re-run must also use 10. Mismatched warmup states cause systematic cold-cache bias in the delta.

Extract the same fields from the test output: P50/P95/P99 latency, error rate, throughput.

### Step 3 — Anomaly Detection

**Use SLO-headroom-relative detection** for any metric that has a defined SLO limit.
This prevents false positives on sub-millisecond operations where raw delta% is meaningless.

**Formula (for latency metrics with a defined SLO)**:
```
slo_consumption_delta = (post - pre) / SLO_limit
Flag as anomaly if slo_consumption_delta > 5%
```

```
Example A — sub-ms operation, trivial noise (old algorithm: false positive):
  pre_p99 = 0.004ms, post_p99 = 0.009ms, SLO = 1ms
  old: (0.009 - 0.004) / 0.004 = 125% delta → WRONG ANOMALY
  new: (0.009 - 0.004) / 1.0   = 0.5% of SLO consumed → no anomaly ✓

Example B — real regression:
  pre_p99 = 0.187ms, post_p99 = 0.290ms, SLO = 1ms
  new: (0.290 - 0.187) / 1.0   = 10.3% of SLO consumed → ANOMALY ✓

Example C — metric with no SLO (throughput_rps) — fall back to raw delta:
  pre = 14838 rps, post = 9000 rps
  fallback: (14838 - 9000) / 14838 = 39.3% → ANOMALY ✓
```

Build a comparison table:

| Metric | Pre | Post | SLO | SLO-delta | Anomaly? |
|---|---|---|---|---|---|
| latency_p50_ms | X | Y | N ms | Z% | YES / NO |
| latency_p95_ms | X | Y | N ms | Z% | YES / NO |
| latency_p99_ms | X | Y | N ms | Z% | YES / NO |
| error_rate_pct | X | Y | 0% | raw delta | YES / NO |
| throughput_rps | X | Y | — | raw delta | YES / NO |

If `memory_leak_detected` changes from `false` to `true` → always an anomaly, regardless of delta.

### Step 4 — Rollback Decision

| Condition | Decision |
|---|---|
| No anomalies | `rollback_triggered: false` |
| Anomaly detected (SLO-delta 5-50%) | `rollback_triggered: false` + note in `anomalies` |
| Any metric `post > 80% of SLO_limit` | Present to user, await rollback authorization |
| Any metric `post > 2× pre-deploy baseline` | Present to user, await rollback authorization |
| Error rate > 1% in live mode | Present to user, await rollback authorization |
| Simulation mode | `rollback_triggered: false` (no live deployment to roll back) |

**Never trigger rollback automatically** — always require explicit user confirmation.

### Step 5 — Extract next_cycle_inputs

Synthesize what the next iteration should address. Sources:

| Source | What to extract |
|---|---|
| `docs/audit/YYYY-MM-DD-<branch>-pr-review.md` | DEFERRED items |
| `docs/audit/YYYY-MM-DD-<branch>-sast.md` | LOW severity items that were suppressed |
| `test-results.json` traceability | ACs covered by only one test (low confidence) |
| Anomalies from Step 3 | Metrics with delta 15-20% (close to threshold) |
| `CHANGELOG.md` | Deprecated items |

Each entry must be actionable:
```json
{
  "source": "pr-review | sast | perf | changelog | telemetry",
  "priority": "HIGH | MEDIUM | LOW",
  "description": "One-sentence actionable item"
}
```

### Step 6 — Write telemetry.json

Write to `docs/releases/YYYY-MM-DD-<version>-telemetry.json`:

```json
{
  "timestamp": "2026-05-16T12:00:00Z",
  "version": "1.0.0",
  "simulation_mode": true,
  "status": "healthy",
  "metrics": {
    "error_rate": 0.0,
    "latency_p50_ms": 0.003,
    "latency_p95_ms": 0.183,
    "latency_p99_ms": 0.187,
    "throughput_rps": 14838
  },
  "pre_deploy_baseline": {
    "latency_p50_ms": 0.003,
    "latency_p95_ms": 0.183,
    "latency_p99_ms": 0.187,
    "throughput_rps": 14838,
    "source": "docs/tests/YYYY-MM-DD-perf-baseline.json"
  },
  "anomalies": [],
  "next_cycle_inputs": [
    {
      "source": "pr-review",
      "priority": "LOW",
      "description": "Add OpenAPI spec for /api/analyze endpoint (deferred from Stage 5 PR review)"
    }
  ],
  "rollback_triggered": false,
  "slo_compliance": {
    "<metric>_p99_under_<Nms>": "PASS (<actual>ms) | FAIL (<actual>ms)"
  }
}
```

Required fields (from HANDOFF.md Stage 7 → Next Iteration):
- `status`: `"healthy"` | `"degraded"` | `"rolled_back"`
- `metrics`: object with `error_rate`, `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`, `throughput_rps`
- `pre_deploy_baseline`: object mirroring `metrics` keys, plus `source` pointing to the perf-baseline.json file — makes the comparison auditable
- `anomalies`: array (empty array if none, each entry names the metric and delta)
- `next_cycle_inputs`: array (at least one entry; if truly empty, explain why)
- `rollback_triggered`: boolean
- `slo_compliance`: object keyed by SLO name (e.g. `word_count_p99_under_1ms`), value is `"PASS (<actual>)"` or `"FAIL (<actual>)"`

Commit the file:
```bash
git add docs/releases/YYYY-MM-DD-<version>-telemetry.json
git commit -m "release(v<version>): add telemetry report and close iteration"
```

## Red Flags — 停下來重新考慮

| 如果你在想… | 現實是 |
|------------|--------|
| simulation_mode 就不用真的比較指標了 | simulation_mode 只改變數據來源，不取消比較；pre 和 post 仍然要比較，只是 post 來自本地重跑 |
| anomalies 是空的代表沒問題 | 空的 anomalies 要靠實際計算支撐；不能因為「看起來沒問題」就直接填空陣列 |
| next_cycle_inputs 我不知道下一輪要做什麼 | next_cycle_inputs 從 audit、SAST、deferred PR comments 中提取；如果全是空的，說明上游 Stage 5 文檔不完整 |
| 我直接 rollback，不問用戶 | Rollback 是生產操作；必須先報告，取得授權後才執行 |

## Completion Report

Report status using exactly one of:
- **DONE** — `telemetry.json` committed; `status: healthy`; `next_cycle_inputs` ready for Product Manager. Iteration closed.
- **DONE_WITH_CONCERNS** — `telemetry.json` committed; anomalies detected but below rollback threshold; listed in report.
- **BLOCKED** — rollback decision required; state the specific metric, the threshold, and the actual value.
- **NEEDS_CONTEXT** — deploy log, CHANGELOG, or perf baseline missing; state which artifact is absent.

</what-to-do>

<supporting-info>

## Role Identity: Release Manager (Telemetry & Iteration Close)
- **Mindset**: Production sentinel and archaeologist. Confirm the ship is seaworthy, surface what should feed the next iteration.
- **Upstream Dependency**: `/s7-release-notes` (CHANGELOG committed) + `/s7-deploy` (deploy.md) + `/s6-test-perf` (perf-baseline.json).
- **Downstream Target**: `next_cycle_inputs` array → Product Manager's seed for `/s2-capture-vision`.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-telemetry/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: `docs/tests/YYYY-MM-DD-perf-baseline.json`, `docs/releases/YYYY-MM-DD-<version>-deploy.md`, `CHANGELOG.md`, `docs/audit/*.md`, `test-results.json`
- **Writes**: `docs/releases/YYYY-MM-DD-<version>-telemetry.json`

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

## Anomaly Severity Reference

Thresholds are expressed as % of SLO budget consumed by the regression
`(post - pre) / SLO_limit`. For metrics without a defined SLO, use raw delta%.

| SLO-delta consumed | Severity | Action |
|---|---|---|
| < 3% | Normal variance | No anomaly |
| 3–5% | Close to threshold | Log as warning in anomalies array |
| > 5% | Anomaly | Add to anomalies array |
| `post > 80% of SLO` | High risk | Present rollback decision to user |
| `post > 2× pre` | Critical regression | Present rollback decision to user |

## next_cycle_inputs Priority Guide

| Source | Default priority |
|---|---|
| Error rate anomaly in production | HIGH |
| P99 > 15% degradation | HIGH |
| PR review DEFERRED items | MEDIUM |
| Deprecated items in CHANGELOG | MEDIUM |
| SAST LOW severity suppressed | LOW |
| Single-test AC coverage | LOW |

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

</supporting-info>
