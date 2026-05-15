# Handoff Protocol

> This document defines the **exact artifacts** each Stage must deliver before the next Stage may begin.
> A Stage is NOT complete until every artifact listed in its handoff is committed to git.
> Any downstream Role that receives an incomplete handoff must report `NEEDS_CONTEXT` and halt.

---

## Overview: The 7-Stage Artifact Pipeline

```
Stage 1                Stage 2                Stage 3
Foundation Engineer → Product Manager      → System Architect
RULES.md               vision.md              design.md
CONTEXT.md             alignment.md           wbs.md
<tech stack lock>      requirements.md        TASK_DAG.md
                       CONTEXT_SNAPSHOT.md

Stage 4                Stage 5                Stage 6                Stage 7
Implementer         → Code Auditor         → QA Engineer          → Release Manager
Code + unit tests      SAST report            integration-results    Artifact + tag
TASK_DAG.md updated    Audit report           e2e-results            CHANGELOG.md
                       PR review report       perf-baseline.json     deploy log
                                              test-results.json      telemetry.json
```

---

## s0-brainstorm → Stage 2 (Optional)

**From**: Problem Scout (s0-brainstorm)
**To**: Product Manager (s2-capture-vision) — **user-initiated, not automatic**
**Triggered by**: User explicitly runs `/s2-capture-vision` after reviewing the draft

### Required Artifact (if used)

| Artifact | Path | Required Sections |
|---|---|---|
| Problem statement draft | `docs/brainstorm/YYYY-MM-DD-<topic>-problem-draft.md` | Chosen Problem Framing / Problem Space Map / Rejected Framings / Open Questions / What This Is NOT |

> `s0-brainstorm` is outside the s1–s7 pipeline. Its output is optional input — not a gate — for `/s2-capture-vision`.

---

## Stage 1 → Stage 2 Handoff

**From**: Foundation Engineer
**To**: Product Manager
**Triggered by**: Completion of `/s1-lock-tech-stack`

### Required Artifacts

| Artifact | Path | Required Sections |
|---|---|---|
| Governance rules | `RULES.md` | Linter config / Directory structure / Forbidden patterns |
| Domain glossary | `CONTEXT.md` | Language / AI Boundaries / Skill Routing |
| Dependency lock file | `package.json` / `go.mod` / `requirements.txt` | Pinned exact versions (no `^` or `~`) |
| Stack ADR | `docs/adr/000N-tech-stack.md` | Context / Decision / Consequences |

### Acceptance Criteria for Stage 2 to Begin
- [ ] `RULES.md` exists and has been approved by user
- [ ] `CONTEXT.md` contains the domain glossary with at least the core entities
- [ ] Lock file has no unpinned (`^`, `~`) core framework versions
- [ ] `git status` is clean — all artifacts committed

---

## Stage 2 → Stage 3 Handoff

**From**: Product Manager
**To**: System Architect
**Triggered by**: Completion of `/s2-snapshot-ctx`

### Required Artifacts

| Artifact | Path | Required Sections |
|---|---|---|
| Vision spec | `docs/specs/YYYY-MM-DD-<topic>-vision.md` | Problem Statement / Target Users / Proposed Approach / Out of Scope / Open Questions |
| Alignment doc | `docs/specs/YYYY-MM-DD-<topic>-alignment.md` | Resolved Conflicts / IN Scope / OUT of Scope / Deferred |
| Structured requirements | `docs/specs/YYYY-MM-DD-<topic>-requirements.md` | REQ-N blocks / Test Coverage Map / Scope Contract |
| Context Snapshot | `CONTEXT_SNAPSHOT.md` (project root) | Iteration Goal / Must-Have REQs / Out of Scope / Key Constraints / Forbidden Actions / Source Docs |

### Acceptance Criteria for Stage 3 to Begin
- [ ] `CONTEXT_SNAPSHOT.md` exists at project root with `## Forbidden Actions` section
- [ ] Every REQ-N has at least one Acceptance Criterion with a binary pass/fail condition
- [ ] `## Scope Contract` clearly states IN and OUT of scope
- [ ] All four artifacts committed to git

---

## Stage 3 → Stage 4 Handoff

**From**: System Architect
**To**: Implementer
**Triggered by**: Completion of `/s3-build-dag`

### Required Artifacts

| Artifact | Path | Required Sections |
|---|---|---|
| Impact report | `docs/arch/YYYY-MM-DD-<topic>-impact.md` | Breaking Changes / Additive / Technical Debt / Recommended Approach |
| OpenSpec design | `docs/arch/YYYY-MM-DD-<topic>-design.md` | Context / Decision / Data Structures / API Contracts / Sequence Diagrams / Consequences |
| WBS task list | `docs/arch/YYYY-MM-DD-<topic>-wbs.md` | TASK-N blocks with Input / Output / AC / Estimate / Blocked-by / File Scope |
| Task DAG | `TASK_DAG.md` (project root) | Mermaid graph / Critical Path / Parallel Opportunities / Execution Checklist `[ ]` |

### Acceptance Criteria for Stage 4 to Begin
- [ ] `TASK_DAG.md` has unchecked `[ ]` tasks ready to be implemented
- [ ] Every TASK-N maps to at least one AC-N.M from the requirements doc
- [ ] No task estimated > 5 minutes (code only)
- [ ] DAG has no cycles — confirmed by architect
- [ ] All artifacts committed to git

---

## Stage 4 → Stage 5 Handoff

**From**: Implementer
**To**: Code Auditor
**Triggered by**: Completion of `/s4-local-debug`

### Required Artifacts

| Artifact | Path | Notes |
|---|---|---|
| Implementation code | `<file paths from TASK_DAG.md>` | Only files within declared TASK-N File Scope |
| Unit test files | `*.test.ts` / `*_test.go` / `test_*.py` | One test file per TASK-N |
| Updated TASK_DAG.md | `TASK_DAG.md` | All completed tasks marked `[x]` |

### Acceptance Criteria for Stage 5 to Begin
- [ ] All unit tests pass (`npm test` / `go test ./...` / `pytest` returns 0)
- [ ] No debug logs (`console.log` / `fmt.Printf` added during debug) remain in code
- [ ] Only files within declared File Scope were modified (verify with `git diff --stat`)
- [ ] No TODO/FIXME comments left in implementation code
- [ ] All completed TASK-N items checked `[x]` in `TASK_DAG.md`

---

## Stage 5 → Stage 6 Handoff

**From**: Code Auditor
**To**: QA Engineer
**Triggered by**: Completion of `/s5-fix-optimize`

### Required Artifacts

| Artifact | Path | Required Sections |
|---|---|---|
| SAST/Lint report | `docs/audit/YYYY-MM-DD-<branch>-sast.md` | Status (PASS) / CRITICAL count (0) / Auto-fixed count / Zero Violations list |
| Architecture audit report | `docs/audit/YYYY-MM-DD-<branch>-audit.md` | Layer violations (none) / API contract compliance / Naming compliance |
| PR review report | `docs/audit/YYYY-MM-DD-<branch>-pr-review.md` | Scope Drift (CLEAN) / Overall Status (APPROVED) / No open CRITICAL items |

### Acceptance Criteria for Stage 6 to Begin
- [ ] SAST report has `Status: PASS` (zero CRITICAL issues)
- [ ] PR review report has `Overall Status: APPROVED`
- [ ] Scope Drift is `CLEAN`
- [ ] Full unit test suite still GREEN after Stage 5 fixes
- [ ] All three audit reports committed to `docs/audit/`

---

## Stage 6 → Stage 7 Handoff

**From**: QA Engineer
**To**: Release Manager
**Triggered by**: Completion of `/s6-verify-release`

### Required Artifacts

| Artifact | Path | Required Fields |
|---|---|---|
| Integration test results | `docs/tests/YYYY-MM-DD-integration-results.md` | Summary / Critical Path Coverage / Coverage Early Warning / Failures |
| E2E test results | `docs/tests/YYYY-MM-DD-e2e-results.md` | Summary / AC Traceability / Main Flows / Secondary Flows / Failures |
| Performance baseline | `docs/tests/YYYY-MM-DD-perf-baseline.json` | `slo_gate: "PASS"` / P50/P95/P99 / error_rate / throughput / memory_leak_detected |
| Test results (aggregated) | `test-results.json` (project root) | `release_gate: "PASS"` / unit / integration / e2e objects / traceability array / `blockers: []` |

### Acceptance Criteria for Stage 7 to Begin
- [ ] `test-results.json` exists with `"release_gate": "PASS"`
- [ ] `unit_tests.coverage_pct` ≥ threshold in `RULES.md` (default 80%)
- [ ] `integration_tests.failed === 0`
- [ ] `e2e_tests.failed === 0`
- [ ] `traceability` array covers every AC-N.M from requirements doc
- [ ] `blockers` array is empty

> ⛔ If `release_gate` is not `"PASS"`, Stage 7 is **unconditionally blocked**.

---

## Stage 7 → Next Iteration (Stage 2) Handoff

**From**: Release Manager
**To**: Product Manager (next cycle)
**Triggered by**: Completion of `/s7-telemetry`

### Required Artifacts

| Artifact | Path | Required Sections |
|---|---|---|
| Build artifact | Registry (Docker Hub / npm / GitHub Releases) | Versioned tag, signed, reproducible |
| CHANGELOG | `CHANGELOG.md` | `## [vN.N.N] - YYYY-MM-DD` block / Migration Guide if breaking |
| Deployment log | `docs/releases/YYYY-MM-DD-<version>-deploy.md` | Deploy timestamp / canary metrics / smoke test results / final status |
| Telemetry report | `docs/releases/YYYY-MM-DD-<version>-telemetry.json` | `status` / `metrics` (error_rate / latency P50/P95/P99 / throughput) / `anomalies` / `next_cycle_inputs` / `rollback_triggered` |

### Acceptance Criteria for Iteration Close
- [ ] Artifact published and tagged in registry
- [ ] `CHANGELOG.md` updated and committed
- [ ] Production stable for minimum 24 hours (confirmed in telemetry report)
- [ ] Telemetry report's `next_cycle_inputs` array has been handed to the Product Manager as seed for the next `/s2-capture-vision` session

---

## Quick Reference: Blocked Handoff Escalation

If a Role receives an incomplete handoff:

1. Do NOT attempt to proceed or infer missing artifacts
2. Report: `NEEDS_CONTEXT: <artifact name> missing at <expected path>. Cannot begin Stage N until this is provided.`
3. Tag the upstream Role that must fix it
4. Wait for the artifact to be committed before restarting

> A blocked handoff always escalates to the previous Stage — never forward.
