from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from utils.auth import is_user_admin


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ) -> Any:
        if await is_user_admin(event.from_user.id):
            return await handler(event, data)
