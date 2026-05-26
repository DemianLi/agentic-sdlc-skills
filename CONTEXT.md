# Agentic Skill System

This context defines the ubiquitous language for the Agentic Software Development Lifecycle (SDLC) framework. The core pipeline has 7 sequential stages (Foundation Engineer → Release Manager); five standalone skills (Stage 0) operate outside the pipeline and may be used at any time. It establishes how AI Agents are directed through different phases of software development using specialized, atomic instructions.

## Language

**Stage**:
One of the 7 sequential phases of the Agentic SDLC pipeline (Foundation Engineer → Release Manager). Stage 0 is a special label for standalone skills that exist outside the pipeline.
*Avoid*: Phase, Step, Level

**Role**:
The specific persona an AI Agent assumes to execute a given Stage. There is a strict 1-to-1 mapping between a Role and a Stage (e.g., Stage 1 is always executed by the Foundation Engineer).
*Avoid*: Agent, Persona, Actor

**Skill**:
A discrete, atomic Markdown file containing instructions for a specific Role to accomplish a specific task within a Stage.
*Avoid*: Prompt, Command, Script

**Slash Command**:
The user-facing trigger for a Skill, following the naming convention `/s{StageNumber}-{Action}` (e.g., `/s4-tdd`, `/s0-trace-feature`). Stage 0 commands use `/s0-` prefix and are standalone — not part of the sequential pipeline.
*Avoid*: Trigger, Command Line, Input

**Standalone Skill**:
A Skill with the `/s0-` prefix that operates outside the s1–s7 pipeline. It produces an artifact that may optionally feed into the pipeline but is never a required gate. Current standalone skills: `/s0-grill`, `/s0-grill-docs`, `/s0-trace-feature`, `/s0-eval-skill`, `/s0-eval-alignment`, `/s0-skill-budget`, `/s0-semantic-validate`.
*Avoid*: Pre-stage skill, utility skill

**OpenSpec**:
The highly rigorous specification document format produced in Stage 3, serving as the absolute single source of truth (Source of Truth) for Stage 4's Test-Driven Development (TDD).
*Avoid*: PRD, Design Doc, Requirements

**Atomic Task**:
A functionally independent, minimal unit of work derived from the technical design in Stage 3, suitable for concurrent implementation in Stage 4.
*Avoid*: Ticket, Issue, Story

## Relationships

- A **Stage** requires exactly one **Role** to execute it.
- A **Role** possesses multiple atomic **Skills**.
- A **Skill** is invoked via exactly one **Slash Command**.
- The **OpenSpec** dictates the acceptable outcomes for an **Atomic Task**.
- A **Standalone Skill** has no upstream gate and no downstream requirement; its artifact is optional input to a pipeline stage.

## Example dialogue

> **Dev:** "I need the Agent to write tests for this new feature."
> **Architect:** "You can't jump straight to the `/s4-tdd` **Slash Command**. The **Role** for Stage 4 needs the **OpenSpec** first. Run `/s3-breakdown` to generate the **Atomic Tasks** and specs."

**Development Mode**:
The rigor level applied during a `/s-fast-track` session. Three variants exist: Standard (default), Vibe Mode, and Hotfix Mode. Activated by intent signals in the task description. Mode signal overrides task-type routing.
*Avoid*: Mode flag, rigor level, fast-track variant

**Vibe Mode**:
A Development Mode for exploratory, throwaway prototypes. Bypasses TDD ceremony (routes directly to `/s4-impl-task`); s5 review is skipped. Requires explicit user confirmation (Y/n) and `[WIP/Prototype]` commit tagging on every commit.
*Avoid*: Prototype mode, skip-test mode

**Hotfix Mode**:
A Development Mode for fixes on legacy or low-test-coverage codebases. TDD Iron Law is preserved; s5 review runs in a simplified form (CRITICAL issues remain blocking; WARNING items are informational only). Faster than Standard but not discipline-free.
*Avoid*: Quick-fix mode, brownfield mode

**Skill Index**:
The declarative YAML file (`schemas/SKILL_INDEX.yaml`) that maps trigger keywords to skill names, enabling O(1) routing without semantic inference. Each keyword maps to exactly one skill (strict mutual exclusion). Used by `/s-fast-track` for direct lookup and by `/s0-skill-budget` for I-axis coverage checks. Maintained alongside the Skill Graph — every new or renamed skill requires an update to both files.
*Avoid*: Keyword map, routing table, skill lookup

**Token Budget Audit**:
The three-axis evaluation performed by `/s0-skill-budget` on any SKILL.md before it is merged. Axis D checks description precision (≤40 tokens, `Use when` trigger, `NOT` exclusion clause, no process verbs). Axis I checks Skill Index coverage (skill name present, ≥2 keywords, mutual exclusion). Axis S checks size budget (≤10 KB, no section >50 lines, referenced files exist). A skill must reach Overall PASS or PARTIAL before being considered production-ready from a token-efficiency standpoint.
*Avoid*: Token check, budget review, efficiency audit

**Skill Graph**:
The declarative YAML file (`schemas/skill_graph_schema.yaml`) that encodes all skill dependencies. Each node declares its `stage`, `requires` (upstream skills that must complete first), and `outputs` (glob-matchable artifact paths used to detect completion). The graph is acyclic; `SkillGraphEngine` validates this on initialization.
*Avoid*: Dependency map, skill tree, pipeline config

**SkillGraphEngine**:
The Python runtime (`skills/s0-eval-alignment/scripts/engine.py`) that loads the Skill Graph, performs topological sorting, detects dependency cycles, and computes `completed`, `next`, and `blocked` node sets. Exposes a CLI and a Python API. Operates in `fluid` mode (default) or `strict` mode.
*Avoid*: Graph runner, topology checker

**Fluid Mode**:
The default `SkillGraphEngine` navigation mode. Completion is determined purely by filesystem presence of declared `outputs` (or sentinel files). Skills whose upstream dependencies were skipped are reported as advisory catch-up suggestions rather than hard blockers.
*Avoid*: Soft mode, advisory mode

**Strict Mode**:
A `SkillGraphEngine` navigation mode where a skill is only counted as completed if every transitive upstream dependency is also completed. Used when sequential pipeline enforcement is required.
*Avoid*: Hard mode, sequential mode

**Sentinel File**:
A zero-byte marker file named `.{skill-name}.done` (e.g., `.s4-setup-env.done`) placed in the workspace root to signal completion for skills that declare no `outputs` in the Skill Graph schema (typically environment-setup or configuration skills).
*Avoid*: Done file, completion marker

## Flagged ambiguities

- "Agent" vs "Role" — resolved: An "Agent" is the underlying AI model (e.g., Claude, Gemini). A "Role" is the specific hat the Agent wears (e.g., Foundation Engineer) when executing a Skill.
