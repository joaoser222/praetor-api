import importlib
from pathlib import Path
from typing import Optional, cast
from fastapi import APIRouter
from config.logging import logger


class BaseAppConfig:
    """
    Base configuration class for an app.

    Each app should have an apps.py file with a class that inherits from this one.
    This class is responsible for loading its own components, such as routers.
    """

    def __init__(self, app_path: Path):
        self.name: str = app_path.name
        self.label: str = self.name.capitalize()
        self.path: Path = app_path
        self.module_path: str = f"apps.{self.name}"
        self._router: Optional[APIRouter] = None

    @property
    def router(self) -> APIRouter:
        """
        Lazily loads and returns the aggregated APIRouter for the app.
        """
        if self._router is None:
            self._router = self._load_router()
        return cast(APIRouter, self._router)

    def _load_router(self) -> APIRouter:
        """
        Discovers and aggregates all APIRouters from the app's 'routers' directory.

        It scans for all .py files in the routers subdirectory, imports them,
        finds any APIRouter instance (conventionally named 'router'), and includes
        it in a main app-level router.
        """
        app_level_router = APIRouter()
        routers_dir = self.path / "routers"

        if not routers_dir.is_dir():
            return app_level_router  # Return empty router if no routers dir

        for router_file in routers_dir.glob("*.py"):
            if router_file.stem.startswith("_"):
                continue

            module_name = f"{self.module_path}.routers.{router_file.stem}"
            try:
                router_module = importlib.import_module(module_name)
                if hasattr(router_module, "router") and isinstance(getattr(router_module, "router"), APIRouter):
                    entity_router = getattr(router_module, "router")
                    app_level_router.include_router(entity_router)
                    logger.debug(f"Router from '{module_name}' included in app '{self.name}'.")
            except ImportError as e:
                logger.error(f"Failed to import router module '{module_name}': {e}")

        return app_level_router
