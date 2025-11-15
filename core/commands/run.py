import click
import uvicorn
import subprocess
import pytest
import os
from config.settings import settings

@click.group('run')
def run_cli():
    """ A group of commands intended for operational execution."""
    pass

@run_cli.command('run:server')
@click.option("--host", default=settings.SERVER_HOST, help="Host to bind.", show_default=True) # type: ignore
@click.option("--port", default=settings.SERVER_PORT, help="Port to bind.", show_default=True) # type: ignore
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload.") # type: ignore
def run_server(host: str, port: int, reload: bool):
    """Starts the development server."""
    uvicorn.run("main:app", host=host, port=port, reload=reload)

@run_cli.command("run:worker")
@click.option("--loglevel", default="info", help="Logging level for the worker.")
def run_worker(loglevel: str):
    """Starts a Celery worker process."""
    click.echo("Starting Celery worker...")
    # The -A flag points to our Celery app instance.
    command = ["celery", "-A", "core.celery_app.celery_app", "worker", f"--loglevel={loglevel}"]
    subprocess.run(command)

@run_cli.command('run:test')
@click.argument("app_name", required=False) # type: ignore
def run_test(app_name: str | None):
    """Runs tests, optionally for a specific app."""
    test_path = f"apps/{app_name}/tests" if app_name and os.path.exists(f"apps/{app_name}/tests") else "tests/"
    pytest.main(["-v", test_path])