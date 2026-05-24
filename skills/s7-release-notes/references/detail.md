# s7-release-notes — Extended Reference

## Role Identity: Release Manager (Release Notes Phase)
- **Mindset**: Historian. Every entry is auditable, traceable to a requirement, and honest about what changed.
- **Upstream Dependency**: `/s7-deploy` — deploy log must confirm the version was deployed (or dry-run completed).
- **Downstream Target**: `/s7-telemetry` uses the CHANGELOG to populate `next_cycle_inputs`.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-release-notes/cases.json`。

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
Deploy log (Status: DEPLOYED or DRY-RUN)
   ↓ Status confirmed?
   ├── NO → BLOCKED
   └── YES
        ↓
   git log v<prev>..v<current> --oneline
        ↓
   Read REQ-N titles from requirements doc
        ↓
   Classify commits → Added / Changed / Fixed / Breaking
        ↓
   Write CHANGELOG.md block
        ↓
   git add CHANGELOG.md && git commit
        ↓
   Await approval → /s7-telemetry
```
