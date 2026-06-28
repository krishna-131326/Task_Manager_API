from fastapi import FastAPI

from routers.task import router as task_router

app = FastAPI(title="Task Manager API", version="1.0.0")


@app.get("/", tags=["Home"], summary="API welcome message")
async def home() -> dict[str, str]:
    return {"message": "Welcome to the Task Manager!"}


app.include_router(task_router)
