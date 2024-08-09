from logging import Logger

from core.deps import get_logger, get_settings
from settings import Settings


class BaseStorage:
    def __init__(
        self,
        logger: Logger = get_logger(),
        settings: Settings = get_settings(),
    ):
        self.logger = logger
        self.settings = settings
