"""Unit tests for TodoService — priority support (TDD RED)."""
import uuid
from unittest.mock import MagicMock

from src.domain.models.todo import Todo
from src.domain.todo_service import TodoService


def _make_repo(todos: list) -> MagicMock:
    repo = MagicMock()
    repo.get_by_owner_filtered.return_value = todos
    return repo


def test_create_todo_default_priority():
    owner_id = uuid.uuid4()
    repo = MagicMock()
    saved = Todo(owner_id=owner_id, title="t", priority="MEDIUM")
    repo.save.return_value = saved
    service = TodoService(repo)
    result = service.create_todo(owner_id=owner_id, title="t")
    call_args = repo.save.call_args[0][0]
    assert call_args.priority == "MEDIUM"
    assert result.priority == "MEDIUM"


def test_create_todo_explicit_high_priority():
    owner_id = uuid.uuid4()
    repo = MagicMock()
    saved = Todo(owner_id=owner_id, title="t", priority="HIGH")
    repo.save.return_value = saved
    service = TodoService(repo)
    result = service.create_todo(owner_id=owner_id, title="t", priority="HIGH")
    call_args = repo.save.call_args[0][0]
    assert call_args.priority == "HIGH"
    assert result.priority == "HIGH"


def test_list_todos_with_priority_filter():
    owner_id = uuid.uuid4()
    high_todo = Todo(owner_id=owner_id, title="urgent", priority="HIGH")
    repo = _make_repo([high_todo])
    service = TodoService(repo)
    results = service.list_todos(owner_id=owner_id, priority="HIGH")
    repo.get_by_owner_filtered.assert_called_once_with(owner_id, priority="HIGH")
    assert len(results) == 1
    assert results[0].priority == "HIGH"


def test_list_todos_no_filter_returns_all():
    owner_id = uuid.uuid4()
    todos = [
        Todo(owner_id=owner_id, title="a", priority="HIGH"),
        Todo(owner_id=owner_id, title="b", priority="LOW"),
    ]
    repo = _make_repo(todos)
    service = TodoService(repo)
    results = service.list_todos(owner_id=owner_id)
    repo.get_by_owner_filtered.assert_called_once_with(owner_id, priority=None)
    assert len(results) == 2


def test_update_todo_priority():
    owner_id = uuid.uuid4()
    todo_id = uuid.uuid4()
    existing = Todo(owner_id=owner_id, title="task", priority="LOW", todo_id=todo_id)
    repo = MagicMock()
    repo.get_by_id_and_owner.return_value = existing
    updated = Todo(owner_id=owner_id, title="task", priority="HIGH", todo_id=todo_id)
    repo.update.return_value = updated
    service = TodoService(repo)
    result = service.update_todo(todo_id=todo_id, owner_id=owner_id, priority="HIGH")
    assert result.priority == "HIGH"
