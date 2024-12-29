from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from constants.commands import side_menu
from schemas.keyboard import ButtonSchema
from utils.keyboard import get_main_menu_keyboard

router = Router()


@router.message(Command(side_menu['start'].command))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [ButtonSchema(text='Рандом')]
    await message.answer(
        text='Подберу рандомную тренировку в стиле FYSM\n\n' 'Жми /random',
        parse_mode='HTML',
        reply_markup=get_main_menu_keyboard(buttons),
    )
