---
name: s7-deploy
description: >
  Use after /s7-build-artifact to deploy the versioned artifact to the target
  environment and confirm with smoke tests — supports dry-run mode for environments without live infra.
---

<HARD-GATE>
Do NOT proceed if:
1. The artifact from `/s7-build-artifact` is not available (no `dist/` contents or Docker image).
2. No deploy target is defined AND `dry-run` mode has not been explicitly selected.

---
⛔ OUTPUT DISCIPLINE — applies after the gate conditions above are met:
After writing `docs/releases/YYYY-MM-DD-<version>-deploy.md`, proceed immediately to /s7-release-notes.
Do NOT skip /s7-release-notes's own HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in the deployment phase.
Your task is to deploy the versioned artifact and confirm stability via smoke tests.

## Deploy Mode Selection

**First action**: determine the deploy mode. Ask the user if unclear.

| Mode | When to use | `deploy_mode` field in deploy.md |
|---|---|---|
| `live` | Real target available (k8s, fly.io, Docker registry, PyPI) | `"live"` |
| `dry-run` | No real target (trial, CI preview, local validation) | `"dry-run"` |
| `gitops` | 團隊使用 ArgoCD / Flux；部署即為 PR 合入 main，CD pipeline 自動觸發 | `"gitops"` |

**GitOps 模式說明**：選擇 `gitops` 時，「部署」動作本身即為將變更 PR 合入 `main` 分支。不需手動執行 `kubectl apply` 或 `fly deploy`。Smoke test 應等待 ArgoCD sync / Flux reconcile 完成後再執行（通常透過 `argocd app wait <app> --sync` 或觀察 CD pipeline 狀態確認）。

In `dry-run` mode, simulate every step and record what *would* happen.
Never attempt a real deploy without explicit user confirmation.

## Workflow

### Step 1 — Confirm Artifact

Verify the build output from `/s7-build-artifact`:
```bash
# Python wheel
ls -lh dist/
# Docker image
docker images | grep <name>
```

Record the artifact path and SHA-256 that will be deployed.

### Step 2 — Deploy

#### Live Mode (real target)

```bash
# PyPI
twine upload dist/*

# Docker (fly.io example)
flyctl deploy --image <name>:<version>

# k8s
kubectl set image deployment/<name> <container>=<image>:<version>
kubectl rollout status deployment/<name>

# npm
npm publish
```

Wait for rollout confirmation before proceeding to smoke tests.

#### Dry-Run Mode (simulation)

```bash
# Simulate install from local wheel
pip install dist/<name>-<version>-*.whl --dry-run

# OR: actually install locally (safe, not a real publish)
pip install dist/<name>-<version>-*.whl

# Simulate Docker push (build only, no push)
docker build -t <name>:<version> . --no-cache
echo "[DRY-RUN] Would push: <registry>/<name>:<version>"
```

Record every command with its output, prefixed with `[DRY-RUN]` in the deploy log.

### Step 3 — Smoke Tests

Run smoke tests immediately after deploy (live) or simulated install (dry-run):

```bash
# Python library smoke test
python -c "import <module>; print(<module>.__version__)"

# API service smoke test
curl -s http://localhost:<port>/health | jq .status

# Verify key function
python -c "from string_stats import word_count; print(word_count('hello world'))"
```

Each smoke test must produce a binary PASS/FAIL result.

### Step 4 — Write Deploy Log

Full deploy log template with all required fields (Summary, Smoke Tests, Canary Metrics, Final Status):
→ `references/deploy-log-template.md`

Write to `docs/releases/YYYY-MM-DD-<version>-deploy.md` using that template.

Commit the deploy log:
```bash
git add docs/releases/YYYY-MM-DD-<version>-deploy.md
git commit -m "release(v<version>): add deploy log"
```

## Red Flags — 停下來，這可能是不可逆操作

| 如果你在想… | 現實是 |
|------------|--------|
| 沒有 smoke test，部署看起來沒問題 | 「看起來沒問題」不是證據；smoke test 是最低可行確認；沒有 smoke test 就沒有部署成功的紀錄 |
| dry-run 結果是 PASS，就等於真實部署會成功 | dry-run 是近似值，不是保證；在 deploy.md 中明確記錄 `deploy_mode: "dry-run"`，不要混淆 |
| 部署失敗了，我自動 rollback | Rollback 是不可逆操作；必須先向用戶報告失敗，取得明確授權後才執行 rollback |

## Completion Report

Report status using exactly one of:
- **DONE** — artifact deployed; smoke tests PASS; `deploy.md` committed. Ready for `/s7-release-notes`.
- **DONE_DRY_RUN** — simulation complete; `deploy.md` committed with `deploy_mode: "dry-run"`. Ready for `/s7-release-notes`.
- **BLOCKED** — deploy failed or smoke test failed; list specific failure and recommend rollback decision to user.
- **NEEDS_CONTEXT** — no deploy target defined and dry-run not confirmed; ask user which mode to use.

</what-to-do>

<supporting-info>

## Role Identity: Release Manager (Deploy Phase)
- **Mindset**: Deployment accountant. Every action is logged. No deploy is "done" until smoke tests confirm it.
- **Upstream Dependency**: `/s7-build-artifact` — artifact path and SHA-256 are required inputs.
- **Downstream Target**: `/s7-release-notes` reads the deploy log to confirm what version was shipped.

## Eval Fixtures

Fixtures 位於 `tests/fixtures/s7-deploy/cases.json`。

每個 fixture 包含：`scenario`（情境描述）、`input`（輸入物件）、`expected_behavior`（預期行為）。

冒煙測試：逐一確認 skill 對每個情境的輸出結構與 expected_behavior 一致。

## Artifact Dependencies
- **Reads**: `dist/<artifact>` or Docker image; `test-results.json` (for smoke test targets)
- **Writes**: `docs/releases/YYYY-MM-DD-<version>-deploy.md`

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

</supporting-info>
