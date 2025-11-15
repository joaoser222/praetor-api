# Apps Structure and Functionality

This document describes how the modular "apps" architecture works in this project, how to create new apps, and how they are integrated into the main application.

## The Concept of Modular Apps

The project is organized into **apps**, which are independent Python modules located inside the `apps/` directory. Each app is responsible for a specific functionality within the application domain (e.g., `users`, `products`, `orders`).

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

This app serves as a reference implementation and demonstrates how to structure other apps following the project's standards. You can create additional new apps using the `make:app` command as needed.

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

## App Structure

Each app follows this organizational structure:

```
apps/
└── <app_name>/
    ├── __init__.py
    ├── models/          # SQLAlchemy models
    ├── repositories/    # Data access layer
    ├── schemas/         # Pydantic schemas for validation
    ├── services/        # Business logic
    ├── routers/         # HTTP endpoints
    ├── permissions/     # Permission definitions
    ├── tasks.py         # Asynchronous tasks (Celery)
    ├── dependencies.py  # App-specific dependencies
    └── tests/           # App tests
```

## Internal App Architecture

Each generated app follows a well-defined layered architecture:

- **`routers/`**: **API Layer**. Defines HTTP endpoints, validates input and output data with `schemas`, and calls the `service` layer.
- **`services/`**: **Business Logic Layer**. Orchestrates operations and business rules. It's the app's "brain".
- **`repositories/`**: **Data Access Layer**. Abstracts communication with the database, executing CRUD operations. Inherits from `BaseRepository` which provides generic CRUD methods.
- **`models/`**: **Data Model Layer**. Defines database table structure using SQLAlchemy. Can use `TimestampMixin` to automatically add `created_at` and `updated_at` fields.
- **`schemas/`**: **Validation Layer**. Defines the "shape" of API data using Pydantic, for validation and serialization.
- **`permissions/`**: Contains app-specific permission definitions.
- **`dependencies.py`**: Contains dependency injection functions specific to the app.
- **`tests/`**: Contains unit and integration tests for the app.

### Base Classes

The project provides base classes to accelerate development:

- **`BaseRepository`**: Generic repository with CRUD methods (`get`, `get_multi`, `create`, `update`, `delete`, `get_by_field`)
- **`BaseService`**: Base service with utility methods (`commit`, `rollback`, `refresh`)
- **`TimestampMixin`**: Mixin to automatically add `created_at` and `updated_at` to models
- **`BaseAPIException`**: Base class for custom HTTP exceptions

## Automatic Route Registration (Auto-Discovery)

One of the most powerful features of this boilerplate is **automatic route registration**.

The `main.py` file contains an `auto_discover_routers(app)` function that runs at initialization. This function does the following:

1. Scans all subdirectories inside the `apps/` folder.
2. For each directory (app) found, it looks for a `router.py` file.
3. If `router.py` exists and contains an `APIRouter` object called `router`, it's automatically included in the main FastAPI application.

**What does this mean in practice?**

> You **don't need** to manually add `app.include_router(...)` in `main.py` every time you create a new app. Just create the app with the `make:app` command and the system will take care of the rest.

The URL prefix will be, by default, `/api/<app_name>`, and the tags for Swagger/OpenAPI documentation will be the capitalized app name (e.g., "Products").

## Comparison with Django

For developers with Django experience, this architecture will feel familiar, as it was directly inspired by its modularity principles. However, there are some important differences in implementation and philosophy.

| Concept | Django | This Boilerplate (FastAPI) | Notes |
| :--- | :--- | :--- | :--- |
| **App Creation** | `python manage.py startapp` | `python manage.py make:app` | Similar to Django, but generates a more opinionated structure with service and repository layers. |
| **Data Models** | `models.py` (with Django ORM) | `models.py` (with SQLAlchemy) | The concept is identical: define database structure in Python. |
| **Routes/Views** | `views.py` + `urls.py` | `router.py` | The `router.py` combines the responsibilities of defining endpoint logic (like in `views.py`) and the route (like in `urls.py`) using decorators (`@router.get`). |
| **Validation/Serialization** | `forms.py` or `serializers.py` (DRF) | `schemas.py` (with Pydantic) | Pydantic is native to FastAPI and uses type hints for validation, being more modern and integrated with the ecosystem. |
| **Business Logic** | In `views.py` or Models ("Fat Models") | `service.py` | This boilerplate **formalizes** the service layer, encouraging complex business logic to be separated from HTTP endpoints. |
| **Data Access** | Django ORM (e.g., `Model.objects.all()`) | `repository.py` | The Repository pattern is explicitly implemented to abstract database queries, while in Django access is made directly through `Model.objects`. |
| **Route Registration** | Manual inclusion in `project/urls.py` | Auto-discovery in `main.py` | The boilerplate eliminates the need to manually register routes for each new app. |

### Main Philosophical Difference

While Django offers flexibility about where to place business logic (views, models, etc.), this boilerplate is more **opinionated** and promotes strict layer separation from the start:

- **`router.py`**: HTTP only.
- **`service.py`**: Business logic only.
- **`repository.py`**: Database access only.

This separation aims to improve testability and maintainability of complex applications in the long term.

## Permission System

The project includes a complete permissions and roles system (RBAC - Role-Based Access Control):

- **Permissions**: Granular permissions defined in `apps/*/permissions/*.py`
- **Roles**: Groups of permissions that can be assigned to users
- **Synchronization**: Use `python manage.py auth:sync-permissions` to synchronize code permissions with the database

Permissions are automatically discovered and can be checked at endpoints through dependencies. Each app can define its own permissions in the `permissions/` directory, and they will be automatically synchronized with the database when the sync command is executed.