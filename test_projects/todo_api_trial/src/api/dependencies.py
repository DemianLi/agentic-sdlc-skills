import uuid
from typing import Optional

from fastapi import Header, HTTPException


def get_user_id(x_user_id: Optional[str] = Header(default=None)) -> uuid.UUID:
    if x_user_id is None:
        raise HTTPException(status_code=400, detail={"error": "MISSING_USER_ID"})
    try:
        return uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "INVALID_USER_ID"}) from None  # noqa: E501
