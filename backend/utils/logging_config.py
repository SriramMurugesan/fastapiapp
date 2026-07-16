import logging
import sys
import os

# Configure logging path
LOG_FILE = "app.log"

# Define logging format
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def setup_logging():
    """
    Configure root logging settings.
    Logs will output to both the console and a file named app.log.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if setup is called multiple times
    if logger.handlers:
        return logger

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.info("Logging successfully initialized. Outputs configured to Console and file: %s", os.path.abspath(LOG_FILE))
    return logger

def get_logger(name: str):
    """
    Get a sub-logger for a specific module.
    """
    return logging.getLogger(name)
