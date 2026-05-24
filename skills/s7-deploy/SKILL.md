---
name: s7-deploy
description: >
  Use when deploying versioned artifact to target environment and confirming with smoke tests.
  Outputs deploy.md. NOT for building artifacts.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s7-deploy`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

---

Do NOT proceed if:
1. Artifact from `/s7-build-artifact` is not available (no `dist/` or Docker image).
2. No deploy target defined AND `dry-run` mode not explicitly selected.

After writing `docs/releases/YYYY-MM-DD-<version>-deploy.md`, proceed immediately to `/s7-release-notes`.
Do NOT skip `/s7-release-notes`'s HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in deployment phase. Task: deploy versioned artifact and confirm stability via smoke tests.

## Deploy Mode Selection

Ask the user if unclear.

| Mode | When | deploy_mode field |
|---|---|---|
| `live` | Real target available (k8s, fly.io, Docker registry, PyPI) | `"live"` |
| `dry-run` | No real target (trial, CI preview, local validation) | `"dry-run"` |
| `gitops` | Team uses ArgoCD/Flux; deploy = PR merge to main, CD auto-triggers | `"gitops"` |

**GitOps**: "deploy" = merge PR to `main`. No manual `kubectl apply` or `fly deploy`. Wait for ArgoCD sync / Flux reconcile before smoke tests.

In dry-run, simulate every step. Never attempt real deploy without explicit user confirmation.

## Workflow

### Step 1 — Confirm Artifact

Verify: **Python** `ls -lh dist/` OR **Docker** `docker images | grep <name>`

Record artifact path and SHA-256.

### Step 2 — Deploy

#### Live Mode

- **PyPI**: `twine upload dist/*`
- **Docker**: `flyctl deploy --image <name>:<version>`
- **k8s**: `kubectl set image deployment/<name> <container>=<image>:<version>` && `kubectl rollout status`
- **npm**: `npm publish`

#### Dry-Run Mode

- **Wheel**: `pip install dist/<name>-<version>-*.whl` (local, safe)
- **Docker**: `docker build -t <name>:<version> . --no-cache`

Record commands with `[DRY-RUN]` prefix.

### Step 3 — Smoke Tests

Run immediately after deploy:

- **Python library**: `python -c "import <module>; print(<module>.__version__)"`
- **API service**: `curl -s http://localhost:<port>/health | jq .status`
- **Key function**: `python -c "from module import func; print(func('test'))"`

Each must produce PASS/FAIL.

### Step 4 — Write Deploy Log

Write to `docs/releases/YYYY-MM-DD-<version>-deploy.md` using template at `references/deploy-log-template.md`.

Commit:
```bash
git add docs/releases/YYYY-MM-DD-<version>-deploy.md
git commit -m "release(v<version>): add deploy log"
```

---

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| No smoke test, deploy looks OK | "Looks OK" ≠ evidence; smoke tests = minimum proof; no smoke tests = no success record |
| dry-run PASS = real deploy will succeed | dry-run is approximation, not guarantee; mark `deploy_mode: "dry-run"` in deploy.md |
| Deploy failed, I'll auto-rollback | Rollback is irreversible; must report failure & get explicit user approval |

---

## Completion Report

- **DONE** — artifact deployed; smoke tests PASS; `deploy.md` committed. Ready for `/s7-release-notes`.
- **DONE_DRY_RUN** — simulation complete; `deploy.md` committed with `deploy_mode: "dry-run"`. Ready for `/s7-release-notes`.
- **BLOCKED** — deploy/smoke test failed; list specific failure; recommend rollback decision.
- **NEEDS_CONTEXT** — no deploy target and dry-run not confirmed; ask which mode.

</what-to-do>

<supporting-info>
**Reads**: dist/<artifact> or Docker image; test-results.json
**Writes**: docs/releases/YYYY-MM-DD-<version>-deploy.md
→ Full reference: `references/detail.md`
</supporting-info>
