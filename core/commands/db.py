import asyncio
import click
from alembic.config import Config
from alembic import command

from config.database import engine, AsyncSessionFactory
from core.base_model import Base
from config.settings import settings

alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


@click.group('db')
def db_cli():
    """Database management commands."""
    pass


async def _create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@db_cli.command("db:create")
def create():
    """Creates all database tables."""
    click.echo("Creating database tables...")
    asyncio.run(_create_all())
    click.echo("Done.")


async def _drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@db_cli.command("db:drop")
def drop():
    """Drops all database tables."""
    if click.confirm("Are you sure you want to drop all tables?"):
        click.echo("Dropping database tables...")
        asyncio.run(_drop_all())
        click.echo("Done.")


@db_cli.command("db:makemigrations")
@click.option("-m", "--message", required=True, help="Revision message")
def makemigrations(message: str):
    """Creates a new revision file (makemigrations)."""
    click.echo(f"Creating new migration: {message}")
    command.revision(alembic_cfg, message=message, autogenerate=True)


@db_cli.command("db:migrate")
def migrate():
    """Applies all pending migrations."""
    click.echo("Applying migrations...")
    command.upgrade(alembic_cfg, "head")
    click.echo("Migrations applied.")


@db_cli.command("db:rollback")
@click.option("--steps", default=1, help="Number of migrations to rollback.")
def rollback(steps: int):
    """Rolls back migrations."""
    click.echo(f"Rolling back {steps} migration(s)...")
    command.downgrade(alembic_cfg, f"-{steps}")
    click.echo("Rollback complete.")


@db_cli.command("db:reset")
def reset():
    """Resets the database (drops all tables and applies migrations)."""
    if click.confirm(
        "This will delete all data. Are you sure you want to reset the database?"
    ):
        click.echo("Resetting database...")
        asyncio.run(_drop_all())
        command.upgrade(alembic_cfg, "head")
        click.echo("Database has been reset.")


@db_cli.command("db:current")
def current():
    """Shows the current migration revision."""
    command.current(alembic_cfg)


@db_cli.command("db:history")
def history():
    """Shows the migration history."""
    command.history(alembic_cfg)