import click
import subprocess

@click.command("run:worker")
@click.option("--loglevel", default="info", help="Logging level for the worker.")
def run_worker(loglevel: str):
    """Starts a Celery worker process."""
    click.echo("Starting Celery worker...")
    # The -A flag points to our Celery app instance.
    command = ["celery", "-A", "core.celery_app.celery_app", "worker", f"--loglevel={loglevel}"]
    subprocess.run(command)