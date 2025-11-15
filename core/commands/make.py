import click
import os
from jinja2 import Environment, FileSystemLoader
from core.utils import create_from_template
from config.settings import settings


def _load_template_env():
    # Setup Jinja2 environment
    template_path = os.path.join(settings.BASE_DIR, "core", "templates")
    return Environment(loader=FileSystemLoader(template_path))

@click.group('make')
def make_cli():
    """A group of commands to generate boilerplate code."""
    pass

@make_cli.command("make:app")
@click.argument("name")
def make_app(name: str):
    """Creates a new app with a default structure."""
    app_dir = os.path.join(settings.BASE_DIR, "apps", name)
    env = _load_template_env()

    if os.path.exists(app_dir):
        click.secho(f"App '{name}' already exists.", fg="yellow")
        return
    
    # Create app directory
    os.makedirs(app_dir)

    # Create __init__.py file in app directory
    open(os.path.join(app_dir, "__init__.py"), "w").close()
    
    # Create app.py file in app directory
    create_from_template(env, 'app.py.j2', os.path.join(app_dir, "app.py"), {"name": name})

    # Create tasks.py file in app directory
    create_from_template(env, 'tasks.py.j2', os.path.join(app_dir, "tasks.py"), {"name": name})

    # Create dependencies.py file in app directory
    create_from_template(env, 'dependencies.py.j2', os.path.join(app_dir, "dependencies.py"), {"name": name})

    # Create app base directories
    for subdir in ["repositories", "services", "models", "schemas","tests", "routers", "permissions"]:
        path = os.path.join(app_dir, subdir)
        os.makedirs(path)
        open(os.path.join(path, "__init__.py"), "w").close()
    
    click.secho(f"App '{name}' created successfully in '{app_dir}'.", fg="green")
    click.echo("The app router will be automatically discovered.")
    click.echo(f"Now, you can create an entity inside it with: python manage.py make:entity <entity_name> --app {name}")


@make_cli.command("make:entity")
@click.argument("name")
@click.option("--app", required=True, help="The app where the entity will be created.")
def make_entity(name: str, app: str):
    """Creates a new entity (model, schema, repo, service) inside an app."""
    app_dir = os.path.join(settings.BASE_DIR, "apps", app)
    env = _load_template_env()

    if not os.path.exists(app_dir):
        click.secho(f"App '{app}' not found. Please create it first with 'make:app {app}'.", fg="red")
        return

    context = {
        "name": name,
        "class_name": name.capitalize(),
        "model_name": name.capitalize(),
        "schema_name": name.capitalize(),
        "repo_name": f"{name.capitalize()}Repository",
        "service_name": f"{name.capitalize()}Service",
    }

    # Files to generate for the entity
    template_files = {
        "entity/model.py.j2": f"models/{name}.py",
        "entity/schema.py.j2": f"schemas/{name}.py",
        "entity/repository.py.j2": f"repositories/{name}.py",
        "entity/service.py.j2": f"services/{name}.py",
        "entity/permission.py.j2": f"permissions/{name}.py",
        "entity/router.py.j2": f"routers/{name}.py",
        "entity/test.py.j2": f"tests/{name}.py",
    }

    init_files = {
        "models":  context["model_name"],
        "schemas": context["schema_name"],
        "repositories": context["repo_name"],
        "services": context["service_name"]
    }

    for template_file, target_file in template_files.items():
        target_path = os.path.join(app_dir, target_file)
        create_from_template(env, template_file, target_path, context)
    
    # Update importation of modules
    for init_directory, importation_class in init_files.items():
        target_dir = os.path.join(app_dir, init_directory)
        init_file = os.path.join(target_dir, "__init__.py")
        import_line = f"from .{name} import {importation_class}\n"
        with open(init_file, "a") as f:
            f.write(import_line)

    click.secho(f"Entity '{name}' created successfully in app '{app}'.", fg="green")

@make_cli.command("make:command")
@click.argument("name")
def make_command(name: str):
    """Creates a new custom command file in the root commands/ directory."""
    command_root = os.path.join(settings.BASE_DIR, "commands")
    command_path = os.path.join(command_root, f"{name}.py")
    env = _load_template_env()

    # Create commands directory if nos exists
    if not os.path.exists(command_root):
        os.makedirs(command_root)
        open(os.path.join(command_root, f"__init__.py"), "w").close()

    if os.path.exists(command_path):
        click.echo(f"Command file 'commands/{name}.py' already exists.")
        return
    
    create_from_template(env, "command.py.j2", command_path, {"name": name})

    click.secho(f"Command file 'commands/{name}.py' created successfully.", fg="green")

@make_cli.command("make:middleware")
@click.argument("name")
def make_middleware(name: str):
    """Creates a new middleware file in the root middlewares/ directory."""
    
    middleware_root = os.path.join(settings.BASE_DIR, "middlewares")
    middleware_path = os.path.join(middleware_root, f"{name}.py")
    env = _load_template_env()

    # Create commands directory if nos exists
    if not os.path.exists(middleware_root):
        os.makedirs(middleware_root)
        open(os.path.join(middleware_root, f"__init__.py"), "w").close()

    if os.path.exists(middleware_path):
        click.echo(f"Middleware file 'middlewares/{name}.py' already exists.")
        return

    create_from_template(env, "middleware.py.j2", middleware_path, {"name": name})

    click.secho(f"Middleware file 'middlewares/{name}.py' created successfully.", fg="green")
