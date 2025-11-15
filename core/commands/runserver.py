import click
import code
import uvicorn
from config.settings import settings

@click.command()
@click.option("--host", default=settings.SERVER_HOST, help="Host to bind.", show_default=True) # type: ignore
@click.option("--port", default=settings.SERVER_PORT, help="Port to bind.", show_default=True) # type: ignore
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload.") # type: ignore
def runserver(host: str, port: int, reload: bool):
    """Starts the development server."""
    uvicorn.run("main:app", host=host, port=port, reload=reload)