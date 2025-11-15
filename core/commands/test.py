import click
import pytest
import os

@click.command()
@click.argument("app_name", required=False) # type: ignore
def test(app_name: str | None):
    """Runs tests, optionally for a specific app."""
    test_path = f"apps/{app_name}/tests" if app_name and os.path.exists(f"apps/{app_name}/tests") else "tests/"
    pytest.main(["-v", test_path])