from loguru import logger
import os

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def custom_format(record):
    name = record["extra"].get("name", "GLOBAL")
    return f"<green>{record['time']:YYYY-MM-DD HH:mm:ss}</green> | <level>{record['level']}</level> | {name} | {record['message']}"

# Remove default logger to prevent duplication
logger.remove()

logger.add(
    os.path.join(LOG_DIR, "booking_api.log"),
    rotation="1 MB",
    retention="7 days",
    level="DEBUG",
    format=custom_format,
    diagnose=False,
    catch=True
)

# Export logger
log = logger
