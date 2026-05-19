# Deploy Log Template — s7-deploy

Write to `docs/releases/YYYY-MM-DD-<version>-deploy.md`:

```markdown
# Deploy Log — v<version> — YYYY-MM-DD

## Summary

| Field | Value |
|---|---|
| Deploy timestamp | YYYY-MM-DDTHH:MM:SSZ |
| Version | v1.0.0 |
| Environment | production \| staging \| local |
| Deploy mode | live \| dry-run |
| Artifact | dist/string-stats-api-1.0.0-py3-none-any.whl |
| SHA-256 | abc123... |
| Status | DEPLOYED \| DRY-RUN \| FAILED |

## Smoke Tests

| Test | Command | Result |
|---|---|---|
| Module import | `python -c "import string_stats"` | PASS |
| Version check | `python -c "import string_stats; print(string_stats.__version__)"` | PASS |
| Core function | `python -c "from string_stats import word_count; print(word_count('hi'))"` | PASS |

## Canary Metrics (live mode only)

| Metric | Value |
|---|---|
| Error rate (first 5 min) | 0.0% |
| P99 latency (first 5 min) | N/A (dry-run) |

## Final Status

**DEPLOYED** — all smoke tests pass, no rollback triggered.

_OR_

**DRY-RUN** — simulation complete, all steps would succeed. No live deployment was performed.
```

## Deploy Mode Field Reference

| Scenario | `deploy_mode` | `Status` in deploy.md |
|---|---|---|
| PyPI / Docker push succeeded | `"live"` | `DEPLOYED` |
| k8s rollout complete | `"live"` | `DEPLOYED` |
| Dry-run / trial validation | `"dry-run"` | `DRY-RUN` |
| Any deploy step failed | `"live"` or `"dry-run"` | `FAILED` |
