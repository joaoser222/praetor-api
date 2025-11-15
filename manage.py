import click
from core.utils import auto_discover_commands

@click.group()
def cli():
    """A command-line interface for managing the application."""
    pass

auto_discover_commands(cli, "commands")
auto_discover_commands(cli, "core.commands")

if __name__ == "__main__":
    cli()