from aiogram.types import CallbackQuery, Message

from infra.config.settings import get_settings


def is_private_chat(event: Message | CallbackQuery) -> bool:
    match event:
        case Message():
            return event.chat.type == 'private'
        case CallbackQuery():
            return event.message.chat.type == 'private'
        case _:
            return False


def is_user_admin(user_id: int) -> bool:
    return user_id == get_settings().DEVELOPER_ID
