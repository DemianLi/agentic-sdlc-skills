from __future__ import annotations
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

PRIORITY = Literal["HIGH", "MEDIUM", "LOW"]


class CreateTodoRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    priority: PRIORITY = "MEDIUM"


class UpdateTodoRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    is_done: bool | None = None
    priority: PRIORITY | None = None


class TodoResponse(BaseModel):
    todo_id: UUID
    owner_id: UUID
    title: str
    is_done: bool
    priority: str
    created_at: datetime

    model_config = {"from_attributes": True}
