---
name: s7-telemetry
description: >
  Use when comparing pre/post deployment metrics. Outputs telemetry.json with anomaly
  detection and next iteration seeds. NOT for deployment or release decisions.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)

Check in order — stop at the first missing file:
1. Does any file matching `docs/releases/*-deploy.md` exist?
   - **No** → run `python skills/s0-eval-alignment/scripts/engine.py --suggest "docs/releases/*-deploy.md"`, report its output, and **STOP**.
   - **Yes, but no `Status: DEPLOYED` or `Status: DRY-RUN` line** → NEEDS_CONTEXT: "Deploy log exists but deployment status is missing. Update the deploy log, then return to /s7-telemetry."
2. Does `CHANGELOG.md` exist?
   - **No** → run `python skills/s0-eval-alignment/scripts/engine.py --suggest CHANGELOG.md`, report its output, and **STOP**.
   - **Yes, but no `## [vN.N.N]` version block** → NEEDS_CONTEXT: "CHANGELOG.md exists but has no version block. Run /s7-release-notes first."
3. Does any file matching `docs/tests/*-perf-baseline.json` exist?
   - **No** → run `python skills/s0-eval-alignment/scripts/engine.py --suggest "docs/tests/*-perf-baseline.json"`, report its output, and **STOP**.
   - **Yes, but `slo_gate` ≠ `"PASS"`** → NEEDS_CONTEXT: "Perf baseline exists but slo_gate is not PASS. Return to /s6-test-perf."

Only proceed when all three files exist with valid content.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After writing `docs/releases/YYYY-MM-DD-<version>-telemetry.json`, your message MUST end with exactly:
  "Stage 7 complete. next_cycle_inputs have been written to telemetry.json. Awaiting your approval to close this iteration."
Do NOT generate Stage 2 artifacts or begin the next iteration until the user explicitly approves.
</HARD-GATE>

<what-to-do>

**Release Manager (telemetry phase)**: Compare pre/post metrics, detect anomalies, produce handoff for next iteration.

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
Read `docs/tests/YYYY-MM-DD-perf-baseline.json`: extract P50/P95/P99 latency, error_rate_pct, throughput_rps, memory_leak_detected.

### Step 2 — Collect Post-Deploy Metrics
**Live**: Query production monitoring (Prometheus/Datadog/CloudWatch) over first 30m. **Simulation (dry-run)**: Re-run perf suite on installed artifact (match warmup_iterations). Extract same fields.

### Step 3 — Anomaly Detection
Apply SLO-headroom detection (formula: → `references/anomaly-detection.md`). Build table: Pre/Post/SLO/SLO-delta/Anomaly for each metric. Memory leak change false→true always anomaly.

### Step 4 — Rollback Decision
No anomalies → false. Anomaly (5-50% delta) → false + note. Any metric >80% SLO or >2× baseline or error >1% (live) → present to user, await auth. Simulation → false. Never auto-rollback.

### Step 5 — Extract next_cycle_inputs
From pr-review: DEFERRED. From SAST: LOW suppressed. From test-results: single-test ACs. From anomalies: 15-20% delta metrics. From CHANGELOG: deprecated. Format: source, priority (HIGH/MEDIUM/LOW), actionable description.

### Step 6 — Write telemetry.json
Write `docs/releases/YYYY-MM-DD-<version>-telemetry.json` (schema: → `references/telemetry-schema.md`). Commit with message "release(v<version>): add telemetry report".

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

Outputs: `docs/releases/YYYY-MM-DD-<version>-telemetry.json` with anomalies, status, next_cycle_inputs. Stage 7 final artifact.

→ Full reference: `references/detail.md`

## Artifact Dependencies
- **Reads**: `docs/tests/YYYY-MM-DD-perf-baseline.json`, `docs/releases/YYYY-MM-DD-<version>-deploy.md`, CHANGELOG.md, `docs/audit/*.md`, `test-results.json`
- **Writes**: `docs/releases/YYYY-MM-DD-<version>-telemetry.json`

</supporting-info>
