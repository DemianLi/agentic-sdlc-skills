# s7-deploy — Extended Reference

## Role Identity: Release Manager (Deploy Phase)
- **Mindset**: Deployment accountant. Every action is logged. No deploy is "done" until smoke tests confirm it.
- **Upstream Dependency**: `/s7-build-artifact` — artifact path and SHA-256 are required inputs.
- **Downstream Target**: `/s7-release-notes` reads the deploy log to confirm what version was shipped.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-deploy/cases.json`。

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
[s7-telemetry] → docs/releases/.../telemetry.json
```

## Process Flow

```
Artifact from /s7-build-artifact
   ↓ Confirm artifact exists
   ↓
Deploy mode? (live / dry-run)
   ├── live → deploy to target → wait for rollout
   └── dry-run → simulate commands → record [DRY-RUN] prefix
        ↓
   Smoke tests (binary PASS/FAIL per test)
        ↓
   All smoke tests PASS?
   ├── NO → BLOCKED (report failure, await rollback decision)
   └── YES → Write docs/releases/.../deploy.md
        ↓
   git commit
        ↓
   Await approval → /s7-release-notes
```
