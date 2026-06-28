from typing import Any, Mapping

from models.task_model import TaskOutput


def task_serializer(task: Mapping[str, Any]) -> TaskOutput:
    """Convert a MongoDB document into the public task model."""
    return TaskOutput(
        id=str(task["_id"]),
        title=task["title"],
        status=task["status"],
        created_at=task["created_at"],
    )
