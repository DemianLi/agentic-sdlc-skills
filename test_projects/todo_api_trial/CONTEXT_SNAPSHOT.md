# Context Snapshot — Priority Filtering Iteration — 2026-05-15

> This snapshot supersedes the previous iteration snapshot (2026-05-16 Todo CRUD).
> Previous iteration complete. This is a new feature addition.

## Iteration Goal

Add a `priority` field (HIGH / MEDIUM / LOW, default MEDIUM) to the Todo entity.
Expose a `?priority=` filter on `GET /todos`.
Allow priority updates via `PATCH /todos/{id}`.

## Must-Have REQs

- REQ-1: Priority field on Todo entity (HIGH/MEDIUM/LOW, default MEDIUM)
- REQ-2: `GET /todos?priority=<level>` filter
- REQ-3: `PATCH /todos/{id}` accepts priority update

## Out of Scope

- Sorting by priority
- Multi-value priority query (e.g. `?priority=HIGH,MEDIUM`)
- Priority-based notifications

## Key Constraints

- No breaking changes to existing endpoints (existing clients must not break)
- `priority` must be validated — `422` on invalid value
- Coverage ≥ 80% on `src/` after changes (RULES.md threshold)
- Tech stack: Python 3.9.19 / FastAPI 0.111.0 / SQLAlchemy 2.0.30 / SQLite in-memory for tests

## Forbidden Actions

- Do NOT modify `TodoId`, `Completion`, or `is_done` field semantics
- Do NOT add raw SQL — use SQLAlchemy ORM only
- Do NOT add sorting behavior — deferred to next iteration
- Do NOT rename any existing API response fields

## Source Documents

- Vision: `docs/specs/2026-05-15-priority-vision.md`
- Alignment: `docs/specs/2026-05-15-priority-alignment.md`
- Requirements: `docs/specs/2026-05-15-priority-requirements.md`
- Rules: `RULES.md`
- Context: `CONTEXT.md`

## User Flows (E2E scope)

1. Create todo with HIGH priority → retrieve → verify `priority: "HIGH"`
2. Create 3 todos with different priorities → filter by HIGH → verify 1 returned
3. Create todo (default priority MEDIUM) → PATCH to HIGH → verify updated
