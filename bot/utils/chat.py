from aiogram.types import Message, CallbackQuery


def is_private_chat(event: Message | CallbackQuery) -> bool:
    if isinstance(event, Message):
        return event.chat.type == 'private'
    elif isinstance(event, CallbackQuery):
        return event.message.chat.type == 'private'