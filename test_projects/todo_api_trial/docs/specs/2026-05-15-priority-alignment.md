# Alignment — Todo Priority Filtering

## Resolved Conflicts

| Conflict | Resolution |
|---|---|
| Priority on PATCH vs read-only | Priority IS mutable via PATCH — included in scope |
| Enum vs integer for priority | Enum (HIGH/MEDIUM/LOW) — human-readable, no ordering ambiguity |
| Default priority on creation | MEDIUM — neutral default, explicit choice |

## IN Scope

- `priority` field on Todo entity (HIGH / MEDIUM / LOW, default MEDIUM)
- `POST /todos` — accept optional `priority` in request body
- `PATCH /todos/{id}` — accept optional `priority` update
- `GET /todos?priority=HIGH` — filter Todos by exact priority level
- `GET /todos/{id}` — include `priority` in response

## OUT of Scope

- Sorting by priority
- Multi-value priority filter
- Notifications or escalation logic

## Deferred

- Priority-based SLA tracking (future iteration)
