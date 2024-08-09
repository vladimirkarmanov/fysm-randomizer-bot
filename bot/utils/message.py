from contextlib import suppress

from aiogram import types
from aiogram.exceptions import TelegramBadRequest


async def update_text_message(
    message: types.Message,
    new_value: str,
    keyboard: types.InlineKeyboardMarkup | None,
) -> None:
    with suppress(TelegramBadRequest):
        await message.edit_text(new_value, parse_mode='HTML', reply_markup=keyboard)
