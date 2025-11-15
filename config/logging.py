import logging
import sys

from config.settings import settings

# Create logger
logger = logging.getLogger(settings.APP_NAME)
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Create console handler and set level
handler = logging.StreamHandler(sys.stdout)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Add formatter to handler
handler.setFormatter(formatter)
logger.addHandler(handler)