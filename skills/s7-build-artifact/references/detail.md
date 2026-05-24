# s7-build-artifact — Extended Reference

## Role Identity: Release Manager (Build Phase)
- **Mindset**: Build integrity guardian. Every artifact must be traceable to a specific commit and reproducible from that commit.
- **Upstream Dependency**: `/s6-verify-release` — `test-results.json` with `release_gate: "PASS"` is the entry token.
- **Downstream Target**: `/s7-deploy` reads the artifact path and SHA-256 from the build summary.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-build-artifact/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Pipeline Position

```
[s6-verify-release] → test-results.json (release_gate: PASS)
        ↓
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
test-results.json
   ↓ release_gate == PASS?
   ├── NO → BLOCKED (return to Stage 6)
   └── YES
        ↓
   Read version from manifest
        ↓
   Build artifact (python -m build / npm pack / docker build)
        ↓
   Capture SHA-256
        ↓
   Create git tag v<version>
        ↓
   Report Build Summary
        ↓
   Await approval → /s7-deploy
```
