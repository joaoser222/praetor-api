# Managing Workers with Celery

This document details how to configure, run, and create background tasks using Celery in this project. Celery is used to execute time-consuming operations asynchronously, without blocking the API response.

## What are Workers?

Workers are processes that run continuously, waiting for "tasks" to execute. When your application needs to perform a long operation (such as sending an email, processing a video, generating a complex report), it doesn't execute the task directly. Instead, it sends a message to a queue. The worker picks up this message from the queue and executes the corresponding task in the background.

This allows the API to respond immediately to the user, improving experience and scalability.

## 1. Configuration

Celery configuration is done through environment variables in your `.env` file.

```dotenv
# .env

# ... other settings

# Celery Settings
# The broker is the "mailman" that transports task messages. It's mandatory.
# Redis is a lightweight and common choice for development.
# You can easily start a Redis container with: docker run -d -p 6379:6379 redis
CELERY_BROKER_URL="redis://localhost:6379/0"

# The result backend stores the state and result of tasks.
# For development, you can use SQLite to avoid an extra dependency.
# For production, Redis or a dedicated database is recommended.
CELERY_RESULT_BACKEND="db+sqlite:///celery_results.db"
```

-   **`CELERY_BROKER_URL`**: The URL of the message broker system. This is a requirement for Celery to work. Redis is the default and recommended option for development.
-   **`CELERY_RESULT_BACKEND`**: The URL of the backend that stores the state and results of tasks. The example uses a SQLite database (`celery_results.db` will be created in the project root) to simplify the development environment.

## 2. Running the Worker

To start a worker that will listen for new tasks, run the following command from your project root:

```bash
celery -A core.celery_app worker --loglevel=info
```

-   `-A core.celery_app`: Points to the Celery instance, which is in the `core/celery_app.py` file.
-   `worker`: Tells Celery we want to start a worker process.
-   `--loglevel=info`: Sets the log level to `INFO`, useful for seeing tasks being received and executed.

You'll see output in the terminal indicating that the worker is ready to receive tasks.

## 3. Creating a New Task

Thanks to the auto-discovery system and code generators, creating and registering a new task is very simple.

1.  When creating a new app with `python manage.py make:app <app_name>`, a `tasks.py` file is automatically created inside the app directory.
2.  Open the `apps/<app_name>/tasks.py` file.
3.  Use the `@celery_app.task` decorator to define your function as a task, following the example below.

**Example: `apps/notifications/tasks.py`**

```python
import time
from core.celery_app import celery_app
from config.logging import logger

@celery_app.task(name="notifications.send_email")
def send_email_task(recipient: str, subject: str, message: str):
    """
    An example task that simulates sending an email.
    """
    logger.info(f"Sending email to {recipient} with subject '{subject}'...")
    # Simulates a time-consuming operation
    time.sleep(5)
    logger.info(f"Email to {recipient} sent successfully!")
    return f"Email sent to {recipient}"
```

The Celery worker will find this task automatically the next time it's started.

## 4. Calling a Task in the Application

To execute a background task from your API endpoint, import the task function and call it with the `.delay()` method.

**Example: `apps/notifications/routers/notifications.py`**

```python
from fastapi import APIRouter, BackgroundTasks
from ..tasks import send_email_task

router = APIRouter()

@router.post("/send-test-email")
def send_test_email(email_to: str):
    """
    Endpoint to queue an email sending task.
    The response is immediate.
    """
    # Sends the task to the Celery queue and returns immediately
    task = send_email_task.delay(email_to, "Test Subject", "This is a test message.")
    
    return {"message": "Email sending task queued successfully!", "task_id": task.id}
```

When accessing this endpoint, the API will respond instantly, and you'll see the task log message appearing in the terminal where the worker is running after 5 seconds.