from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import TelegramObject

from core.deps import get_settings
from storages.redis import redis_storage, RedisStorage

settings = get_settings()


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, storage: RedisStorage = redis_storage):
        self.storage = storage

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_key = f'throttling:{event.from_user.id}'

        user_limit = await self.storage.get(user_key)

        if user_limit is not None:
            user_limit = int(user_limit)

            if user_limit == settings.RATE_LIMIT:
                user_limit += 1
                await self.storage.set(key=user_key, value=user_limit, ex=10)
                return await event.answer('Мы обнаружили подозрительную активность. Ждите 10 секунд.')
            elif user_limit > settings.RATE_LIMIT:
                return

            user_limit += 1
            await self.storage.set(key=user_key, value=user_limit, ex=10)

            return await handler(event, data)

        await self.storage.set(key=user_key, value=1, ex=10)
        return await handler(event, data)
