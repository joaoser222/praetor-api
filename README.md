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

## 📁 Project Structure

```
praetor-api/
├── main.py                      # Main FastAPI application
├── manage.py                    # CLI to manage the project
├── requirements.txt             # Project dependencies
├── alembic.ini                  # Alembic configuration
│
├── config/                      # Centralized configuration
│   ├── settings.py              # Settings with Pydantic
│   ├── database.py              # SQLAlchemy setup
│   ├── security.py              # JWT, password hashing
│   └── logging.py               # Logging configuration
│
├── core/                        # Base classes and utilities
│   ├── base_model.py            # Base SQLAlchemy + TimestampMixin
│   ├── base_repository.py       # Generic Repository Pattern
│   ├── base_service.py          # Base Service Layer

│   ├── exceptions.py            # Custom HTTP exceptions
│   ├── dependencies.py          # Global dependencies
│   ├── celery_app.py            # Celery instance and configuration
│   ├── middlewares/             # Custom middlewares
│   ├── utils.py                 # Auto-discovery of routes/commands
│   ├── cli.py                   # Main CLI
│   ├── commands/                # CLI Core commands
│   └── templates/               # Jinja2 templates for code generation
│
├── apps/                        # Modular apps (Domain-Driven)
│   └── {app_name}/              # App directory
│       ├── models/              # SQLAlchemy models
│       ├── schemas/             # Pydantic schemas
│       ├── repositories/        # Data access layer
│       ├── services/            # Business logic
│       ├── routers/             # HTTP endpoints
│       ├── permissions/         # Permission definitions
|       ├── tests/               # App tests
│       ├── tasks.py             # Asynchronous tasks (Celery)
│       ├── app.py               # Base class app
│       └── dependencies.py      # App-specific dependencies
│       
│
├── migrations/                  # Alembic migrations
│
└── tests/                       # Global tests

```

## 🏛️ Architecture

The project follows a layered architecture to ensure separation of concerns:

1. **Router (`routers/`)**: The outermost layer, responsible for receiving HTTP requests, validating input data (using `schemas/`) and calling the service layer.
2. **Service (`services/`)**: Contains the application's business logic. Orchestrates operations, using one or more repositories to interact with the database.
3. **Repository (`repositories/`)**: Responsible for data access and manipulation in the database. Abstracts SQL/ORM queries, exposing clear methods to the service layer.
4. **Model (`models/`)**: Defines the database table structure using SQLAlchemy ORM.

### Auto-Discovery

The system has automatic discovery of:
- **Routes**: All `APIRouter` in `apps/*/routers/*.py` are automatically registered with prefix `/api/<app_name>`
- **CLI Commands**: Commands in `core/commands/` are automatically discovered and registered

> 💡 **Tip**: For more details about app architecture, app structure, Base Classes, and how to create new apps, check the [apps documentation](docs/APPS.md).

## 📦 Creating Apps and Entities

To add new functionality, you can create a new app:

```bash
python manage.py make:app posts
```

After creating an app, you can generate complete entities within it:

```bash
python manage.py make:entity post --app posts
```

> 💡 **Tip**: For more details about creating apps, entities, app structure, and permission system, check the [apps documentation](docs/APPS.md).

## 🛠️ Additional Features

### Custom Exceptions

The project provides custom HTTP exceptions:
- `NotFoundException` (404)
- `ValidationException` (422)
- `UnauthorizedException` (401)
- `ForbiddenException` (403)

All inherit from `BaseAPIException` and are automatically handled by FastAPI.

### Logging

The logging system is configured and includes:
- HTTP request logging middleware (method, path, status, duration)
- Configurable logger via settings
- Standardized log formatting

## 📚 Additional Documentation

- [Apps Documentation](docs/APPS.md): Details about the modular app architecture
- [Commands Documentation](docs/COMMANDS.md): Complete guide of available CLI commands
- [Middlewares](docs/MIDDLEWARES.md): How middlewares work
- [Celery Workers](docs/WORKERS.md): How to configure and use background tasks