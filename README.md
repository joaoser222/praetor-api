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
- Poetry (optional, but recommended) or pip

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
python manage.py runserver --reload
```

Access the API documentation at http://127.0.0.1:8000/docs.

## ⚙️ CLI Commands

The project includes a powerful CLI (`manage.py`) to manage the project. Main commands:

- **Apps**: `make:app`, `make:entity`, `make:command`
- **Database**: `db:create`, `db:migrate`, `db:makemigrations`, `db:rollback`, etc.
- **Authentication**: `auth:createsuperuser`, `auth:makepermissions`
- **Development**: `runserver`, `test`, `shell`

> 💡 **Tip**: For the complete and detailed list of all commands, check the [full commands documentation](docs/COMMANDS.md).

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
│   ├── commands/                # CLI commands
│   │   ├── auth.py              # Authentication commands
│   │   ├── db.py                # Database commands
│   │   ├── make.py              # Code generation commands
│   │   └── shell.py             # Interactive shell
│   └── templates/               # Jinja2 templates for code generation
│       ├── command.py.j2
│       └── entity/
│           ├── model.py.j2
│           ├── schema.py.j2
│           ├── repository.py.j2
│           ├── service.py.j2
│           ├── router.py.j2
│           ├── permission.py.j2
│           └── test.py.j2
│
├── apps/                        # Modular apps (Domain-Driven)
│   └── auth/                    # Authentication app (project's basic structure)
│       ├── models/              # SQLAlchemy models
│       │   ├── user.py
│       │   ├── role.py
│       │   ├── permission.py
│       │   └── token.py
│       ├── schemas/             # Pydantic schemas
│       │   └── user.py
│       ├── repositories/        # Data access layer
│       │   ├── user.py
│       │   └── token.py
│       ├── services/            # Business logic
│       │   └── user.py
│       ├── routers/             # HTTP endpoints
│       │   └── auth.py
│       ├── permissions/         # Permission definitions
│       │   └── user.py
│       ├── tasks.py             # Asynchronous tasks (Celery)
│       ├── dependencies.py      # App-specific dependencies
│       └── tests/               # App tests
│           └── user.py
│
├── migrations/                  # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                # Migration files
│
├── tests/                       # Global tests
│   ├── conftest.py              # pytest fixtures
│   └── __init__.py
│
└── docs/                        # Additional documentation
    ├── APPS.md                  # Apps documentation
    ├── COMMANDS.md              # CLI commands documentation
    ├── MIDDLEWARES.md           # Middlewares documentation
    └── WORKERS.md               # Celery/Workers documentation
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