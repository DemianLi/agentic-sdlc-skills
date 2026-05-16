---
name: s7-build-artifact
description: >
  製品建構 — 讀取 test-results.json 確認 release_gate，建構版本化 artifact，
  打 git tag，為 /s7-deploy 提供可追蹤的 build 產出。
---

<HARD-GATE>
Do NOT proceed with the build if `test-results.json` does not exist at project root
or if `release_gate` is not `"PASS"`. A blocked or missing gate file means Stage 6
did not complete — this is a pipeline violation, not a judgment call.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After presenting the build summary, your message MUST end with exactly:
  "Awaiting your approval to proceed to /s7-deploy."
Do NOT generate the next stage's artifact, code, or analysis until the user
explicitly approves. A user response that is silent on approval is NOT approval.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the build phase.
Your task is to produce a versioned, reproducible artifact from the source that passed Stage 6.

## Pre-flight Check

Before building, verify all of the following. Stop immediately and report `NEEDS_CONTEXT` if any check fails.

| Check | What to verify | If it fails |
|---|---|---|
| `test-results.json` exists | File present at project root | `NEEDS_CONTEXT: test-results.json missing. Cannot build without Stage 6 gate.` |
| `release_gate` is PASS | `cat test-results.json \| jq .release_gate` == `"PASS"` | `BLOCKED: release_gate is not PASS. Stage 7 is unconditionally blocked until Stage 6 issues are resolved.` |
| Version is set | `pyproject.toml` / `package.json` / `go.mod` has an explicit version | `NEEDS_CONTEXT: no version found in project manifest. Set version before building.` |
| Build tool available | `python -m build` / `npm pack` / `go build` works | Report specific error and missing dependency |

## Workflow

### Step 1 — Determine Artifact Type

| Project type | Artifact | Build command |
|---|---|---|
| Python library | `.whl` + `.tar.gz` | `python -m build` |
| Python service | Docker image | `docker build -t <name>:<version> .` |
| Node library | `.tgz` | `npm pack` |
| Node service | Docker image | `docker build -t <name>:<version> .` |
| Go binary | Binary | `go build -o dist/<name> .` |

If a `Dockerfile` is present, prefer the Docker path for services.

### Step 2 — Build

```bash
# Python wheel example:
pip install build
python -m build
# Outputs: dist/<name>-<version>-py3-none-any.whl and dist/<name>-<version>.tar.gz

# Verify contents:
ls -lh dist/
```

Capture the exact SHA-256 of the primary artifact:
```bash
shasum -a 256 dist/<artifact>
```

### Step 3 — Git Tag

```bash
git tag -a v<version> -m "Release v<version>"
# Verify:
git show v<version> --stat
```

Do NOT push the tag to remote unless the user explicitly instructs it.

### Step 4 — Report Build Summary

Present a structured summary:

```
## Build Summary

| Field | Value |
|---|---|
| Version | v1.0.0 |
| Artifact type | Python wheel |
| Primary artifact | dist/string-stats-api-1.0.0-py3-none-any.whl |
| SHA-256 | abc123... |
| Git tag | v1.0.0 |
| Build timestamp | 2026-05-16T11:30:00Z |
| Reproducible | yes (pinned deps in requirements.txt) |
```

## Simulation Mode

If no registry is configured (e.g., trial validation context), the artifact lives in `dist/`
and the git tag is local only. This is acceptable — document it as `deploy_target: "local"`.
Do NOT attempt to push to PyPI / Docker Hub / npm unless explicitly instructed.

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| release_gate 是 BLOCKED 但測試其實都過了 | 你在 Stage 7，不是 Stage 6。Stage 6 有修正的機會；如果 release_gate 不是 PASS，退回 Stage 6，不要繼續 |
| 版本號沒 bump，先用舊版本建構 | 如果版本未更新，新舊 artifact 無法區分；build 前必須確認版本號已正確 |
| 我直接 push tag 到 remote | 推送 tag 是不可逆操作；不要在未獲授權的情況下推送 |

## Completion Report

Report status using exactly one of:
- **DONE** — artifact built; SHA-256 captured; git tag created. Ready for `/s7-deploy`.
- **BLOCKED** — `release_gate` not PASS; list the specific value found.
- **NEEDS_CONTEXT** — state exactly what is missing (build tool, version, manifest).

</what-to-do>

<supporting-info>

## Role Identity: Release Manager (Build Phase)
- **Mindset**: Build integrity guardian. Every artifact must be traceable to a specific commit and reproducible from that commit.
- **Upstream Dependency**: `/s6-verify-release` — `test-results.json` with `release_gate: "PASS"` is the entry token.
- **Downstream Target**: `/s7-deploy` reads the artifact path and SHA-256 from the build summary.

## Artifact Dependencies
- **Reads**: `test-results.json`, `pyproject.toml` / `package.json` / `go.mod`, source files
- **Writes**: `dist/<artifact>` (or Docker image layer cache), local git tag `v<version>`

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

</supporting-info>
