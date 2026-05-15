from uuid import UUID, uuid4

import pytest

from src.domain.exceptions import TodoNotFoundError
from src.domain.models.todo import Todo


def test_todo_default_is_done_is_false() -> None:
    todo = Todo(owner_id=uuid4(), title="Buy milk")
    assert todo.is_done is False


def test_todo_has_auto_generated_id() -> None:
    todo = Todo(owner_id=uuid4(), title="Buy milk")
    assert isinstance(todo.todo_id, UUID)


def test_todo_has_created_at() -> None:
    todo = Todo(owner_id=uuid4(), title="Buy milk")
    assert todo.created_at is not None


def test_todo_not_found_error_is_exception() -> None:
    with pytest.raises(TodoNotFoundError):
        raise TodoNotFoundError("not found")
