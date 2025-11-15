# PraetorAPI: FastAPI Modular Boilerplate

A complete and modular boilerplate for FastAPI, inspired by Django architecture, focused on scalability and maintainability.

## ✨ Features

- **Modular Structure**: Organizes the project into independent "apps", just like Django.
- **Powerful CLI**: A `manage.py` with `click` to manage the project (create apps, migrations, users, etc.).
- **Layered Architecture**: Clear separation of concerns with Repository Pattern and Service Layer.
- **Async by Default**: Fully compatible with Python's `async`/`await`.
- **Database**: Integration with SQLAlchemy and Alembic for migrations.
- **Authentication**: Ready-to-use JWT authentication system (Access & Refresh tokens).
- **Permission System**: Complete permissions and roles system (RBAC) with automatic synchronization.
- **Centralized Configuration**: Settings managed with Pydantic for validation and security.
- **Integrated Tests**: Test structure with `pytest` and ready-made fixtures.
- **Code Templates**: Automatic code generation for new apps and entities with Jinja2 templates.
- **Auto-Discovery**: Automatic discovery of routes and CLI commands, no manual registration needed.
- **Base Classes**: Reusable base classes (BaseRepository, BaseService, TimestampMixin) to accelerate development.
- **Background Tasks**: Celery integration to execute time-consuming tasks asynchronously.
- **Custom Exceptions**: Custom HTTP exception system for consistent error handling.
- **Integrated Logging**: Configured logging system with middleware for request tracking.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- pip

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd project_root

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure your environment variables
cp .env.example .env
```

Edit the `.env` file with your database settings and security keys.

### 3. Database Setup

```bash
# Create the database (if it doesn't exist yet)
# python manage.py db create

# Apply migrations
python manage.py db:migrate
```

### 4. Create a Superuser

```bash
python manage.py auth:createsuperuser
```

### 5. Run the Server

```bash
python manage.py run:server --reload
```


## 📁 Project Structure

```
praetor-api/
├── main.py                      # Main FastAPI application
├── manage.py                    # CLI to manage the project
├── requirements.txt             # Project dependencies
├── alembic.ini                  # Alembic configuration
│
├── config/                      # Centralized configuration
├── core/                        # Base classes and utilities
│   ├── exceptions.py            # Custom HTTP exceptions
│   ├── dependencies.py          # Global dependencies
│   ├── celery_app.py            # Celery instance and configuration
│   ├── middlewares/             # Core middlewares
│   ├── commands/                # CLI Core commands
│   └── templates/               # Jinja2 templates for code generation
│
├── apps/                        # Modular apps (Domain-Driven)
├── migrations/                  # Alembic migrations
└── tests/                       # Global tests

```

## 🏛️ Architecture

The project is organized into **apps**, which are independent Python modules located inside the `apps/` directory. Each app is responsible for a specific functionality within the application domain (e.g., `gateway`, `billing`).

This approach offers several benefits:
- **Organization:** Code related to a functionality is grouped in a single location.
- **Reusability:** Well-defined apps can be more easily reused in other projects.
- **Maintainability:** It's easier to understand, debug, and modify isolated functionality.

### Project's Core Apps

The project comes with the **`auth`** app pre-configured, which is a basic and fundamental structure of the boilerplate. This app provides:

- Complete authentication system (JWT + Refresh Tokens)
- User, roles, and permissions management
- Registration, login, logout, and refresh token endpoints
- Integrated RBAC (Role-Based Access Control) system

### Base Classes

The project provides base classes to accelerate development:

- **`BaseRepository`**: Generic repository with CRUD methods (`get`, `get_multi`, `create`, `update`, `delete`, `get_by_field`)
- **`BaseService`**: Base service with utility methods (`commit`, `rollback`, `refresh`)
- **`TimestampMixin`**: Mixin to automatically add `created_at` and `updated_at` to models
- **`BaseAPIException`**: Base class for custom HTTP exceptions

### Auto-Discovery

The system has automatic discovery of:
- **Routes**: All `APIRouter` in `apps/*/routers/*.py` are automatically registered with prefix `/api/<app_name>`
- **CLI Commands**: Commands in `commands/` are automatically discovered and registered

## Creating a New App
To ensure consistency across apps, we use a command to generate the basic structure of a new app from templates.
To create a new app, run the following command from the project root:

```bash
python manage.py make:app <app_name>
```

For example, to create an app to manage products:

```bash
python manage.py make:app products
```

This will create the `apps/products/` folder with all the necessary file structure. There's no need for route registration as it's automatically discovered by the framework. The default prefix is `/api/products`.

### Creating Entities within an App

After creating an app, you can generate complete entities (model, schema, repository, service, router, permission, and test) using:

```bash
python manage.py make:entity <entity_name> --app <app_name>
```

For example, to create the `post` entity inside the `posts` app:

```bash
python manage.py make:entity post --app posts
```

This will create all necessary files for the `post` entity within the `posts` app, using Jinja2 templates located in `core/templates/entity/`:

- `models/post.py` - SQLAlchemy model
- `schemas/post.py` - Pydantic schemas
- `repositories/post.py` - Repository with CRUD
- `services/post.py` - Service with business logic
- `routers/post.py` - Router with HTTP endpoints
- `permissions/post.py` - Permission definitions
- `tests/post.py` - Entity tests

### App Structure

Each app follows this organizational structure:

```
apps/
└── <app_name>/
    ├── models/          # SQLAlchemy models
    ├── repositories/    # Data access layer
    ├── schemas/         # Pydantic schemas for validation
    ├── services/        # Business logic
    ├── routers/         # HTTP endpoints
    ├── permissions/     # Permission definitions
    ├── tasks.py         # Asynchronous tasks (Celery)
    ├── dependencies.py  # App-specific dependencies
    ├── app.py           # Base config class of the app.
    └── tests/           # App tests
```

### Internal App Architecture

Each generated app follows a well-defined layered architecture:

- **`routers/`**: **API Layer**. Defines HTTP endpoints, validates input and output data with `schemas`, and calls the `service` layer.
- **`services/`**: **Business Logic Layer**. Orchestrates operations and business rules. It's the app's "brain".
- **`repositories/`**: **Data Access Layer**. Abstracts communication with the database, executing CRUD operations. Inherits from `BaseRepository` which provides generic CRUD methods.
- **`models/`**: **Data Model Layer**. Defines database table structure using SQLAlchemy. Can use `TimestampMixin` to automatically add `created_at` and `updated_at` fields.
- **`schemas/`**: **Validation Layer**. Defines the "shape" of API data using Pydantic, for validation and serialization.
- **`permissions/`**: Contains app-specific permission definitions.
- **`dependencies.py`**: Contains dependency injection functions specific to the app.
- **`app.py`**: Basic config class of the app.
- **`tests/`**: Contains unit and integration tests for the app.

### Permission System

The project includes a complete permissions and roles system (RBAC - Role-Based Access Control):

- **Permissions**: Granular permissions defined in `apps/*/permissions/*.py`
- **Roles**: Groups of permissions that can be assigned to users
- **Synchronization**: Use `python manage.py auth:makepermissions` to synchronize code permissions with the database

Permissions are automatically discovered and can be checked at endpoints through dependencies. Each app can define its own permissions in the `permissions/` directory, and they will be automatically synchronized with the database when the sync command is executed.

## ⚙️ CLI Commands

The project includes a powerful CLI (`manage.py`) to manage the project. Main commands:


This project comes with a powerful command-line interface (CLI), `manage.py`, built with the Click library. It provides a set of commands to assist with development, database management, and other routine tasks.

Here's a list of all available commands and their functions. To see all options for a command, you can use `python manage.py <command> --help`.

### Development

**`python manage.py run:server`**
Starts the Uvicorn development server.
- `--host`: The host address to use (default: `127.0.0.1`).
- `--port`: The port to use (default: `8000`).
- `--reload`: Enables automatic reload when files are changed.

**`python manage.py test [app_name]`**
Runs tests with `pytest`.
- `app_name` (optional): If provided, runs only tests inside the `apps/<app_name>/tests` folder. Otherwise, runs all tests.

**`python manage.py shell`**
Opens an interactive Python shell with the application context loaded.
- If `IPython` is installed, it will be used automatically (better experience).
- Otherwise, uses the standard Python shell.
- Useful for testing code, debugging, and exploring the application interactively.

### Code Generation (`make`)

**`python manage.py make:app <name>`**
Creates a new modular app inside the `apps/` directory.
- `<name>`: The name of the new app (e.g., `products`).

**`python manage.py make:entity <name> --app <app>`**
Creates a new complete entity (model, schema, repository, service, router, permission, test) inside an existing app.
- `<name>`: The name of the entity (e.g., `post`).
- `--app <app>`: The name of the app where the entity will be created (required).

Example:
```bash
python manage.py make:entity post --app posts
```

This will create all necessary files for the entity using Jinja2 templates located in `core/templates/entity/`.

**`python manage.py make:command <name>`**
Creates a new custom command file in the `core/commands/` directory.
- `<name>`: The name of the new command (e.g., `reports`).

### Database (`db:`)

**`python manage.py db:create`**
Creates all tables in the database based on your SQLAlchemy models (if supported by the driver).

**`python manage.py db:drop`**
Drops all tables from the database. Asks for confirmation.

**`python manage.py db:makemigrations -m "<message>"`**
Creates a new Alembic migration file based on detected changes in your models.
- `-m "<message>"`: A descriptive message for the migration.

**`python manage.py db:migrate`**
Applies all pending migrations to the database.

**`python manage.py db:rollback --steps <n>`**
Reverts a specific number of migrations.
- `--steps <n>`: The number of migrations to revert (default: 1).

**`python manage.py db:reset`**
Completely resets the database (drop all + migrate). Asks for confirmation.

**`python manage.py db:current`**
Shows the current migration revision.

**`python manage.py db:history`**
Displays the migration history.

### Authentication and Users (`auth:`)

**`python manage.py auth:createsuperuser`**
Creates a new superuser interactively, asking for email, username, name, and password.

**`python manage.py auth:makepermissions`**
Discovers and synchronizes permissions defined in each app's `permissions/*.py` files with the database.

---


## Celery Workers

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
