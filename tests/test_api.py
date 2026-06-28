from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any, AsyncIterator

import pytest
from fastapi.testclient import TestClient

import routers.task as task_module
from main import app

client = TestClient(app)


class FakeCollection:
    def __init__(self) -> None:
        self.tasks: list[dict[str, Any]] = []
        self._next_id = 1

    def find(self, query: dict[str, str]) -> AsyncIterator[dict[str, Any]]:
        async def generator() -> AsyncIterator[dict[str, Any]]:
            for task in self.tasks:
                if not query or task.get("status") == query.get("status"):
                    yield task

        return generator()

    async def insert_one(self, task: dict[str, Any]) -> SimpleNamespace:
        new_task = dict(task)
        new_task["_id"] = f"task-{self._next_id}"
        self._next_id += 1
        self.tasks.append(new_task)
        return SimpleNamespace(inserted_id=new_task["_id"])

    async def find_one(self, query: dict[str, Any]) -> dict[str, Any] | None:
        task_id = query["_id"]
        for task in self.tasks:
            if task["_id"] == task_id:
                return task
        return None

    async def update_one(
        self,
        query: dict[str, Any],
        update: dict[str, dict[str, str]],
    ) -> SimpleNamespace:
        task_id = query["_id"]
        for task in self.tasks:
            if task["_id"] == task_id:
                task["title"] = update["$set"]["title"]
                task["status"] = update["$set"]["status"]
                return SimpleNamespace(matched_count=1)
        return SimpleNamespace(matched_count=0)

    async def delete_one(self, query: dict[str, Any]) -> SimpleNamespace:
        task_id = query["_id"]
        for index, task in enumerate(self.tasks):
            if task["_id"] == task_id:
                del self.tasks[index]
                return SimpleNamespace(deleted_count=1)
        return SimpleNamespace(deleted_count=0)


@pytest.fixture
def fake_collection(monkeypatch: pytest.MonkeyPatch) -> FakeCollection:
    collection = FakeCollection()
    monkeypatch.setattr(task_module, "tasks_collection", collection)
    return collection


def test_home() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Task Manager!"}


def test_create_task(fake_collection: FakeCollection) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Write tests", "status": "pending"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Write tests"
    assert response.json()["status"] == "pending"
    assert len(fake_collection.tasks) == 1


def test_fetch_tasks(fake_collection: FakeCollection) -> None:
    fake_collection.tasks.append(
        {
            "_id": "task-1",
            "title": "Study FastAPI",
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
        }
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Study FastAPI"


def test_filter_tasks_by_status(fake_collection: FakeCollection) -> None:
    created_at = datetime.now(timezone.utc)
    fake_collection.tasks.extend(
        [
            {
                "_id": "task-1",
                "title": "Still working",
                "status": "pending",
                "created_at": created_at,
            },
            {
                "_id": "task-2",
                "title": "Already done",
                "status": "completed",
                "created_at": created_at,
            },
        ]
    )

    response = client.get("/tasks", params={"status": "completed"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Already done"]


def test_update_task(fake_collection: FakeCollection) -> None:
    fake_collection.tasks.append(
        {
            "_id": "task-1",
            "title": "Old title",
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
        }
    )

    response = client.put(
        "/tasks/task-1",
        json={"title": "Updated title", "status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["status"] == "completed"


def test_delete_task(fake_collection: FakeCollection) -> None:
    fake_collection.tasks.append(
        {
            "_id": "task-1",
            "title": "Delete me",
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
        }
    )

    response = client.delete("/tasks/task-1")

    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}
    assert fake_collection.tasks == []
