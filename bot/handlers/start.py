from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from commands.base import commands
from core.deps import get_settings
from keyboards.common import get_main_menu_keyboard
from schemas.keyboard import ButtonSchema

router = Router()
settings = get_settings()


@router.message(Command(commands['start'].command))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [ButtonSchema(text='Рандом')]
    await message.answer(
        text='Подберу рандомную тренировку в стиле FYSM\n\n' 'Жми /random',
        parse_mode='HTML',
        reply_markup=get_main_menu_keyboard(buttons),
    )
