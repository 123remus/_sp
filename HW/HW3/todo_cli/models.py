from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    priority: int = Field(default=1, ge=1, le=3)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    @property
    def priority_label(self) -> str:
        return {1: "low", 2: "medium", 3: "high"}[self.priority]

    def mark_complete(self) -> None:
        self.completed = True
        self.completed_at = datetime.now(timezone.utc).isoformat()
