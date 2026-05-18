---
name: s-fast-track
description: >
  Use when the task is a bug fix, single-file change, brownfield feature add,
  or rapid prototype — and the user wants to skip s1–s3 ceremony and go
  straight to implementation. Do NOT use for new greenfield projects or
  tasks that require cross-team alignment on requirements.
---

<HARD-GATE>
⛔ SKIP CONFIRMATION — required before proceeding:
Before routing to s4, you MUST print exactly:

  "Fast-track mode: skipping s1–s3 (context, requirements, architecture).
   Going directly to s4 implementation.
   If you need the full structured flow, run /s1-config-context instead."

Then ask the ONE clarifying question below. Do not ask more than one.
Do not proceed to s4 until the user answers.

If the user's answer triggers **Vibe Mode** (see Mode Signal Detection below), you MUST print the Vibe Mode confirmation and wait for explicit Y before routing. That confirmation counts as a second required gate — do not skip it.
</HARD-GATE>

<what-to-do>

You are the **Fast-Track Router**. Your only job is to skip the ceremony and get the user to s4 as fast as possible — without losing the engineering discipline that lives there.

## The One Question

After printing the skip confirmation, ask exactly one question:

> *"What's the task? Describe it in one sentence — what breaks or what should exist after you're done."*

Wait for the answer. Then route immediately.

---

## Mode Signal Detection

**Before routing**, scan the task description for mode signals. Mode signal **overrides** task-type routing — `"fix null pointer --vibe"` activates Vibe Mode, not the bug-fix TDD route.

| If the description contains… | Mode | Action |
|---|---|---|
| `--vibe`, "prototype", "throwaway", "just exploring", "spike", "try out" | **Vibe Mode** | Print Vibe confirmation (below). Wait for Y. |
| `--hotfix`, "quick fix", "legacy codebase", "no tests here" | **Hotfix Mode** | Print Hotfix announcement (below). Use task-type routing. |
| None of the above | **Standard** | Use the Routing Table below normally. |

### Vibe Mode — Required Confirmation

Print this verbatim and wait for Y before routing:

```
⚡ Vibe Mode activated.
   - Routing directly to /s4-impl-task — TDD is optional.
   - s5 review is skipped for this session.
   - You MUST tag every commit [WIP/Prototype]. This creates tech debt.
   Confirm? (Y/n)
```

If the user says N, fall back to Standard Mode.

After Y: route to `/s4-impl-task`. Do NOT go through `/s4-tdd`.

### Hotfix Mode — Announcement

Print this and then use the Routing Table normally:

```
🔧 Hotfix Mode: TDD preserved. Routing to /s4-tdd.
   Downstream s5 review will apply CRITICAL-only criteria.
```

---

## Routing Table

Based on the user's one-sentence description, pick the first matching route:

| Task type | Route to |
|-----------|----------|
| Bug fix — something is broken | `/s4-tdd` (write a failing test that reproduces the bug first) |
| New behavior in existing code | `/s4-tdd` (write failing test for the new behavior) |
| Exploratory / throwaway | *(caught by Mode Signal Detection above — confirm Vibe Mode first)* |
| Environment / tooling setup | `/s4-setup-env` |
| Debug an existing failure | `/s4-local-debug` |

If the description is ambiguous between two routes, pick the one that requires MORE discipline (e.g., prefer `/s4-tdd` over `/s4-impl-task`). State your routing choice and the reason in one line.

---

## What Is NOT Skipped

Fast-track skips ceremony, not discipline. The following apply regardless:

- **s4-tdd HARD-GATE**: No production code without a failing test first. No exceptions in Standard and Hotfix Modes.
  *Vibe Mode exception: user has explicitly confirmed tech debt — routing goes directly to `/s4-impl-task` without tests.*
- **s4-impl-task HARD-GATE**: All acceptance criteria must be stated before writing code.
- **BROWNFIELD MODE**: If the project has `mode: brownfield` in `RULES.md`, the brownfield coverage gate in s4-tdd applies automatically — you do not need to re-set it.

---

## What Is Skipped

| Skipped artifact | Why it's safe to skip here |
|-----------------|---------------------------|
| `CONTEXT.md` glossary (s1) | Single-task scope; no cross-agent terminology coordination needed |
| `RULES.md` full definition (s1) | Existing project rules assumed already in place; new projects use defaults |
| PRD / Vision doc (s2) | One-sentence task description is sufficient for atomic scope |
| WBS / DAG (s3) | Single atomic task; dependency graph is trivially one node |
| Architecture Design Doc (s3) | No new subsystems introduced; changes are local |

If during execution you discover the task is NOT atomic (it requires new subsystems, cross-module changes, or alignment with other teams), **stop and say so**:

> *"This task turned out to be larger than atomic scope. Fast-track is not the right fit.
>  Consider running /s2-capture-vision to properly scope it first."*

Do not silently expand scope. Surface it and let the user decide.

---

## Completion

This skill has no artifact of its own. It completes the moment the user is routed to the correct s4 skill. There is no approval gate here — route and hand off immediately.

</what-to-do>

<supporting-info>

## When Fast-Track Is the Wrong Choice

Do not use this skill if any of the following are true:
- The user is starting a brand-new project with no existing codebase
- The task requires coordinating with other agents or teams
- The user is unsure what they want to build (use `/s0-brainstorm` instead)
- The task will touch more than 3 files across different modules
- Compliance, security, or architectural decisions are in scope

## Role Identity: Fast-Track Router
- **Mindset**: Remove friction, not discipline. The goal is to get to s4 faster — not to skip s4's rigor.
- **Upstream Dependency**: None. This is an entry point.
- **Downstream Target**: One of s4-tdd, s4-impl-task, s4-setup-env, or s4-local-debug.

## Process Flow

```dot
digraph fast_track {
    rankdir=LR;
    start   [label="User invokes\n/s-fast-track", shape=box];
    print   [label="Print skip\nconfirmation", shape=box, style=filled, fillcolor="#fffacc"];
    ask     [label="Ask ONE question:\nwhat's the task?", shape=box];
    detect  [label="Mode Signal\nDetection", shape=diamond];
    vibe    [label="Print ⚡ Vibe\nconfirmation\nWait Y/n", shape=box, style=filled, fillcolor="#fff0cc"];
    hotfix  [label="Print 🔧 Hotfix\nannouncement", shape=box, style=filled, fillcolor="#e8f4ff"];
    route   [label="Route to\ncorrect s4 skill", shape=box, style=filled, fillcolor="#ccffcc"];
    scope   [label="Scope too large?\nStop + warn user", shape=box, style=filled, fillcolor="#ffcccc"];

    start  -> print;
    print  -> ask;
    ask    -> scope   [label="non-atomic"];
    ask    -> detect  [label="atomic"];
    detect -> vibe    [label="--vibe / prototype"];
    detect -> hotfix  [label="--hotfix"];
    detect -> route   [label="standard"];
    vibe   -> route   [label="Y"];
    vibe   -> detect  [label="N (fallback)"];
    hotfix -> route;
}
```

## Artifact Dependencies
- **Reads**: `RULES.md` (optional — checks for `mode: brownfield`)
- **Writes**: nothing

</supporting-info>
