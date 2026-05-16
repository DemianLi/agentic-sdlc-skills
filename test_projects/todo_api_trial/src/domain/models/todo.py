from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Todo:
    owner_id: UUID
    title: str
    priority: str = "MEDIUM"
    todo_id: UUID = field(default_factory=uuid4)
    is_done: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
