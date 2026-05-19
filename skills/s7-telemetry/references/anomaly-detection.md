# Anomaly Detection — SLO-Headroom-Relative Formula

## Formula

Use **SLO-headroom-relative detection** for any metric that has a defined SLO limit.
This prevents false positives on sub-millisecond operations where raw delta% is meaningless.

```
slo_consumption_delta = (post - pre) / SLO_limit
Flag as anomaly if slo_consumption_delta > 5%
```

For metrics with **no defined SLO** (e.g. throughput_rps), fall back to raw delta%:

```
raw_delta = (pre - post) / pre
Flag as anomaly if raw_delta > 20%
```

## Examples

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

Special case: if `memory_leak_detected` changes from `false` to `true` → always an anomaly.

## Severity Reference

Thresholds are expressed as % of SLO budget consumed by the regression
`(post - pre) / SLO_limit`. For metrics without a defined SLO, use raw delta%.

| SLO-delta consumed | Severity | Action |
|---|---|---|
| < 3% | Normal variance | No anomaly |
| 3–5% | Close to threshold | Log as warning in anomalies array |
| > 5% | Anomaly | Add to anomalies array |
| `post > 80% of SLO` | High risk | Present rollback decision to user |
| `post > 2× pre` | Critical regression | Present rollback decision to user |
