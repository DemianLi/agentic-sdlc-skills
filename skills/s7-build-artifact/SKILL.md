---
name: s7-build-artifact
description: >
  Use when building and tagging deployable artifact after Stage 6 verification passes.
  Outputs artifact + SHA-256 + git tag. NOT for testing or verification.
---

<HARD-GATE>
## Step 0 — Prerequisite Check (run before anything else)
Run: `python skills/s0-eval-alignment/scripts/engine.py --check-prereqs --for s7-build-artifact`
If it reports any missing prerequisite, follow its suggestion and **STOP**.

If prerequisites pass but `test-results.json` has `release_gate` ≠ `"PASS"` →
NEEDS_CONTEXT: "test-results.json exists but release_gate is not PASS. Stage 6 is incomplete — return to /s6-verify-release."

---

After presenting build summary, proceed immediately to /s7-deploy.
Do NOT skip /s7-deploy's HARD-GATE conditions.
</HARD-GATE>

<what-to-do>

You are the **Release Manager** in build phase. Task: produce versioned, reproducible artifact from source that passed Stage 6.

## Pre-flight Check

Stop with `NEEDS_CONTEXT` if any check fails.

| Check | Verify | Failure |
|---|---|---|
| test-results.json | File at root | NEEDS_CONTEXT: missing |
| release_gate | `jq .release_gate` == `"PASS"` | BLOCKED: not PASS |
| Version | manifest has version | NEEDS_CONTEXT: not found |
| Build tool | `python -m build` / `npm pack` works | Report error |

## Workflow

### Step 1 — Determine Artifact Type

| Project type | Artifact | Command |
|---|---|---|
| Python library | `.whl` + `.tar.gz` | `python -m build` |
| Python service | Docker image | `docker build -t <name>:<version> .` |
| Node library | `.tgz` | `npm pack` |
| Node service | Docker image | `docker build -t <name>:<version> .` |
| Go binary | Binary | `go build -o dist/<name> .` |

If `Dockerfile` present, prefer Docker for services.

### Step 2 — Build

**Python**: `pip install build && python -m build` (outputs to dist/)

**Capture SHA-256**: `shasum -a 256 dist/<artifact>`

### Step 3 — Git Tag

```bash
git tag -a v<version> -m "Release v<version>"
git show v<version> --stat
```

Do NOT push tag to remote unless explicitly instructed.

### Step 4 — Report Build Summary

Present: version, artifact type, path, SHA-256, git tag, timestamp, reproducible (yes/no).

---

## Simulation Mode

If no registry configured (trial context), artifact lives in `dist/` and git tag is local only. Document as `deploy_target: "local"`.

Do NOT push to PyPI / Docker Hub / npm unless explicitly instructed.

**Monorepo caveat**: If trial project in larger repo subdirectory, `git tag` tags monorepo root, not trial project. Skip git tag step; note `git_tag: "skipped (monorepo context)"`. Git tags only make sense when repo root = project root.

---

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| release_gate BLOCKED but tests pass | You're in Stage 7, not Stage 6. Stage 6 has fix opportunity; if gate not PASS, return to Stage 6 |
| Version not bumped, use old version | New/old artifacts can't be distinguished without version update; confirm version before building |
| Push tag to remote directly | Tag push is irreversible; never push without authorization |

---

## Completion Report

- **DONE** — artifact built; SHA-256 captured; git tag created. Ready for `/s7-deploy`.
- **BLOCKED** — `release_gate` not PASS; list specific value found.
- **NEEDS_CONTEXT** — state exactly what is missing (build tool, version, manifest).

</what-to-do>

<supporting-info>

**Reads**: test-results.json, pyproject.toml/package.json/go.mod, source files
**Writes**: dist/<artifact> (or Docker image), local git tag v<version>

→ Full reference: `references/detail.md`

</supporting-info>
