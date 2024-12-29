from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from core.container import container
from settings import settings
from storages.base import BaseStorage


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        self.storage = container.resolve(BaseStorage)

    async def __call__(
        self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
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
