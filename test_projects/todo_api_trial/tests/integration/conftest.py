from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.routes.todos import get_db, get_todo_service
from src.domain.todo_service import TodoService
from src.infrastructure.database import Base
from src.infrastructure.repositories.sqla_todo_repository import SQLATodoRepository
from src.main import app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_db():
        yield db_session

    def override_service():
        return TodoService(SQLATodoRepository(db_session))

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_todo_service] = override_service
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
