# WBS — Todo Priority Filtering

## TASK-1: Add priority field to Todo domain model

**Input**: `src/domain/models/todo.py`
**Output**: `Todo` dataclass has `priority: str = "MEDIUM"` field
**AC**: AC-1.1, AC-1.2 (unit tests pass for default and explicit priority)
**Estimate**: 3 min
**Blocked-by**: nothing
**File Scope**: `src/domain/models/todo.py`, `tests/unit/test_todo_model.py`

---

## TASK-2: Add priority filter to TodoRepository interface

**Input**: `src/domain/repositories/todo_repository.py`
**Output**: New abstract method `get_by_owner_filtered(owner_id, priority=None) -> list[Todo]`
**AC**: Interface defines the filter contract
**Estimate**: 2 min
**Blocked-by**: TASK-1
**File Scope**: `src/domain/repositories/todo_repository.py`

---

## TASK-3: Implement priority filter in SQLATodoRepository

**Input**: `src/infrastructure/repositories/sqla_todo_repository.py`, `src/infrastructure/models.py`
**Output**: `TodoORM.priority` column + `get_by_owner_filtered` implementation with WHERE clause
**AC**: AC-2.1 (filter returns only matching todos)
**Estimate**: 5 min
**Blocked-by**: TASK-2
**File Scope**: `src/infrastructure/models.py`, `src/infrastructure/repositories/sqla_todo_repository.py`, `tests/integration/test_priority_filter.py`

---

## TASK-4: Update TodoService (create + list + update)

**Input**: `src/domain/todo_service.py`
**Output**: `create_todo` accepts `priority`; `list_todos` accepts optional filter; `update_todo` accepts `priority`
**AC**: AC-1.1, AC-1.2, AC-2.1, AC-2.2, AC-3.1
**Estimate**: 4 min
**Blocked-by**: TASK-1, TASK-2
**File Scope**: `src/domain/todo_service.py`, `tests/unit/test_todo_service.py`

---

## TASK-5: Update API schemas and routes

**Input**: `src/api/schemas.py`, `src/api/routes/todos.py`
**Output**: `CreateTodoRequest`, `UpdateTodoRequest`, `TodoResponse` include `priority`; list route accepts `?priority=` query param
**AC**: AC-1.3, AC-2.3 (validation 422 on invalid enum)
**Estimate**: 4 min
**Blocked-by**: TASK-4
**File Scope**: `src/api/schemas.py`, `src/api/routes/todos.py`
