# TRIAL-15 Design: HARD-GATE Enforcement Validation

**Date**: 2026-05-16
**Status**: DESIGN (awaiting user approval before execution)
**Objective**: Validate that HARD-GATEs genuinely block forward progression — each downstream stage starts cold from committed artifacts only.

---

## Why Trial-15 Exists

Trial-14 DONE_WITH_CONCERNS: every gate was bypassed in a single continuous agent session. The assistant had all previous context in memory, so "chain health" was trivially satisfied without actually testing isolation.

Trial-15 tests the corrected protocol: **sub-agent isolation per stage**.

---

## Execution Protocol (non-negotiable)

### Orchestrator Role

The main session (this conversation) is the **orchestrator only**. It:
- Creates s1+s2 artifacts directly (small enough to not need a sub-agent)
- Spawns one sub-agent per gated stage
- **STOPS after each sub-agent and waits for explicit user approval before spawning the next**
- Reports findings, does not write code

### Sub-Agent Rule

Each sub-agent prompt contains ONLY:
- The stage goal (one sentence)
- Absolute paths to upstream artifacts
- "Do not ask the user questions — if information is missing from the artifacts, report what's missing and stop"

**Forbidden in sub-agent prompts**: summaries of previous stages, descriptions of the domain, explanations of what the upstream artifacts contain. The sub-agent must derive everything from the files themselves.

### Gate Enforcement

After each sub-agent completes, the orchestrator:
1. Reports result to user
2. Writes "Awaiting your approval to proceed to s[N+1]"
3. **Stops. Does not spawn the next sub-agent in the same response.**
4. Waits for explicit user message before continuing

A silent user response or a follow-up unrelated message does NOT constitute approval.

### Expected Negative Findings

If a sub-agent cannot proceed from the upstream artifacts alone — it's missing required information — that is a **positive research finding**, not a failure. It means the artifact specification for that stage is incomplete. Record it verbatim in the trial report.

---

## Scope: 3 Gate Boundaries

Full s1→s7 is trial-16. Trial-15 tests 3 representative boundaries:

| Gate | Upstream → Downstream | Why this boundary |
|---|---|---|
| Gate 1 | s2 → s3 | Requirements → Design: highest info density, most inference required |
| Gate 2 | s3 → s4 | Design → TDD: sub-agent must write tests from API contracts alone |
| Gate 3 | s6 → s7 | Test results → Release: HARD-GATE on `release_gate` field |

Stages s4→s5→s6 (between Gate 2 and Gate 3): orchestrator produces artifacts directly (non-isolated, not part of gate test).

---

## Problem Domain

**`slugify` CLI** — URL slug generator. Smaller than mdtoc, no overlap with trial-14.

Why: simple enough that a cold-start sub-agent can complete a stage in one pass; complex enough to have non-trivial API contracts and testable behavior.

### Requirements (pre-written by orchestrator)

- **REQ-1** `slugify(text, separator="-") → str` — lowercase, spaces→separator, strip `[^a-z0-9<sep>]`
- **REQ-2** CLI: `python -m slugify [TEXT]` → stdout. If TEXT missing, read from stdin
- **REQ-3** `--separator SEP` flag (default `-`)
- **REQ-4** Exit 0 on success; exit 1 on empty input after stripping

4 requirements, 8 acceptance criteria (2 per REQ).

---

## Artifacts Layout

```
test_projects/trial-15-gates/
├── CONTEXT.md                              # orchestrator writes (s1)
├── docs/
│   ├── specs/
│   │   └── 2026-05-16-slugify-requirements.md   # orchestrator writes (s2)
│   ├── arch/
│   │   ├── 2026-05-16-slugify-design.md         # Gate 1 sub-agent writes (s3)
│   │   └── 2026-05-16-slugify-wbs.md            # Gate 1 sub-agent writes (s3)
│   ├── audit/
│   │   └── 2026-05-16-pr-review.md              # orchestrator writes (s5, non-gated)
│   └── tests/
│       ├── 2026-05-16-test-results.json         # orchestrator writes (s6, non-gated)
│       └── 2026-05-16-perf-baseline.json        # orchestrator writes (s6, non-gated)
├── src/slugify/
│   ├── __init__.py
│   ├── core.py
│   └── __main__.py
├── tests/
│   ├── test_core.py                         # Gate 2 sub-agent writes (s4)
│   └── test_cli.py                          # Gate 2 sub-agent writes (s4)
└── pyproject.toml
```

---

## PASS Criteria

| Gate | Criterion | Measurement |
|---|---|---|
| Gate 1 | s3 sub-agent produces design.md + wbs.md from requirements.md only | Verify design sections map to REQ-N blocks; no information not in requirements.md |
| Gate 1 | s3 sub-agent did NOT ask user for clarification | Check sub-agent output for questions |
| Gate 2 | s4 sub-agent produces failing tests BEFORE seeing any implementation | Verify test stubs reference function signatures from design.md API contracts |
| Gate 2 | s4 sub-agent implements code until all tests pass | 22+ tests green |
| Gate 3 | s7 sub-agent reads `release_gate` from test-results.json and blocks if FAIL | Verify s7 checks the field; would block on FAIL |
| ALL | Gate stop enforced between each | User explicitly approved each transition in this session |

---

## Sub-Agent Prompt Templates

### Gate 1 — s3 sub-agent prompt

```
Read /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/docs/specs/2026-05-16-slugify-requirements.md

Execute the s3-design-arch + s3-breakdown-wbs skills for this project:
- Write docs/arch/2026-05-16-slugify-design.md with: Context, Decision, Data Structures, API Contracts, Sequence Diagram, Consequences
- Write docs/arch/2026-05-16-slugify-wbs.md with implementation tasks

Rules:
- Derive everything from the requirements file. Do not use information not in that file.
- If a requirement is ambiguous, document the ambiguity in a "Design Decisions" section and choose the simplest interpretation.
- Do not ask the user questions. If something is truly unresolvable, write "BLOCKED: <reason>" in the relevant section and stop.
- Working directory: /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/
```

### Gate 2 — s4 sub-agent prompt

```
Read these two files:
- /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/docs/arch/2026-05-16-slugify-design.md
- /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/docs/arch/2026-05-16-slugify-wbs.md

Execute the s4-tdd + s4-impl-task skills:
1. Write tests in tests/test_core.py and tests/test_cli.py from the API contracts in design.md
2. Verify tests fail (ModuleNotFoundError or ImportError)
3. Write implementation in src/slugify/core.py, __init__.py, __main__.py
4. Run tests until all pass

Rules:
- Derive function signatures and behavior from design.md only.
- Do not look at any other project files except the two listed above and the test/src dirs you are creating.
- Do not ask the user questions.
- Working directory: /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/
- Run tests with: PYTHONPATH=src python3 -m pytest tests/ -q
```

### Gate 3 — s7 sub-agent prompt

```
Read these files:
- /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/docs/tests/2026-05-16-test-results.json
- /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/docs/tests/2026-05-16-perf-baseline.json

Execute the s7-build-artifact + s7-deploy + s7-release-notes + s7-telemetry skills:
1. Check release_gate field in test-results.json. If not "PASS", write BLOCKED reason and stop.
2. Build the wheel (dry-run mode): zip src/slugify/ into dist/slugify-1.0.0-py3-none-any.whl
3. Write docs/releases/2026-05-16-v1.0.0-deploy.md
4. Write CHANGELOG.md
5. Write docs/releases/2026-05-16-v1.0.0-telemetry.json using slo-headroom-v1 algorithm

Rules:
- Derive everything from the two JSON files listed above.
- Do not ask the user questions.
- Working directory: /Users/demian/Projects_vibecoding/research_skill_from_github/test_projects/trial-15-gates/
```

---

## What "Validated" Means

Trial-15 is validated if:
1. All 3 sub-agents completed their stage from artifacts alone (no user re-querying)
2. All 3 gate stops were enforced (user explicitly approved each transition)
3. Any negative finding (BLOCKED, missing info) is recorded and counts as valid data

Trial-15 is NOT validated if:
- Any sub-agent prompt contained summaries or context beyond artifact paths
- Any gate was bypassed (orchestrator spawned next stage without user approval)

---

## Approval Required

**Do not proceed to execution without user confirming this design.**

After user approves, orchestrator will:
1. Create `test_projects/trial-15-gates/` scaffold + s1/s2 artifacts
2. Report: "Gate 0 complete. Awaiting approval to spawn s3 sub-agent (Gate 1)."
3. Wait for user approval
4. Spawn Gate 1 sub-agent
5. (repeat for Gates 2 and 3)
