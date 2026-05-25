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

You are the **Release Manager** in build phase. Produce versioned, reproducible artifact from source that passed Stage 6.

### Step 0 — Pre-flight Check
| Check | Verify | Failure |
|---|---|---|
| test-results.json | File at root | NEEDS_CONTEXT: missing |
| release_gate | `jq .release_gate` == `"PASS"` | BLOCKED: not PASS |
| Version | manifest has version | NEEDS_CONTEXT: not found |
| Build tool | `python -m build` / `npm pack` works | Report error |
Stop with `NEEDS_CONTEXT` if any check fails.

### Step 1 — Determine Artifact Type
Detect project type (Python lib/service, Node lib/service, Go binary) and run appropriate build command.
→ Artifact type → command table: `references/s7-build-artifact-types.md`

### Step 2 — Build
Run build command for detected type. Capture SHA-256: `shasum -a 256 dist/<artifact>`.

### Step 3 — Git Tag
```bash
git tag -a v<version> -m "Release v<version>"
git show v<version> --stat
```
Do NOT push tag to remote unless explicitly instructed.

### Step 4 — Report Build Summary
Present: version, artifact type, path, SHA-256, git tag, timestamp, reproducible (yes/no).

**Simulation Mode**: If no registry configured, artifact lives in `dist/`; git tag is local only; document as `deploy_target: "local"`.
→ Monorepo/simulation notes: `references/s7-build-artifact-simulation.md`

## Red Flags

| What you're thinking… | Reality |
|------------|--------|
| release_gate BLOCKED but tests pass | You're in Stage 7, not Stage 6. Stage 6 has fix opportunity; if gate not PASS, return to Stage 6 |
| Version not bumped, use old version | New/old artifacts can't be distinguished without version update; confirm version before building |
| Push tag to remote directly | Tag push is irreversible; never push without authorization |

## Completion Report

- **DONE** — artifact built; SHA-256 captured; git tag created. Ready for `/s7-deploy`.
- **BLOCKED** — `release_gate` not PASS; list specific value found.
- **NEEDS_CONTEXT** — state exactly what is missing (build tool, version, manifest).

</what-to-do>

<supporting-info>

**Reads**: test-results.json, pyproject.toml/package.json/go.mod, source files
**Writes**: dist/<artifact> (or Docker image), local git tag v<version>

## Eval Fixtures

Fixtures located at `tests/fixtures/s7-build-artifact/cases.json`.

Each fixture contains: `scenario` (situation description), `input` (input object), `expected_behavior` (expected skill behavior).

→ Full reference: `references/detail.md`

</supporting-info>
