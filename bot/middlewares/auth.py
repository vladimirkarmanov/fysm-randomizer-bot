from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import TelegramObject

from core.deps import get_settings
from utils.auth import is_user_chat_member, is_user_admin

settings = get_settings()


class IsChatMemberMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await is_user_chat_member(event.from_user.id):
            return await handler(event, data)


class IsAdminMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await is_user_admin(event.from_user.id):
            return await handler(event, data)
