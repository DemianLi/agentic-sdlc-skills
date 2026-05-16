from __future__ import annotations

from uuid import uuid4

USER_A = str(uuid4())
USER_B = str(uuid4())


def test_create_todo_missing_user_id(client) -> None:
    """AC-1.2"""
    resp = client.post("/todos", json={"title": "Buy milk"})
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "MISSING_USER_ID"


def test_create_todo_invalid_user_id(client) -> None:
    """AC-1.3"""
    resp = client.post(
        "/todos", json={"title": "Buy milk"}, headers={"X-User-Id": "bad"}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "INVALID_USER_ID"


def test_create_todo_missing_title(client) -> None:
    """AC-1.4"""
    resp = client.post("/todos", json={}, headers={"X-User-Id": USER_A})
    assert resp.status_code == 422


def test_list_todos_empty(client) -> None:
    """AC-2.2"""
    resp = client.get("/todos", headers={"X-User-Id": USER_A})
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_todos_isolation(client) -> None:
    """AC-2.3 — User B cannot see User A's todos"""
    client.post("/todos", json={"title": "A-1"}, headers={"X-User-Id": USER_A})
    client.post("/todos", json={"title": "A-2"}, headers={"X-User-Id": USER_A})
    client.post("/todos", json={"title": "B-1"}, headers={"X-User-Id": USER_B})
    assert len(client.get("/todos", headers={"X-User-Id": USER_A}).json()) == 2
    assert len(client.get("/todos", headers={"X-User-Id": USER_B}).json()) == 1


def test_list_todos_missing_user_id(client) -> None:
    """AC-2.4"""
    assert client.get("/todos").status_code == 400


def test_update_todo_title(client) -> None:
    """AC-3.2"""
    todo_id = client.post(
        "/todos", json={"title": "Buy milk"}, headers={"X-User-Id": USER_A}
    ).json()["todo_id"]
    resp = client.patch(
        f"/todos/{todo_id}",
        json={"title": "Buy oat milk"},
        headers={"X-User-Id": USER_A},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Buy oat milk"


def test_update_todo_wrong_owner(client) -> None:
    """AC-3.4 — must return 404, not 403"""
    todo_id = client.post(
        "/todos", json={"title": "A todo"}, headers={"X-User-Id": USER_A}
    ).json()["todo_id"]
    assert (
        client.patch(
            f"/todos/{todo_id}", json={"is_done": True}, headers={"X-User-Id": USER_B}
        ).status_code
        == 404
    )


def test_update_todo_missing_user_id(client) -> None:
    """AC-3.5"""
    todo_id = client.post(
        "/todos", json={"title": "Buy milk"}, headers={"X-User-Id": USER_A}
    ).json()["todo_id"]
    assert client.patch(f"/todos/{todo_id}", json={"is_done": True}).status_code == 400


def test_delete_todo_not_found(client) -> None:
    """AC-4.2"""
    assert (
        client.delete(f"/todos/{uuid4()}", headers={"X-User-Id": USER_A}).status_code
        == 404
    )


def test_delete_todo_wrong_owner(client) -> None:
    """AC-4.3"""
    todo_id = client.post(
        "/todos", json={"title": "A todo"}, headers={"X-User-Id": USER_A}
    ).json()["todo_id"]
    assert (
        client.delete(f"/todos/{todo_id}", headers={"X-User-Id": USER_B}).status_code
        == 404
    )


def test_delete_todo_missing_user_id(client) -> None:
    """AC-4.4"""
    todo_id = client.post(
        "/todos", json={"title": "Buy milk"}, headers={"X-User-Id": USER_A}
    ).json()["todo_id"]
    assert client.delete(f"/todos/{todo_id}").status_code == 400
