from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from constants.commands import menu
from schemas.keyboard import ButtonSchema

MAIN_MENU_BUTTONS = [ButtonSchema(text=b.button_text) for b in menu.values()]


def get_inline_keyboard(buttons: list[ButtonSchema], row_size: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in buttons:
        inline_button = InlineKeyboardButton(
            text=b.text,
            callback_data=b.callback_data.pack() if b.callback_data else None,
            url=str(b.url) if b.url else None,
        )
        builder.add(inline_button)

    builder.adjust(row_size)
    return builder.as_markup()


def get_main_menu_keyboard(buttons: list[ButtonSchema] = MAIN_MENU_BUTTONS, row_size: int = 1) -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(text=b.text) for b in buttons]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(row_size)
    return builder.as_markup(resize_keyboard=True)
