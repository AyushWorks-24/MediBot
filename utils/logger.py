import sys
import os
from loguru import logger


logger.remove()


logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - {message}",
    level="DEBUG",
    colorize=True,
)


os.makedirs("logs", exist_ok=True)

logger.add(
    "logs/medibot.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time} | {level} | {name} - {message}",
)