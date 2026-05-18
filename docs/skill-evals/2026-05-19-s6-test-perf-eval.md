# Skill Eval — s6-test-perf — 2026-05-19

**File**: `skills/s6-test-perf/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 4: "after /s6-test-e2e" (upstream); line 14: "before /s6-verify-release" (downstream); boundaries clear |
| 2 | 雙向阻斷 | ✅ | Lines 7–11, 62–68: HARD-GATE with 3 concrete counter-examples (P95 margin abuse, missing baseline, environment variance) |
| 3 | 輸入清洗 | ⚠️ | Line 21 reads "performance acceptance criteria from Stage 2" but doesn't specify error handling if criteria missing; line 58 mentions regression comparison "if exists" baseline without explicit failure mode |
| 4 | 漸進披露 | ✅ | Python warmup code (12 lines), JSON schema (15 lines), DOT diagram (20 lines); no single inline block exceeds 50 lines |
| 5 | 優雅降級 | ✅ | Step 2 run load test (external dep) → BLOCKED if targets exceeded (line 74); missing baseline → NEEDS_CONTEXT (line 75); Step 4 optional memory/deadlock detection with clear fallback semantics |
| 6 | 漂移監控 | ❌ | No reference to `tests/fixtures/` in SKILL.md; no fixture directory on disk at `skills/s6-test-perf/tests/fixtures/` |

**Total**: 5/6 PASS — **NEAR READY** (1 PARTIAL, 1 FAIL — address Criterion 6 before shipping)

## Defect Details

### ⚠️ PARTIAL — Criterion 3: 輸入清洗 (Input Linting)
- **Location**: Line 21 (load perf targets), line 58 (regression check)
- **Gap**: Step 1 reads performance AC from Stage 2 requirements but doesn't specify error handling if criteria are missing, malformed, or use non-standard units. Step 5 regression check assumes baseline exists ("if exists") but doesn't define behavior when baseline is absent or corrupted. Missing explicit validation: is the 80% vs 95% percentile calculation consistent? Are thresholds numeric?

### ❌ FAIL — Criterion 6: 漂移監控 (Drift Monitoring)
- **Location**: No reference found in SKILL.md
- **Defect**: Skill has no `tests/fixtures/` reference and no fixture directory exists on disk. Cannot validate performance baseline logic across model versions.
- **Impact**: Performance validation logic may degrade silently without offline fixtures. Changes to P50/P95/P99 calculation or SLO gate logic won't be caught by regression tests.

## Recommended Next Step

**Before shipping**: Create `skills/s6-test-perf/tests/fixtures/` with ≥1 representative perf-baseline.json artifact (real load test output with documented P50/P95/P99 values), then reference in SKILL.md as `Eval fixtures: see tests/fixtures/`. This enables offline validation of metric capture and SLO gate logic.

