---
name: s6-test-perf
description: >
  Use when validating performance under load — P50/P95/P99, SLO gates, baselines.
  Outputs perf report JSON. NOT for functional testing.
---
<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s6-test-perf`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed to `/s6-verify-release` if performance metrics exceed the thresholds
defined in the REQ acceptance criteria from Stage 2. Performance regressions are BLOCKING.
3. The performance baseline report must be machine-generated from actual load test execution — a manually created baseline does NOT satisfy this gate.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the required artifact, proceed immediately to /s6-verify-release.
Do NOT skip /s6-verify-release’s own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **QA Engineer**. Validate system performance under load.

### Step 1 — Load Performance Targets

Read performance ACs from Stage 2 requirements (e.g., "P99 < 200ms at 100 concurrent users").

### Step 2 — Run Load Tests

Use appropriate tool (k6, Artillery, Locust, ab) per project standards.

### Step 3 — Warmup Before Measurement

Run 10–20 warmup iterations (discard) before capturing P50/P95/P99. Warmup ensures JIT, filesystem cache, and module imports reach steady state (production-like). Record `warmup_iterations` in perf-baseline.json.

### Step 4 — Capture Baseline Metrics

- Response time: P50, P95, P99
- Error rate under load
- Throughput (req/s at target concurrency)
- Memory usage (detect leak over 10-min sustained load, optional but recommended)
- Database deadlock detection (PostgreSQL/MySQL, optional but recommended)

### Step 5 — Regression Check

Compare vs previous baseline (if exists). Any metric 20%+ worse is a regression.

### Step 6 — Write Baseline File

Output: `docs/tests/YYYY-MM-DD-perf-baseline.json` (see Artifact Standard). Read by `/s7-telemetry` post-deploy.

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

**Reads**: source files, RULES.md (performance thresholds if defined)  
**Writes**: `docs/tests/YYYY-MM-DD-perf-baseline.json`

## Eval Fixtures

Fixtures located at `tests/fixtures/s6-test-perf/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
