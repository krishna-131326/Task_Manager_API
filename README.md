# Task Manager API

## Project Overview

This is a simple Task Manager API built using **FastAPI** and **MongoDB**. It allows users to keep track of tasks by creating, updating, reading, and deleting them. Each task has a title, status (pending or completed), and the time it was created. The API can be tested using Swagger UI or tools like Postman or curl.


## Features

- Add a new task  
- View all tasks (with optional filtering by status)  
- Update a task's title or status  
- Delete a task  

Each task includes:
- a title
- a status (either "pending" or "completed")
- the date and time when it was created


## Technologies Used

- **FastAPI** – For building the API
- **Motor** – Async MongoDB driver
- **MongoDB** – NoSQL database for storing tasks
- **Pydantic** – For data validation
- **Uvicorn** – ASGI server to run the app
- **python-dotenv** – To load environment variables from `.env` file



## API Routes Documentation

| Method | Route              | Description                       |
|--------|--------------------|-----------------------------------|
| GET    | `/`                | Welcome message                   |
| GET    | `/tasks`           | Get all tasks (optional filter by status) |
| POST   | `/tasks`           | Add a new task                    |
| PUT    | `/tasks/{task_id}` | Update title/status of a task     |
| DELETE | `/tasks/{task_id}` | Delete a task                     |

## Setup Instructions

### 1. Prerequisites

Make sure you have Python 3.8 or above installed on your system.

### 2. Install Required Libraries

Use the following command to install the necessary Python packages:

bash
pip install -r requirements.txt


