---
name: s6-test-perf
description: >
  效能與壓力測試 — 在負載下驗證 SLO 達標，捕獲 P50/P95/P99 基線，
  輸出結構化 perf-baseline.json 作為 /s7-telemetry 的 pre-deploy 對比基準。
---
<HARD-GATE>
Do NOT proceed to `/s6-verify-release` if performance metrics exceed the thresholds
defined in the REQ acceptance criteria from Stage 2. Performance regressions are BLOCKING.
3. The performance baseline report must be machine-generated from actual load test execution — a manually created baseline does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, your message MUST end with exactly:
  “Awaiting your approval to proceed to /s6-verify-release.”
Do NOT generate the next stage’s artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>
You are the **QA Engineer**.
Your task is to validate system performance under load.
1. **Load performance targets**: Read performance acceptance criteria from Stage 2 requirements (e.g., "API must respond < 200ms at P99 under 100 concurrent users").
2. **Run load tests**: Execute performance tests with a tool appropriate to the project (k6, Artillery, Locust, ab).
3. **Warmup before measurement**: Run 10–20 warmup iterations (discard results) before capturing the actual P50/P95/P99 metrics. Warmup ensures the runtime (interpreter JIT, OS file-system cache, module import) reaches steady state — the same hot state as a production request.

   ```python
   # Warmup phase — discard these results
   for _ in range(10):
       func(test_input)

   # Measurement phase — capture these
   times = []
   for _ in range(N_iterations):
       t0 = time.perf_counter()
       func(test_input)
       times.append((time.perf_counter() - t0) * 1000)
   ```

   Record `warmup_iterations` in `perf-baseline.json` so `/s7-telemetry` can reproduce the same warm-state condition when re-running post-deploy.

4. **Capture baseline metrics**:
   - Response time: P50, P95, P99
   - Error rate under load
   - Throughput (req/s at target concurrency)
   - Memory usage (no leak over 10-minute sustained load)
5. **Regression check**: Compare against previous iteration's baseline (if exists). Any metric 20%+ worse is a regression.
6. **Report format**: Provide numeric values for every metric, not vague descriptions.
7. **Write `docs/tests/YYYY-MM-DD-perf-baseline.json`** — see Artifact Standard. This file is the pre-deploy baseline read by `/s7-telemetry` for post-deploy comparison.

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| P95 超標但只超了一點點 | 「一點點」是主觀判斷；定義在 REQ 的門檻是客觀值；超過就是超過，沒有「差一點」的特例 |
| 這是新功能，沒有 baseline 可比較所以跳過 | 第一次就沒 baseline，但仍然要驗證是否符合 Stage 2 performance AC；無法驗證就是 BLOCKED |
| 測試環境機器比較慢，實際部署後會更快 | 部署環境和測試環境配置應該相同；如果不同就說明測試不representative；不representative 的測試結果不能當 gate |

## Completion Report
Report status using exactly one of:
- **DONE** — all performance targets met; no regressions detected; baseline captured for `/s7-telemetry`. Proceeding to `/s6-verify-release`.
- **DONE_WITH_CONCERNS** — targets met, but note metrics that are close to the threshold.
- **BLOCKED** — performance target failed; state the metric, the target, and the actual value (e.g., "P99 = 450ms, target = 200ms").
- **NEEDS_CONTEXT** — no performance acceptance criteria defined in Stage 2; state what thresholds to use.
</what-to-do>
<supporting-info>
## Artifact Standard
Output file: `docs/tests/YYYY-MM-DD-perf-baseline.json`

This file is consumed by `/s7-telemetry` as the pre-deploy baseline for production comparison. Every field must come from the load test tool's output — no manual estimates.

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "tool": "k6 | Artillery | Locust | ab | custom-timing-harness",
  "concurrency": 100,
  "duration_seconds": 600,
  "warmup_iterations": 10,
  "latency_p50_ms": 38,
  "latency_p95_ms": 95,
  "latency_p99_ms": 180,
  "error_rate_pct": 0.08,
  "throughput_rps": 820,
  "memory_leak_detected": false,
  "slo_gate": "PASS"
}
```

Field rules:
- `slo_gate`: `"PASS"` if all Stage 2 performance ACs met; `"FAIL"` blocks progression to `/s6-verify-release`
- `memory_leak_detected`: set to `true` if memory grows monotonically over the 10-minute sustained test

## Role Identity: QA Engineer
- **Mindset**: Stress instigator. You push the system to its limits to see where it cracks. The baseline you capture here is the contract that `/s7-telemetry` will hold production to.
- **Upstream Dependency**: `/s6-test-e2e`.
- **Downstream Target**: `/s6-verify-release`.

## Artifact Dependencies
- **Reads**: source files, `RULES.md` (performance thresholds if defined)
- **Writes**: `docs/tests/YYYY-MM-DD-perf-baseline.json`

## Process Flow

```dot
digraph test_perf {
    rankdir=TD;
    load     [label="1. Load perf AC\nfrom OpenSpec", shape=box];
    run      [label="2. Run load test\n(k6 / Artillery)", shape=box];
    capture  [label="3. Capture P50 / P95 / P99\nand throughput", shape=box];
    regress  [label="Regression > 20%\nvs baseline?", shape=diamond];
    slo      [label="SLO targets\nmet?", shape=diamond];
    done     [label="DONE → /s6-verify-release", shape=doublecircle];
    concerns [label="DONE_WITH_CONCERNS\nlist regressions", shape=doublecircle];
    blocked  [label="BLOCKED\nSLO breach", shape=doublecircle];

    load -> run;
    run -> capture;
    capture -> regress;
    regress -> concerns [label="yes — minor"];
    regress -> slo [label="no"];
    slo -> done [label="met"];
    slo -> blocked [label="not met"];
}
```

</supporting-info>
