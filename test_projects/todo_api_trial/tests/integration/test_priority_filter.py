"""Integration tests for priority filtering."""
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.database import Base
from src.main import create_app
from src.api.routes.todos import get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture()
def client():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


USER_ID = str(uuid.uuid4())
HEADERS = {"X-User-Id": USER_ID}


def test_create_todo_with_high_priority(client):
    """AC-1.2: POST /todos with priority=HIGH returns priority=HIGH."""
    resp = client.post("/todos", json={"title": "urgent", "priority": "HIGH"}, headers=HEADERS)
    assert resp.status_code == 201
    assert resp.json()["priority"] == "HIGH"


def test_create_todo_default_priority(client):
    """AC-1.1: POST /todos without priority returns priority=MEDIUM."""
    resp = client.post("/todos", json={"title": "normal"}, headers=HEADERS)
    assert resp.status_code == 201
    assert resp.json()["priority"] == "MEDIUM"


def test_create_todo_invalid_priority(client):
    """AC-1.3: POST /todos with invalid priority returns 422."""
    resp = client.post("/todos", json={"title": "x", "priority": "URGENT"}, headers=HEADERS)
    assert resp.status_code == 422


def test_filter_todos_by_priority(client):
    """AC-2.1: GET /todos?priority=HIGH returns only HIGH todos."""
    client.post("/todos", json={"title": "high", "priority": "HIGH"}, headers=HEADERS)
    client.post("/todos", json={"title": "medium", "priority": "MEDIUM"}, headers=HEADERS)
    client.post("/todos", json={"title": "low", "priority": "LOW"}, headers=HEADERS)

    resp = client.get("/todos?priority=HIGH", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["priority"] == "HIGH"
    assert data[0]["title"] == "high"


def test_list_todos_no_filter_returns_all(client):
    """AC-2.2: GET /todos without filter returns all todos."""
    client.post("/todos", json={"title": "a", "priority": "HIGH"}, headers=HEADERS)
    client.post("/todos", json={"title": "b", "priority": "LOW"}, headers=HEADERS)

    resp = client.get("/todos", headers=HEADERS)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_todos_invalid_priority(client):
    """AC-2.3: GET /todos?priority=INVALID returns 422."""
    resp = client.get("/todos?priority=INVALID", headers=HEADERS)
    assert resp.status_code == 422


def test_patch_todo_priority(client):
    """AC-3.1: PATCH /todos/{id} with priority updates it."""
    create_resp = client.post("/todos", json={"title": "task", "priority": "LOW"}, headers=HEADERS)
    todo_id = create_resp.json()["todo_id"]

    patch_resp = client.patch(f"/todos/{todo_id}", json={"priority": "HIGH"}, headers=HEADERS)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["priority"] == "HIGH"
