from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from constants.commands import menu, side_menu
from schemas.keyboard import ButtonSchema
from settings import settings
from utils.keyboard import get_main_menu_keyboard

router = Router()


@router.message(Command(side_menu['start'].command))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [ButtonSchema(text=b.button_text) for b in menu.values()]
    text = (
        f'Подберу рандомную тренировку в стиле FYSM /random\n\n'
        f'Оставить обратную связь или предложения @{settings.DEVELOPER_USERNAME}'
    )
    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=get_main_menu_keyboard(buttons),
    )
