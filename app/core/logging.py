import logging
from app.core.config import settings

def setup_logging():
    """Sets up standard structured logging for the application."""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

logger = setup_logging()