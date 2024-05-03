from pathlib import Path

from environs import Env
from loguru import logger

ENV = Env()
ENV.read_env()

BASE_DIR = Path(__file__).parent
DEBUG_MODE = ENV.bool("DEBUG_MODE")
DB_NAME = ENV.str("DB_NAME")
DB_URL = f"sqlite:///{BASE_DIR}/{DB_NAME}.sqlite3"
PROMT_1 = (" " + ENV.str("PROMT_1")).rstrip()
PROMT_2 = (" " + ENV.str("PROMT_2")).rstrip()

with ENV.prefixed("CHATGPT_"):
    CHATGPT_API_KEY = ENV.str("API_KEY")
    CHATGPT_MAX_TOKENS = ENV.int("MAX_TOKENS")
    CHATGPT_MODEL_ENGINE = ENV.str("MODEL_ENGINE")
    CHATGPT_TEMPERATURE = ENV.float("TEMPERATURE")

logger.add(
    f"logs/{BASE_DIR.stem}.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 day",
    retention="7 days")
