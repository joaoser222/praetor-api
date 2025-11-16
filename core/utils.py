from typing import Dict, Any, Optional, List, NamedTuple, Callable
import click
import importlib
from types import ModuleType
from fastapi import FastAPI

from config.settings import settings
from config.logging import logger
from core.apps import app_registry


def auto_discover_apps():
    """
    Automatically discovers and registers all apps from the 'apps' directory.

    This function scans the 'apps' directory, looks for an 'app.py' file
    in each subdirectory, imports the 'app_config' instance, and registers it
    in the global 'app_registry'.
    """
    apps_dir = settings.BASE_DIR / "apps"
    if not apps_dir.is_dir():
        return

    logger.info("Starting automatic app discovery...")
    for app_path in apps_dir.iterdir():
        if not app_path.is_dir() or app_path.name.startswith("_"):
            continue

        app_config_file = app_path / "app.py"
        if app_config_file.is_file():
            module_name = f"apps.{app_path.name}.app"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "app_config"):
                    app_config_instance = getattr(module, "app_config")
                    app_registry.register(app_config_instance)
                    logger.info(f"App '{app_config_instance.name}' registered successfully.")
            except ImportError as e:
                logger.error(f"Failed to import app '{app_path.name}': {e}")


def auto_discover_routers(app: FastAPI, base_prefix: str = "/api"):
    """
    Iterates over the registered AppConfigs and includes their routers in the main FastAPI app.
    """
    logger.info("Loading routers from registered apps...")
    for app_config in app_registry.apps:
        # Accessing .router triggers the lazy loading of the app's router.
        # The property ensures it's loaded only once.
        if app_config.router.routes:
            app.include_router(
                app_config.router,
                prefix=f"{base_prefix}/{app_config.name}",
                tags=[app_config.label],
            )
            logger.info(f"Routes for app '{app_config.name}' loaded.")

def auto_discover_commands(cli, base_dir: str):
    """
    Automatically discover and register all CLI commands from commands directory.
    """
    commands_path = settings.BASE_DIR / base_dir.replace(".", "/")

    def process_command_module(module: ModuleType, module_stem: str):
        # Search for objects from Click (Command or Group)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, (click.Command, click.Group)):
                cli.add_command(attr)

    if not commands_path.is_dir():
        return

    for file in commands_path.glob("*.py"):
        if file.stem.startswith("_"):
            continue
        module_name = f"{base_dir}.{file.stem}"
        module = importlib.import_module(module_name)
        process_command_module(module, file.stem)


def create_from_template(template_env, template_name, target_path, context):
    """Renders a template and writes it to a file."""
    template = template_env.get_template(template_name)
    rendered_content = template.render(context)
    with open(target_path, "w") as f:
        f.write(rendered_content)

def to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase"""
    return ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))


def to_plural(word: str) -> str:
    """
    Convert a word to its plural form following English pluralization rules.
    """
    # Special irregular plurals
    irregular_plurals = {
        'person': 'people',
        'child': 'children',
        'man': 'men',
        'woman': 'women',
        'tooth': 'teeth',
        'foot': 'feet',
        'mouse': 'mice',
        'goose': 'geese',
    }
    
    word_lower = word.lower()
    
    # Check for irregular plurals
    if word_lower in irregular_plurals:
        return irregular_plurals[word_lower]
    
    # Words ending in consonant + y -> ies
    if len(word) > 1 and word[-1] == 'y' and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    
    # Words ending in s, ss, sh, ch, x, z -> es
    if word.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    
    # Words ending in consonant + o -> es
    if len(word) > 1 and word[-1] == 'o' and word[-2] not in 'aeiou':
        return word + 'es'
    
    # Words ending in f or fe -> ves
    if word.endswith('fe'):
        return word[:-2] + 'ves'
    if word.endswith('f'):
        return word[:-1] + 'ves'
    
    # Default: just add s
    return word + 's'

class PermissionDef(NamedTuple):
    name: str
    description: str