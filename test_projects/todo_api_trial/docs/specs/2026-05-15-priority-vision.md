# Vision — Todo Priority Filtering

## Problem Statement

Users create many Todos but have no way to indicate urgency. Everything looks equally important. Without priority, the API is a flat list — consumers (mobile apps, dashboards) must implement their own sorting heuristics, leading to inconsistent UX across clients.

## Target Users

- Mobile-app developers calling the Todo API who need to show "urgent items first"
- Dashboard builders who want to surface HIGH-priority incomplete Todos

## Proposed Approach

Add an optional `priority` field to the Todo entity with three levels: `HIGH`, `MEDIUM`, `LOW` (default `MEDIUM`).
Expose a `?priority=` query parameter on `GET /todos` to filter by priority level.
No breaking changes to existing fields or response shape.

## Out of Scope

- Sorting/ordering by priority — deferred
- Multiple priority values in a single query (e.g. `?priority=HIGH,MEDIUM`)
- Priority-based notifications

## Open Questions

- Should `PATCH /todos/{id}` accept `priority` updates? **Decision: YES — included in scope.**
