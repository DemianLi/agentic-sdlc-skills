from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class TodoORM(Base):
    __tablename__ = "todos"

    todo_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    priority: Mapped[str] = mapped_column(String(10), nullable=False, default="MEDIUM")
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
