from pydantic import SecretStr, DirectoryPath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    CACHE: bool
    ENVIRONMENT: str

    BOT_TOKEN: SecretStr

    # ids
    DEVELOPER_ID: int

    # database
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_KEY_EX: int

    RATE_LIMIT: int

    # media files
    MEDIA_URL: DirectoryPath

    @property
    def is_dev(self):
        return self.ENVIRONMENT == "development"

    @property
    def is_prod(self):
        return self.ENVIRONMENT == "production"
