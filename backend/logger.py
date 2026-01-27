import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from backend.config import Config  

load_dotenv() 
print("APP_ENV LIDO NO LOGGER:", os.getenv("APP_ENV"))


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

APP_ENV = os.getenv("APP_ENV", "development")


def setup_logger():
    logger = logging.getLogger("app")

    # 🔥 IMPORTANTE: evita propagação para o root logger
    logger.propagate = False

    # Remove handlers existentes (Werkzeug / Flask)
    if logger.handlers:
        logger.handlers.clear()

    # 🔹 nível base do logger
    if APP_ENV == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # 🔸 Arquivo
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 🔸 Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if APP_ENV == "production":
        console_handler.setLevel(logging.WARNING)
    else:
        console_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger



logger = setup_logger()
