"""Unit tests for Todo domain model — priority field (TDD RED)."""
import uuid
from src.domain.models.todo import Todo


def test_todo_default_priority_is_medium():
    """AC-1.1: New Todo without explicit priority defaults to MEDIUM."""
    todo = Todo(owner_id=uuid.uuid4(), title="buy milk")
    assert todo.priority == "MEDIUM"


def test_todo_explicit_priority():
    """AC-1.2: New Todo with explicit HIGH priority retains it."""
    todo = Todo(owner_id=uuid.uuid4(), title="urgent task", priority="HIGH")
    assert todo.priority == "HIGH"
