# Agentic SDLC Skills

32 atomic Skill files that drive an AI Agent through a structured, gated Software Development Lifecycle. The core pipeline is 7 stages (Foundation → Release); four standalone Stage 0 skills operate outside the pipeline and can be used at any time. Each Skill is a Markdown file that defines a Role, a Workflow, and a HARD-GATE — a mandatory stop that blocks the Agent from proceeding until explicit human approval is given.

---

## Why this exists

AI Agents are fast but undisciplined. Left ungated, they will:
- Jump from requirements directly to code, skipping impact analysis
- Write production code before writing failing tests
- Self-approve quality gates and push to production

This Skill system forces the Agent to work the same way a senior engineering team does: produce an artifact, present it, stop, wait for a human to approve, then proceed.

---

## Stage 0 — Standalone Skills (use any time)

Four skills operate outside the s1–s7 pipeline. They produce artifacts that can optionally feed into the pipeline but do not block or gate it.

| Slash Command | Purpose | Optional output feeds into |
|---|---|---|
| `/s0-brainstorm` | Explore a problem space; produce a framed problem statement | `/s2-capture-vision` |
| `/s0-trace-feature` | Trace an existing feature's call chain; produce a Mermaid sequence diagram | `/s3-eval-system` or `/s2-capture-vision` |
| `/s0-eval-skill` | Audit a single skill against 6 structural quality criteria; output a scored report | Skill author fixes drift |
| `/s0-eval-alignment` | Batch-scan all 28 s1–s7 skills against QA.md design intent; detect drift before it compounds | Maintainer applies fixes |

---

## The 7-Stage Pipeline

```
Stage 1              Stage 2              Stage 3              Stage 4
Foundation        →  Product           →  System            →  Implementer
Engineer             Manager              Architect
RULES.md             vision.md            design.md            Code + tests
CONTEXT.md           alignment.md         wbs.md               TASK_DAG [x]
<tech lock>          requirements.md      TASK_DAG.md
                     CONTEXT_SNAPSHOT.md

Stage 5              Stage 6              Stage 7
Code Auditor      →  QA Engineer       →  Release Manager
SAST report          test-results.json    Artifact + tag
Audit report         Integration pass     CHANGELOG.md
PR review            E2E pass             Telemetry report
```

Each arrow is a **Handoff** — a set of committed artifacts that must exist before the next Stage begins. See `HANDOFF.md` for the complete acceptance criteria.

---

## The 32 Skills

| Stage | Role | Slash Command | Purpose |
|---|---|---|---|
| 0 *(standalone)* | Problem Scout | `/s0-brainstorm` | Explore problem space; produce framed problem statement |
| 0 *(standalone)* | Code Archaeologist | `/s0-trace-feature` | Trace existing feature call chain; produce Mermaid sequence diagram |
| 0 *(standalone)* | Skill Auditor | `/s0-eval-skill` | Audit single skill against 6 structural quality criteria |
| 0 *(standalone)* | Alignment Inspector | `/s0-eval-alignment` | Batch-scan all s1–s7 skills for design-intent drift |
| 1 | Foundation Engineer | `/s1-define-rules` | Author `RULES.md` (linter, directory, forbidden patterns) |
| 1 | Foundation Engineer | `/s1-config-context` | Author domain glossary `CONTEXT.md` |
| 1 | Foundation Engineer | `/s1-lock-tech-stack` | Pin runtime + framework versions; generate lock files |
| 1 | Foundation Engineer | `/s1-git-guardrails` | Configure git hooks, branch protection, and commit conventions |
| 2 | Product Manager | `/s2-capture-vision` | Elicit problem statement, target users, proposed approach |
| 2 | Product Manager | `/s2-align-req` | Resolve stakeholder conflicts, define scope boundary |
| 2 | Product Manager | `/s2-struct-req` | Write structured requirements with binary Acceptance Criteria |
| 2 | Product Manager | `/s2-snapshot-ctx` | Produce `CONTEXT_SNAPSHOT.md` (iteration seed for Stage 3) |
| 3 | System Architect | `/s3-eval-system` | Scan codebase, classify blast radius (🔴/🟡/🟢), write impact report |
| 3 | System Architect | `/s3-design-arch` | Author OpenSpec design doc with Mermaid sequence diagrams |
| 3 | System Architect | `/s3-breakdown-wbs` | Decompose design into Atomic Tasks (≤5 min each) |
| 3 | System Architect | `/s3-build-dag` | Build dependency DAG, identify critical path, write `TASK_DAG.md` |
| 4 | Implementer | `/s4-setup-env` | Select task from DAG, set up branch + runtime environment |
| 4 | Implementer | `/s4-tdd` | RED → GREEN → REFACTOR (Iron Law: no production code without a failing test) |
| 4 | Implementer | `/s4-impl-task` | Implement one Atomic Task to GREEN |
| 4 | Implementer | `/s4-local-debug` | Reproduce → minimise → hypothesise → instrument → fix → regression-test |
| 5 | Code Auditor | `/s5-sast-lint` | Run SAST + linter, flag CRITICAL violations |
| 5 | Code Auditor | `/s5-audit-rules` | Validate architecture against `RULES.md` constraints |
| 5 | Code Auditor | `/s5-pr-review` | Scope drift detection, severity classification (CRITICAL/WARNING/SUGGESTION) |
| 5 | Code Auditor | `/s5-fix-optimize` | Auto-fix CRITICAL issues; performance optimisations |
| 6 | QA Engineer | `/s6-test-integration` | Run integration tests; verify all critical paths pass |
| 6 | QA Engineer | `/s6-test-e2e` | Run Playwright/Cypress; verify main user flows |
| 6 | QA Engineer | `/s6-test-perf` | Run k6/Artillery; capture P50/P95/P99; regression gate (20%) |
| 6 | QA Engineer | `/s6-verify-release` | Run full suite; write `test-results.json`; issue PASS or BLOCKED |
| 7 | Release Manager | `/s7-build-artifact` | Build, tag, and sign the release artifact |
| 7 | Release Manager | `/s7-release-notes` | Generate `CHANGELOG.md` following Keep a Changelog format |
| 7 | Release Manager | `/s7-deploy` | Deploy → monitor → verify (canary-aware) |
| 7 | Release Manager | `/s7-telemetry` | Capture 24h metrics; compare to S6 baseline; feed back to Stage 2 |

---

## HARD-GATE Enforcement

Every Skill contains a `<HARD-GATE>` block that specifies the conditions that must be true **before** the Agent proceeds. After meeting those conditions and presenting the required artifact, the Agent's message **must** end with:

> *"Awaiting your approval to proceed to \<next-skill\>."*

The Agent may not generate the next stage's artifact, code, or analysis until the human explicitly approves. A response that is silent on approval is **not** approval.

### What the HARD-GATE prevents (examples)

| Skill | What it blocks without evidence |
|---|---|
| `s1-lock-tech-stack` | Generating lock files before recording the actual `python --version` output |
| `s3-eval-system` | Proceeding to design before the impact report is written to disk and committed |
| `s4-tdd` | Writing production code before pasting actual `pytest FAILED` terminal output |
| `s6-verify-release` | Issuing "Ready" signal before `test-results.json` is machine-generated and committed |

---

## How to install

Skills are plain Markdown files. Copy them into your Claude Code project as slash commands.

**Option A — project-local (recommended):**
```bash
# In your project root
mkdir -p .claude/skills
cp -r skills/s4-tdd .claude/skills/
```
Then invoke with `/s4-tdd` inside that project's Claude Code session.

**Option B — global:**
```bash
cp -r skills/* ~/.claude/skills/
```
Available in all Claude Code sessions.

---

## Using a Skill

1. Start Claude Code in your project directory
2. Type the slash command, e.g. `/s3-eval-system`
3. The Agent assumes the Role, runs the Workflow, produces the artifact
4. The Agent stops and says *"Awaiting your approval…"*
5. Review the artifact; type your approval (e.g. "approved, proceed")
6. Move to the next Skill

---

## Repository structure

```
skills/
  s0-brainstorm/        Problem Scout — framed problem statement
  s0-trace-feature/     Code Archaeologist — feature call-chain diagram
  s0-eval-skill/        Skill Auditor — single-skill structural quality check
  s0-eval-alignment/    Alignment Inspector — batch drift detection (28 skills)
    references/         skill-design-intent.md (evaluation baseline)
    scripts/scan.py     Reusable CLI scanner (exit 0 = all ALIGNED)
    tests/              Smoke-test fixtures + pytest suite
  s1-*/SKILL.md         Stage 1 — Foundation Engineer (4 skills)
  s2-*/SKILL.md         Stage 2 — Product Manager (4 skills)
  s3-*/SKILL.md         Stage 3 — System Architect (4 skills)
  s4-*/SKILL.md         Stage 4 — Implementer (4 skills)
  s5-*/SKILL.md         Stage 5 — Code Auditor (4 skills)
  s6-*/SKILL.md         Stage 6 — QA Engineer (4 skills)
  s7-*/SKILL.md         Stage 7 — Release Manager (4 skills)
docs/
  skill-evals/          Alignment scan reports (YYYY-MM-DD-alignment-scan.md)
  TRIALS_INDEX.md       Index of all research trials (07–16) with hypotheses and results
  TRIAL_*_REPORT.md     Individual trial reports
  BENCHMARK_REFERENCE.md  Design analysis of 4 reference repos
.github/workflows/
  alignment.yml         CI gate — runs smoke tests + alignment scan on skills/** changes
CONTEXT.md              Domain glossary and ubiquitous language
HANDOFF.md              Artifact pipeline and acceptance criteria between stages
QA.md                   28-step SDLC quality checklist (design intent source of truth)
```

> **Branches**: `main` contains skills and docs only. `research` branch additionally contains `test_projects/` — 10 trial runs (07–16) with full source, tests, and build artifacts.

---

## Skill anatomy

Each `SKILL.md` has four sections:

```
---
name: <skill-name>
description: <one-line summary>
---

<HARD-GATE>          ← blocking conditions + OUTPUT DISCIPLINE clause
</HARD-GATE>

<what-to-do>         ← Role identity + step-by-step Workflow + Completion Report
</what-to-do>

<supporting-info>    ← Process Flow (Graphviz DOT), Artifact Standard
</supporting-info>
```

---

## Design principles

- **Artifact-first** — every Stage produces a committed file, not just a conversation
- **Vertical slice** — Stage 4 implements one behavior at a time (RED → GREEN → REFACTOR)
- **Human-in-the-loop** — every Stage gate requires explicit approval before proceeding
- **Evidence over assertion** — the Agent must paste actual terminal output, not claim success
- **Blocked handoffs escalate backward** — if an artifact is missing, the Agent reports `NEEDS_CONTEXT` and halts; it never infers forward
- **Description as trigger, not summary** *(Matt Pocock principle)* — every skill's `description` field states only *when* to use it; no workflow steps are summarised there, so the Agent always reads the full `<what-to-do>` body

---

## Alignment tooling

Run the scanner at any time to verify that all skills still match their original design intent:

```bash
# Full scan — console output
python3 skills/s0-eval-alignment/scripts/scan.py

# Single stage
python3 skills/s0-eval-alignment/scripts/scan.py --stage s6

# Write dated report to docs/skill-evals/
python3 skills/s0-eval-alignment/scripts/scan.py --write
```

The scanner checks four dimensions per skill:

| Check | What it verifies |
|-------|-----------------|
| **Q** — QA.md alignment | ≥ 3 design-intent keywords present in skill body |
| **C1** — HARD-GATE | `<HARD-GATE>` block exists; ends with "Awaiting your approval" |
| **C2** — Artifact chain | `<supporting-info>` declares explicit **Reads** and **Writes** |
| **C3** — Matt Pocock | `description` contains no workflow steps or process verbs |

Exits `0` if all skills are ALIGNED; exits `1` if any are PARTIAL or DRIFTED (CI-friendly).

### CI enforcement

A GitHub Actions workflow (`.github/workflows/alignment.yml`) runs automatically on every PR and push that touches `skills/**`:

1. **Smoke tests** — `pytest skills/s0-eval-alignment/tests/ -v` (fixture-aligned + fixture-drifted)
2. **Alignment scan** — `python3 skills/s0-eval-alignment/scripts/scan.py` (exits 1 → blocks merge if any skill drifts)
3. **Dated report** — on push to `main`, writes `docs/skill-evals/YYYY-MM-DD-alignment-scan.md` and uploads as a GitHub Actions artifact

To run the smoke tests locally:

```bash
pip install pytest
pytest skills/s0-eval-alignment/tests/ -v
```

---

## Completion status vocabulary

Every Skill ends with exactly one of:

| Status | Meaning |
|---|---|
| `DONE` | Artifact produced, committed, user approved |
| `DONE_WITH_CONCERNS` | Done, but specific concerns listed that may affect next stage |
| `BLOCKED` | Cannot proceed; exact blocker stated; fix required before retry |
| `NEEDS_CONTEXT` | Missing upstream artifact; halting until provided |
