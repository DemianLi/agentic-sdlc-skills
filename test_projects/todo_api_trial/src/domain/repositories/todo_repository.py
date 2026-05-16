from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.todo import Todo


class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def get_by_owner(self, owner_id: UUID) -> list[Todo]: ...

    @abstractmethod
    def get_by_owner_filtered(
        self, owner_id: UUID, priority: str | None = None
    ) -> list[Todo]: ...

    @abstractmethod
    def get_by_id_and_owner(
        self, todo_id: UUID, owner_id: UUID
    ) -> Todo | None: ...

    @abstractmethod
    def update(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def delete(self, todo_id: UUID) -> None: ...
