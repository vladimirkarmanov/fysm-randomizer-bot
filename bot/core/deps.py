import logging
from logging import Logger

from settings import Settings

settings = Settings()


def get_logger() -> Logger:
    return logging.getLogger("bot")


def get_settings() -> Settings:
    return settings
