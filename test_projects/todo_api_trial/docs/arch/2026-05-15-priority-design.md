# OpenSpec Design — Todo Priority Filtering

## Context

The Todo entity is a flat list with no urgency signal. Consumers (mobile, dashboard) need to sort by importance without implementing their own heuristics. Adding a `priority` enum (HIGH / MEDIUM / LOW) with a filter endpoint is the minimal change that solves this.

## Decision

Add `priority: Literal["HIGH", "MEDIUM", "LOW"]` to the `Todo` domain model with default `MEDIUM`. Propagate through all layers: domain → infra ORM → Pydantic schemas → FastAPI routes. Add a new `get_by_owner_filtered(owner_id, priority=None)` repository method to leave the existing `get_by_owner` signature untouched.

## Data Structures

```python
# domain/models/todo.py
@dataclass
class Todo:
    owner_id: UUID
    title: str
    priority: str = "MEDIUM"          # ← NEW
    todo_id: UUID = field(default_factory=uuid4)
    is_done: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# api/schemas.py
PRIORITY_LEVELS = Literal["HIGH", "MEDIUM", "LOW"]

class CreateTodoRequest(BaseModel):
    title: str
    priority: PRIORITY_LEVELS = "MEDIUM"   # ← NEW

class UpdateTodoRequest(BaseModel):
    title: str | None = None
    is_done: bool | None = None
    priority: PRIORITY_LEVELS | None = None  # ← NEW

class TodoResponse(BaseModel):
    todo_id: UUID
    owner_id: UUID
    title: str
    is_done: bool
    priority: str                            # ← NEW
    created_at: datetime
```

## API Contracts

### POST /todos
Request body: `{ "title": "...", "priority": "HIGH" }` (priority optional, default MEDIUM)
Response: TodoResponse including `priority` field

### GET /todos?priority=HIGH
Query param: `priority: Literal["HIGH","MEDIUM","LOW"] | None = None`
When provided: filter; when absent: return all

### PATCH /todos/{id}
Request body: `{ "priority": "LOW" }` (title and is_done remain optional)

## Sequence Diagram

```
Client          Router           Service          Repository         DB
  |                |                 |                  |             |
  |-- POST /todos →|                 |                  |             |
  |   {priority}   |-- create_todo→  |                  |             |
  |                |   (priority)    |-- save(todo) →   |             |
  |                |                 |                  |-- INSERT → |
  |←── 201 {priority:"HIGH"} ────────────────────────────────────── |
  |                |                 |                  |             |
  |-- GET /todos?priority=HIGH →     |                  |             |
  |                |-- list_todos → |                  |             |
  |                |   (priority)   |-- get_by_owner_filtered() →   |
  |                |                 |                  |-- WHERE →  |
  |←── 200 [{priority:"HIGH"}] ─────────────────────────────────── |
```

## Consequences

- **Positive**: No breaking changes for existing clients (new field in response, optional param in request)
- **Negative**: DB migration required for production SQLite (`ALTER TABLE`)
- **Risk**: Empty test suite means first TDD run builds all coverage from zero — must hit ≥80% in one pass
