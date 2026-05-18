# Skill Eval — s7-deploy — 2026-05-19

**File**: `skills/s7-deploy/SKILL.md`
**Evaluator**: s0-eval-skill

## Score Summary

| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | 衝突防禦 | ✅ | Line 4–5, 179–180: Names upstream dependency `/s7-build-artifact` (artifact is required input) and downstream target `/s7-release-notes` (reads deploy log); clear boundary: deploy phase takes artifact and validates with smoke tests |
| 2 | 雙向阻斷 | ✅ | Lines 8–12, 16: 3+ negative triggers ("Do NOT proceed if artifact not available", "Do NOT skip /s7-release-notes's own HARD-GATE conditions", "Never attempt a real deploy without explicit user confirmation") with concrete scenarios |
| 3 | 輸入清洗 | ✅ | Lines 24–37: Deploy mode must be explicitly selected (live / dry-run / gitops); if unclear, "Ask the user" is defined; failure mode is NEEDS_CONTEXT (line 170) |
| 4 | 漸進披露 | ✅ | Largest code block: 36 lines (lines 111–148, deploy.md template example); largest table: 9 rows (lines 116–124); both under 50-line threshold |
| 5 | 優雅降級 | ⚠️ | Lines 54–86: Live mode deploy steps (twine upload, flyctl deploy, kubectl) have no fallback if they fail. Line 88 says "record every command with [DRY-RUN] prefix" but live mode failure handling is missing. Smoke tests (lines 90–103) are binary PASS/FAIL but no retry or partial-pass fallback defined. |
| 6 | 漂移監控 | ❌ | No `tests/fixtures/` reference found in SKILL.md; no fixture directory exists for s7-deploy |

**Total**: 4/6 PASS — NEAR READY

## Defect Details

### ⚠️ PARTIAL — Criterion 5: 優雅降級
- **Location**: Lines 54–106 (Step 2: Deploy + Step 3: Smoke Tests)
- **Gap**: Live mode deploy commands (lines 57–70) have no fallback on failure. If `twine upload` fails or `kubectl rollout` hangs, skill only reports "deploy failed" (line 169) without a retry strategy, circuit-breaker timeout, or rollback trigger. Smoke tests are binary (line 105: "Each smoke test must produce a binary PASS/FAIL result") but no definition of what constitutes a "recoverable" vs "fatal" test failure.
- **Impact**: Partial deploy (some images pushed, some rollouts incomplete) will block with no guidance on cleanup or retry.

### ❌ FAIL — Criterion 6: 漂移監控
- **Location**: File-wide
- **Defect**: No reference to `tests/fixtures/` directory in SKILL.md. No fixture files exist for evaluating deploy-phase correctness as models drift.
- **Impact**: Skill has no offline test harness. Changes in model behavior cannot be detected.

## Recommended Next Step

1. **Fix Criterion 5**: Add explicit rollback/retry logic to lines 54–86. Example: "If `twine upload` fails, check package integrity (pip check), then retry once before reporting DEPLOY_FAILED." Define which smoke test failures are recoverable (retryable) vs fatal (rollback-required).
2. **Fix Criterion 6**: Create `skills/s7-deploy/tests/fixtures/` with ≥1 fixture (e.g., `mock_artifact.whl` or `docker_image_mock.json`) and reference in SKILL.md under "Validation" section.
