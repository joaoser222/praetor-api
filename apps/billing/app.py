from pathlib import Path
from core.base_app_config import BaseAppConfig

class BillingAppConfig(BaseAppConfig):
    """Configuration class for the 'billing' app."""
    pass


# This instance will be discovered and registered automatically.
app_config = BillingAppConfig(app_path=Path(__file__).parent)