import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "task_manager")
COLLECTION_NAME = "tasks"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
tasks_collection = database[COLLECTION_NAME]
