from aiogram import Router, types
from aiogram.filters.command import Command

from constants.commands import admin
from schemas.keyboard import ButtonSchema
from utils.keyboard import get_main_menu_keyboard

router = Router()


@router.message(Command('admin'))
async def admin_panel(message: types.Message):
    buttons = [ButtonSchema(text=admin_command.button_text) for admin_command in admin.values()]
    await message.answer('Переход в панель администратора', reply_markup=get_main_menu_keyboard(buttons))
