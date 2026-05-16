from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from src.api.dependencies import get_user_id
from src.api.schemas import CreateTodoRequest, TodoResponse, UpdateTodoRequest
from src.domain.exceptions import TodoNotFoundError
from src.domain.todo_service import TodoService
from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories.sqla_todo_repository import SQLATodoRepository

router = APIRouter(prefix="/todos", tags=["todos"])


def get_db() -> Session:  # type: ignore[return]
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(SQLATodoRepository(db))


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(
    body: CreateTodoRequest,
    user_id: UUID = Depends(get_user_id),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    todo = service.create_todo(
        owner_id=user_id, title=body.title, priority=body.priority
    )
    return TodoResponse(
        todo_id=todo.todo_id,
        owner_id=todo.owner_id,
        title=todo.title,
        is_done=todo.is_done,
        priority=todo.priority,
        created_at=todo.created_at,
    )


@router.get("", response_model=list[TodoResponse])
def list_todos(
    user_id: UUID = Depends(get_user_id),
    service: TodoService = Depends(get_todo_service),
    priority: Literal["HIGH", "MEDIUM", "LOW"] | None = Query(None),
) -> list:  # type: ignore[type-arg]
    todos = service.list_todos(owner_id=user_id, priority=priority)
    return [
        TodoResponse(
            todo_id=t.todo_id,
            owner_id=t.owner_id,
            title=t.title,
            is_done=t.is_done,
            priority=t.priority,
            created_at=t.created_at,
        )
        for t in todos
    ]


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    body: UpdateTodoRequest,
    user_id: UUID = Depends(get_user_id),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    try:
        todo = service.update_todo(
            todo_id=todo_id,
            owner_id=user_id,
            title=body.title,
            is_done=body.is_done,
            priority=body.priority,
        )
    except TodoNotFoundError:
        raise HTTPException(status_code=404) from None
    return TodoResponse(
        todo_id=todo.todo_id,
        owner_id=todo.owner_id,
        title=todo.title,
        is_done=todo.is_done,
        priority=todo.priority,
        created_at=todo.created_at,
    )


@router.delete("/{todo_id}", status_code=204, response_class=Response)
def delete_todo(
    todo_id: UUID,
    user_id: UUID = Depends(get_user_id),
    service: TodoService = Depends(get_todo_service),
) -> Response:
    try:
        service.delete_todo(todo_id=todo_id, owner_id=user_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404) from None
    return Response(status_code=204)
