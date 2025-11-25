import importlib
import os
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy import inspect
from core.utils import to_pascal_case


@click.group("generate")
def generate_cli():
    """Code generation commands."""
    pass


def get_model_attributes(model_class):
    """Inspects a SQLAlchemy model and returns its column attributes with type hints."""
    attributes = {}
    dynamic_imports = {
        "typing": ["Optional"]
    }
    mapper = inspect(model_class).mapper
    for prop in mapper.iterate_properties:
        if isinstance(prop, ColumnProperty):
            column = prop.columns[0]
            python_type = column.type.python_type
            type_name = python_type.__name__
            module_name = python_type.__module__

            # Generate importation of modules of types dynamically
            if(module_name != "builtins"):
                if(not dynamic_imports.get(module_name)):
                    dynamic_imports[module_name] = []
            
                if(type_name not in dynamic_imports[module_name]):
                    dynamic_imports[module_name].append(type_name)

            # Wrap nullable columns in Optional, except for the id.
            # The template handles making fields optional for the Update schema.
            if column.nullable and prop.key != 'id':
                attributes[prop.key] = f"Optional[{type_name}]"
            else:
                attributes[prop.key] = type_name
    return attributes,dynamic_imports


@generate_cli.command("generate:schemas")
@click.argument("entity")
@click.option(
    "--app",
    required=True,
    help="The name of the app where the entity model is located.",
)
@click.option("--force", is_flag=True, help="Force overwrite of existing file without confirmation.")
def generate_schemas(entity: str, app: str, force: bool):
    """
    Generates CRUD Pydantic schemas based on an entity model.

    This command inspects the columns of a SQLAlchemy model and generates
    Create, Update, and Read schemas using Jinja2 templates.
    """

    entity_name_lower = entity.lower()
    entity_name_pascal = to_pascal_case(entity)
    app_path = Path(f"apps/{app}")

    if not app_path.exists():
        click.secho(f"Error: App '{app}' not found at '{app_path}'.", fg="red")
        return

    model_path = app_path / "models" / f"{entity_name_lower}.py"
    if not model_path.exists():
        click.secho(
            f"Error: Model file not found at '{model_path}'.",
            fg="red",
        )
        return

    click.echo(f"Inspecting model '{entity_name_pascal}' in app '{app}'...")

    try:
        # Dynamically import the model class
        module_path = f"apps.{app}.models.{entity_name_lower}"
        module = importlib.import_module(module_path)
        model_class = getattr(module, entity_name_pascal)

        # Get model attributes
        attributes,dynamic_imports = get_model_attributes(model_class)
        click.echo(f"Found attributes: {list(attributes.keys())}")

        # Check if there are any attributes other than the base ones
        user_defined_attributes = {
            k for k in attributes.keys() if k not in ['id', 'created_at', 'updated_at']
        }

        if not user_defined_attributes:
            click.secho(
                f"Warning: Model '{entity_name_pascal}' has no custom attributes to generate schemas from.",
                fg="yellow",
            )
            click.secho("Generation skipped. Please add attributes to your model file.", fg="yellow")
            return
    except (ImportError, AttributeError) as e:
        click.secho(
            f"Error: Could not load model class '{entity_name_pascal}' from '{module_path}'.\n{e}",
            fg="red",
        )
        return
    
    # Setup Jinja2 environment
    template_dir = Path("core/templates/entity")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("schema.py.j2")

    # Prepare context for the template
    context = {
        "class_name": entity_name_pascal,
        "attributes": attributes,
        "dynamic_imports": dynamic_imports
    }

    # Render the template
    rendered_code = template.render(context)

    # Write the generated schema file
    schema_output_path = app_path / "schemas" / f"{entity_name_lower}.py"

    # Check if file already exists and ask for confirmation
    if schema_output_path.exists() and not force:
        click.secho(
            f"Warning: The file '{schema_output_path}' will be overwritten based on the model '{model_path}'.", fg="yellow"
        )
        if not click.confirm("Do you want to overwrite it?"):
            click.echo("Generation skipped.")
            return

    schema_output_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
    schema_output_path.write_text(rendered_code)

    click.secho(
        f"Successfully generated schema file at '{schema_output_path}'.", fg="green"
    )