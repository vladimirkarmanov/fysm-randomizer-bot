from aiogram.types import CallbackQuery, Message


def is_private_chat(event: Message | CallbackQuery) -> bool:
    match event:
        case Message():
            return event.chat.type == 'private'
        case CallbackQuery():
            return event.message.chat.type == 'private'
        case _:
            return False
