# telemetry.json Schema

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

## Required Fields

| Field | Type | Values |
|-------|------|--------|
| `status` | string | `"healthy"` \| `"degraded"` \| `"rolled_back"` |
| `simulation_mode` | boolean | `true` if dry-run, `false` if live |
| `metrics` | object | `error_rate`, `latency_p50_ms`, `latency_p95_ms`, `latency_p99_ms`, `throughput_rps` |
| `pre_deploy_baseline` | object | mirrors `metrics` keys + `source` pointing to perf-baseline.json |
| `anomalies` | array | empty array if none; each entry names the metric and delta |
| `next_cycle_inputs` | array | at least one entry; if empty, explain why in a comment |
| `rollback_triggered` | boolean | always `false` in simulation mode |
| `slo_compliance` | object | keyed by SLO name, value is `"PASS (<actual>)"` or `"FAIL (<actual>)"` |

## next_cycle_inputs Entry Format

```json
{
  "source": "pr-review | sast | perf | changelog | telemetry",
  "priority": "HIGH | MEDIUM | LOW",
  "description": "One-sentence actionable item"
}
```

## next_cycle_inputs Priority Guide

| Source | Default priority |
|---|---|
| Error rate anomaly in production | HIGH |
| P99 > 15% degradation | HIGH |
| PR review DEFERRED items | MEDIUM |
| Deprecated items in CHANGELOG | MEDIUM |
| SAST LOW severity suppressed | LOW |
| Single-test AC coverage | LOW |
