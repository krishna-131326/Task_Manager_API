from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from database.mongo import tasks_collection
from models.task_model import TaskInput, TaskOutput, TaskStatus
from schemas.task_schema import task_serializer

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskOutput], summary="List tasks")
async def read_tasks(status: TaskStatus | None = None) -> list[TaskOutput]:
    query: dict[str, str] = {}

    if status:
        query["status"] = status

    task_documents = tasks_collection.find(query)
    return [task_serializer(task) async for task in task_documents]


@router.post(
    "",
    response_model=TaskOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
async def create_task(task_input: TaskInput) -> TaskOutput:
    task_document: dict[str, Any] = {
        "title": task_input.title,
        "status": task_input.status,
        "created_at": datetime.now(timezone.utc),
    }

    result = await tasks_collection.insert_one(task_document)
    saved_task = await tasks_collection.find_one({"_id": result.inserted_id})

    return task_serializer(saved_task)


@router.put("/{task_id}", response_model=TaskOutput, summary="Update a task")
async def update_task(task_id: str, task_input: TaskInput) -> TaskOutput:
    task_identifier = ObjectId(task_id) if ObjectId.is_valid(task_id) else task_id

    result = await tasks_collection.update_one(
        {"_id": task_identifier},
        {"$set": {"title": task_input.title, "status": task_input.status}},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    updated_task = await tasks_collection.find_one({"_id": task_identifier})
    return task_serializer(updated_task)


@router.delete("/{task_id}", summary="Delete a task")
async def delete_task(task_id: str) -> dict[str, str]:
    task_identifier = ObjectId(task_id) if ObjectId.is_valid(task_id) else task_id

    result = await tasks_collection.delete_one({"_id": task_identifier})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return {"message": "Task deleted"}
