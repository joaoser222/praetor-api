from typing import List
from .base_app_config import BaseAppConfig

class AppRegistry:
    """A central registry to store AppConfig instances."""

    def __init__(self):
        self.apps: List[BaseAppConfig] = []

    def register(self, app_config: BaseAppConfig):
        """Registers a new app configuration."""
        self.apps.append(app_config)


# Global instance of the app registry, ready to be imported and used.
app_registry = AppRegistry()
