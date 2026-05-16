from __future__ import annotations
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.models.todo import Todo
from src.domain.repositories.todo_repository import TodoRepository
from src.infrastructure.models import TodoORM


class SQLATodoRepository(TodoRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, todo: Todo) -> Todo:
        orm = TodoORM(
            todo_id=str(todo.todo_id),
            owner_id=str(todo.owner_id),
            title=todo.title,
            priority=todo.priority,
            is_done=todo.is_done,
            created_at=todo.created_at,
        )
        self._session.add(orm)
        self._session.commit()
        self._session.refresh(orm)
        return self._to_domain(orm)

    def get_by_owner(self, owner_id: UUID) -> list[Todo]:
        rows = (
            self._session.query(TodoORM)
            .filter(TodoORM.owner_id == str(owner_id))
            .all()
        )
        return [self._to_domain(r) for r in rows]

    def get_by_owner_filtered(
        self, owner_id: UUID, priority: str | None = None
    ) -> list[Todo]:
        query = (
            self._session.query(TodoORM)
            .filter(TodoORM.owner_id == str(owner_id))
        )
        if priority is not None:
            query = query.filter(TodoORM.priority == priority)
        return [self._to_domain(r) for r in query.all()]

    def get_by_id_and_owner(
        self, todo_id: UUID, owner_id: UUID
    ) -> Todo | None:
        row = (
            self._session.query(TodoORM)
            .filter(
                TodoORM.todo_id == str(todo_id),
                TodoORM.owner_id == str(owner_id),
            )
            .first()
        )
        return self._to_domain(row) if row else None

    def update(self, todo: Todo) -> Todo:
        row = (
            self._session.query(TodoORM)
            .filter(TodoORM.todo_id == str(todo.todo_id))
            .first()
        )
        if row:
            row.title = todo.title
            row.is_done = todo.is_done
            row.priority = todo.priority
            self._session.commit()
            self._session.refresh(row)
        return self._to_domain(row)

    def delete(self, todo_id: UUID) -> None:
        self._session.query(TodoORM).filter(
            TodoORM.todo_id == str(todo_id)
        ).delete()
        self._session.commit()

    @staticmethod
    def _to_domain(orm: TodoORM) -> Todo:
        from uuid import UUID as _UUID
        return Todo(
            todo_id=_UUID(orm.todo_id),
            owner_id=_UUID(orm.owner_id),
            title=orm.title,
            priority=orm.priority,
            is_done=orm.is_done,
            created_at=orm.created_at,
        )
