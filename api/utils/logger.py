import logging
import sys

# Get logger
logger = logging.getLogger()

# Create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    validate=True,
)

# Create handlers
stream_handler = logging.StreamHandler(sys.stdout)
# file_handler = logging.FileHandler("app.log")

# Set formatter
stream_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# Add handlers to the logger
# logger.handlers = [stream_handler, file_handler]
logger.handlers = [stream_handler]

# Set Log-Level
logger.setLevel(logging.INFO)
