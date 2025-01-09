from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    CACHE: bool
    ENVIRONMENT: str

    BOT_TOKEN: SecretStr
    DEVELOPER_ID: int
    DEVELOPER_USERNAME: str

    # database
    DATABASE_PATH: str
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_KEY_EX: int
    RATE_LIMIT: int

    # pagination
    ITEMS_PER_PAGE: int

    @property
    def is_dev(self):
        return self.ENVIRONMENT == 'development'

    @property
    def is_prod(self):
        return self.ENVIRONMENT == 'production'


settings = Settings()
