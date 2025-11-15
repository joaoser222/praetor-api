from pathlib import Path
from core.base_app_config import BaseAppConfig


class AuthAppConfig(BaseAppConfig):
    """Configuration class for the 'auth' app."""

    # In the future, you could override attributes or add new methods here.
    # For example, to set a custom label for the documentation:
    # label = "Authentication"
    pass


# This instance will be discovered and registered automatically.
app_config = AuthAppConfig(app_path=Path(__file__).parent)