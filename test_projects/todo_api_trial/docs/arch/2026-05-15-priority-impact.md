# Impact Report — Todo Priority Filtering

## Breaking Changes (🔴)

- **`src/infrastructure/models.py` → `TodoORM`**: Adding `priority` column requires a DB migration. In-memory SQLite test DB is recreated per session (no migration needed for tests). Production SQLite file requires `ALTER TABLE todos ADD COLUMN priority TEXT DEFAULT 'MEDIUM'`. **Migration needed before any production deployment.**

## Additive Changes (🟡)

- **`src/domain/models/todo.py` → `Todo` dataclass**: Add `priority: str = "MEDIUM"` field. Existing code constructing `Todo(owner_id=..., title=...)` continues to work — default applies.
- **`src/api/schemas.py` → `CreateTodoRequest`**: Add optional `priority: Literal["HIGH","MEDIUM","LOW"] = "MEDIUM"`. Existing POST requests without priority continue to work.
- **`src/api/schemas.py` → `UpdateTodoRequest`**: Add optional `priority: Literal["HIGH","MEDIUM","LOW"] | None = None`. Existing PATCH requests unaffected.
- **`src/api/schemas.py` → `TodoResponse`**: Add `priority: str` field. **Additive for API consumers** — new field in response; existing clients that don't read `priority` are unaffected.
- **`src/domain/repositories/todo_repository.py` → `TodoRepository`**: Add abstract method `get_by_owner_filtered(owner_id, priority=None)` OR modify `get_by_owner` to accept optional filter. Choosing new method to avoid breaking existing `get_by_owner` signature.
- **`src/infrastructure/repositories/sqla_todo_repository.py`**: Implement `get_by_owner_filtered` with SQLAlchemy WHERE clause.
- **`src/domain/todo_service.py` → `create_todo`**: Add `priority: str = "MEDIUM"` parameter.
- **`src/domain/todo_service.py` → `update_todo`**: Add `priority: str | None = None` parameter.
- **`src/domain/todo_service.py` → `list_todos`**: Add `priority: str | None = None` parameter; delegates to `get_by_owner_filtered`.
- **`src/api/routes/todos.py` → `list_todos`**: Add `priority: Literal["HIGH","MEDIUM","LOW"] | None = Query(None)` parameter.
- **`src/api/routes/todos.py` → `create_todo`**: Pass `priority=body.priority` to service.
- **`src/api/routes/todos.py` → `update_todo`**: Pass `priority=body.priority` to service.

## Technical Debt to Resolve First

- **`tests/` is empty**: No existing test files means no regression coverage. Stage 4 will write all tests from scratch — acceptable but risky. Must achieve ≥80% coverage as first run.
- No existing unit tests on `TodoService` or `Todo` domain model. TDD will build this coverage.

## Recommended Approach

Add `priority` as an optional field with default `MEDIUM` across all layers (domain → infra → API). Use a new `get_by_owner_filtered` repository method to avoid breaking the existing `get_by_owner` interface. The DB migration is SQL-trivial for SQLite. Start TDD from the domain model outward.
