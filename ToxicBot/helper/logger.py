import logging
import os

MODE = os.environ.get("MODE")
LOG_FILE_NAME = "actions.log"
LOG_FORMAT = "%(asctime)s %(levelname)s || %(message)s"  # Format for logging

MAX_BYTES = 100
BACKUP = 10

# Log Settings

logger = logging.getLogger("")

file_handler = logging.RotatingFileHandler(LOG_FILE_NAME, maxBytes=MAX_BYTES, backup = BACKUP)  # In production log to file
file_handler.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()  # In development, log to console
logger.setLevel(logging.WARNING)

log_format = logging.Formatter("%(asctime)s - %(levelname)s || %(message)s")

console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

if MODE == "PRODUCTION":
    logger.addHandler(file_handler)  # Add the file handler when in production
else:
    logger.addHandler(console_handler)
