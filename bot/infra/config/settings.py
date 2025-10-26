from functools import lru_cache
from zoneinfo import ZoneInfo

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    CACHE: bool
    ENVIRONMENT: str
    TZ: str

    BOT_TOKEN: SecretStr
    DEVELOPER_ID: int
    DEVELOPER_USERNAME: str

    # database
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_KEY_EX: int
    RATE_LIMIT: int = Field(default=15, ge=1)

    # pagination
    ITEMS_PER_PAGE: int = Field(default=5, ge=1, le=10)

    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == 'development'

    @property
    def is_prod(self) -> bool:
        return self.ENVIRONMENT == 'production'

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.TZ)

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
