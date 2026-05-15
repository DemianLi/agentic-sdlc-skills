from __future__ import annotations

from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.api.dependencies import get_user_id

test_app = FastAPI()


@test_app.get("/test")
def test_route(user_id: UUID = Depends(get_user_id)) -> dict[str, str]:
    return {"user_id": str(user_id)}


client = TestClient(test_app, raise_server_exceptions=False)


def test_missing_user_id_returns_400() -> None:
    """AC-1.2"""
    resp = client.get("/test")
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "MISSING_USER_ID"


def test_invalid_user_id_returns_400() -> None:
    """AC-1.3"""
    resp = client.get("/test", headers={"X-User-Id": "not-a-uuid"})
    assert resp.status_code == 400
    assert resp.json()["detail"]["error"] == "INVALID_USER_ID"


def test_valid_user_id_parses_correctly() -> None:
    valid_uuid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    resp = client.get("/test", headers={"X-User-Id": valid_uuid})
    assert resp.status_code == 200
    assert resp.json()["user_id"] == valid_uuid
