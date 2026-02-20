from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)


class Task(TaskCreate):
    id: int
    done: bool = False
    created_at: datetime
