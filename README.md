# Task Manager API

A small asynchronous REST API for managing tasks with FastAPI and MongoDB.
The project keeps its structure straightforward while demonstrating validation,
database integration, automated tests, and interactive API documentation.
It requires Python 3.10 or newer.

## Features

- Create tasks with a title and status
- List all tasks or filter them by status
- Update task details
- Delete tasks
- Validate request data with Pydantic
- Access MongoDB asynchronously with Motor
- Explore the API through Swagger UI

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Programming language |
| FastAPI | Web framework |
| MongoDB | Document database |
| Motor | Async MongoDB driver |
| Pydantic | Request and response validation |
| Uvicorn | ASGI server |
| Pytest | Automated testing |
| HTTPX | Test client dependency |
| Python-dotenv | Environment variable loading |

## Project Structure

```text
Task_Manager_API/
|-- database/
|   `-- mongo.py
|-- models/
|   `-- task_model.py
|-- routers/
|   `-- task.py
|-- schemas/
|   `-- task_schema.py
|-- tests/
|   `-- test_api.py
|-- .env.example
|-- .gitignore
|-- LICENSE
|-- main.py
|-- README.md
`-- requirements.txt
```

## Installation

```bash
git clone <repository-url>
cd Task_Manager_API
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source venv/bin/activate`.

## Environment Variables

Copy `.env.example` to `.env`, then update the values if needed:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=task_manager
```

Make sure MongoDB is running before starting the API.

## Running Locally

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

With the server running, open the interactive Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Example API Routes

| Method | Route | Description |
| --- | --- | --- |
| GET | `/` | Return a welcome message |
| GET | `/tasks` | List tasks; optionally filter with `?status=pending` |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

Task statuses can be `pending` or `completed`.

## Running Tests

```bash
pytest -v
```

Tests use a lightweight in-memory fake collection, so MongoDB does not need to
be running during the test suite.

## Future Improvements

- Authentication
- Pagination
- Task search
- Docker deployment

## License

This project is available under the [MIT License](LICENSE).
