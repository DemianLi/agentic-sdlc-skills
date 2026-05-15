from __future__ import annotations
from uuid import UUID

from src.domain.exceptions import TodoNotFoundError
from src.domain.models.todo import Todo
from src.domain.repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository) -> None:
        self._repo = repository

    def create_todo(self, owner_id: UUID, title: str, priority: str = "MEDIUM") -> Todo:
        todo = Todo(owner_id=owner_id, title=title, priority=priority)
        return self._repo.save(todo)

    def list_todos(self, owner_id: UUID, priority: str | None = None) -> list[Todo]:
        return self._repo.get_by_owner_filtered(owner_id, priority=priority)

    def update_todo(
        self,
        todo_id: UUID,
        owner_id: UUID,
        title: str | None = None,
        is_done: bool | None = None,
        priority: str | None = None,
    ) -> Todo:
        todo = self._repo.get_by_id_and_owner(todo_id, owner_id)
        if todo is None:
            raise TodoNotFoundError(f"Todo {todo_id} not found for owner {owner_id}")
        if title is not None:
            todo.title = title
        if is_done is not None:
            todo.is_done = is_done
        if priority is not None:
            todo.priority = priority
        return self._repo.update(todo)

    def delete_todo(self, todo_id: UUID, owner_id: UUID) -> None:
        todo = self._repo.get_by_id_and_owner(todo_id, owner_id)
        if todo is None:
            raise TodoNotFoundError(f"Todo {todo_id} not found for owner {owner_id}")
        self._repo.delete(todo_id)
