import logging

from schemas.user import UserDataSchema
from storages.redis import RedisStorage

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, redis_storage: RedisStorage):
        self.redis_prefix = 'user'
        self.redis_storage = redis_storage

    @property
    def redis(self) -> RedisStorage:
        return self.redis_storage

    def _build_key(self, user_id: int):
        return f'{self.redis_prefix}:{str(user_id)}'

    async def save_user_data(self, user_id: int, user_data: UserDataSchema):
        key = self._build_key(user_id)
        await self.redis.hset(key, user_data.model_dump(exclude_unset=True))

    async def get_user_data(self, user_id: int) -> UserDataSchema | None:
        key = self._build_key(user_id)
        user_data = await self.redis.hget(key)
        if len(user_data.keys()) > 0:
            return UserDataSchema(**user_data)
        return None
