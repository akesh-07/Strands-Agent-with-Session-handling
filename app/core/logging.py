import logging
from app.core.config import settings

import sys

def setup_logging():
    """Sets up standard structured logging for the application without breaking Uvicorn."""
    logger = logging.getLogger("app")
    logger.setLevel(settings.LOG_LEVEL)
    
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        # Console output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File output
        file_handler = logging.FileHandler("log.txt", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    # Prevent propagating up to the root logger which Uvicorn might swallow
    logger.propagate = False 
    
    return logger

logger = setup_logging()