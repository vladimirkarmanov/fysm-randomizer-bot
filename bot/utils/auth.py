from aiogram.exceptions import TelegramBadRequest

from app import bot
from core.deps import get_settings

settings = get_settings()


async def is_user_chat_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(settings.GROUP_ID, user_id)
        admins = await bot.get_chat_administrators(settings.GROUP_ID)
        admins_ids = [admin.user.id for admin in admins]
        if user_id in admins_ids or member.status == 'member':
            return True
    except TelegramBadRequest:
        return False

    return False


async def is_user_admin(user_id: int) -> bool:
    try:
        admins = await bot.get_chat_administrators(settings.GROUP_ID)
        return user_id in [admin.user.id for admin in admins]
    except TelegramBadRequest:
        return False
