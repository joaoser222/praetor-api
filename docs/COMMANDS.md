# Managing the Application with CLI (manage.py)

This project comes with a powerful command-line interface (CLI), `manage.py`, built with the Click library. It provides a set of commands to assist with development, database management, and other routine tasks.

## Available Commands

Here's a list of all available commands and their functions. To see all options for a command, you can use `python manage.py <command> --help`.

### Development

**`python manage.py runserver`**
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
- The generated structure includes directories for `models`, `schemas`, `routers`, `services`, `repositories`, `permissions`, `tests`, and the `app.py` and `tasks.py` files.

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
Discovers and synchronizes permissions defined in each app's `permissions.py` files with the database.

---

## How to Extend the CLI with New Commands

Adding your own commands is a simple and organized process, thanks to auto-discovery.

### Step 1: Create the Command File

Use the `make:command` command to create a new command file.

```bash
python manage.py make:command reports
```
This will create the `commands/reports.py` file.

### Step 2: Write the Command Logic with Click

Inside your new file, use Click decorators to define your command. The command name should be explicit.

```python
# commands/reports.py
import click

@click.group()
def reports_cli():
    """Commands to generate reports."""
    pass

@reports_cli.command("reports:sales")
@click.option("--month", required=True, help="Month to generate sales report (e.g., '2023-10').")
def generate_sales_report(month: str):
    """Generates a sales report for a specific month."""
    click.echo(f"Generating sales report for month: {month}...")
    # ... logic to generate the report ...
    click.secho("Report generated successfully!", fg="green")
```

Done! Now you can run `python manage.py reports:sales --month "2023-11"` in your terminal.