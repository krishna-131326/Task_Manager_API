from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Task Manager")

client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_NAME", "FES")]
tasks_collection = db["Data"]

class TaskInput(BaseModel):
    title: str
    status: str

    def validate(self):
        if self.status.lower() not in ["pending", "completed"]:
            raise HTTPException(status_code=400, detail="Status must be pending or completed")
        if not self.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        return self.title.strip(), self.status.lower()

class TaskOutput(BaseModel):
    id: Optional[str]
    title: str
    status: str
    created_at: datetime

def to_task_dict(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "status": task["status"],
        "created_at": task["created_at"]
    }

@app.get("/")
def home():
    return {"message": "Welcome to the Task Manager!"}

@app.get("/tasks", response_model=List[TaskOutput])
async def read_tasks(status: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status.lower()
    results = tasks_collection.find(query)
    return [to_task_dict(task) async for task in results]

@app.post("/tasks", response_model=TaskOutput)
async def add_task(data: TaskInput):
    title, status = data.validate()
    task = {
        "title": title,
        "status": status,
        "created_at": datetime.utcnow()
    }
    result = await tasks_collection.insert_one(task)
    saved = await tasks_collection.find_one({"_id": result.inserted_id})
    return to_task_dict(saved)

@app.put("/tasks/{task_id}", response_model=TaskOutput)
async def update_task(task_id: str, data: TaskInput):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    title, status = data.validate()
    updated = await tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"title": title, "status": status}}
    )
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    return to_task_dict(task)

@app.delete("/tasks/{task_id}")
async def remove_task(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    deleted = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
