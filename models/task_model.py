from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator

TaskStatus = Literal["pending", "completed"]


class TaskInput(BaseModel):
    title: str
    status: TaskStatus

    @field_validator("title")
    @classmethod
    def validate_title(cls, title: str) -> str:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Title cannot be empty")
        return cleaned_title

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, task_status: object) -> object:
        return task_status.lower() if isinstance(task_status, str) else task_status


class TaskOutput(BaseModel):
    id: str
    title: str
    status: TaskStatus
    created_at: datetime
