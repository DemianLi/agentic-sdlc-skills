from __future__ import annotations

from uuid import uuid4

"""TASK-12: E2E journey test — AC-1.1, AC-2.1, AC-3.1, AC-4.1"""

def test_full_crud_journey(client) -> None:
    user_id = str(uuid4())

    # AC-1.1: Create
    r = client.post(
        "/todos", json={"title": "Buy milk"}, headers={"X-User-Id": user_id}
    )
    assert r.status_code == 201
    todo = r.json()
    assert todo["title"] == "Buy milk"
    assert todo["is_done"] is False
    assert todo["owner_id"] == user_id
    todo_id = todo["todo_id"]

    # AC-2.1: List
    todos = client.get("/todos", headers={"X-User-Id": user_id}).json()
    assert len(todos) == 1
    assert todos[0]["todo_id"] == todo_id

    # AC-3.1: Mark done
    updated = client.patch(
        f"/todos/{todo_id}", json={"is_done": True}, headers={"X-User-Id": user_id}
    )
    assert updated.status_code == 200
    assert updated.json()["is_done"] is True

    # AC-4.1: Delete
    assert (
        client.delete(f"/todos/{todo_id}", headers={"X-User-Id": user_id}).status_code
        == 204
    )
    assert client.get("/todos", headers={"X-User-Id": user_id}).json() == []
