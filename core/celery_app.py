from celery import Celery
from config.settings import settings
from core.utils import auto_discover_apps
from core.apps import app_registry

# Create a Celery instance
celery_app = Celery(
    "praetor_api_worker",
    broker=str(settings.CELERY_BROKER_URL),
    backend=str(settings.CELERY_RESULT_BACKEND),
    include=[],  # We will populate this dynamically
)

# It's crucial to discover the apps first so the registry is populated.
auto_discover_apps()

# Use the app_registry to tell Celery where to find tasks.
# This is the key integration point with your modular architecture.
task_modules = [f"{app_config.module_path}.tasks" for app_config in app_registry.apps]
celery_app.autodiscover_tasks(task_modules)

celery_app.conf.update(task_track_started=True)