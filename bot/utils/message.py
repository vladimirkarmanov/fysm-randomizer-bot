from contextlib import suppress

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto


async def update_text_message(
        message: types.Message,
        new_value: str,
        keyboard: types.InlineKeyboardMarkup | None,
) -> None:
    with suppress(TelegramBadRequest):
        await message.edit_text(new_value, parse_mode='HTML', reply_markup=keyboard)


async def update_media_message(
        message: types.Message,
        new_media: InputMediaPhoto,
        keyboard: types.InlineKeyboardMarkup | None,
) -> None:
    with suppress(TelegramBadRequest):
        await message.edit_media(media=new_media, reply_markup=keyboard)
