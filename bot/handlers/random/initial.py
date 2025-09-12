from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from callbacks.fysm import RandomCallback
from constants.commands import menu, side_menu
from schemas.keyboard import ButtonSchema
from utils.keyboard import get_inline_keyboard

router = Router()


@router.message(Command(side_menu['random'].command))
@router.message(F.text == menu['random'].button_text)
async def random_handler(message: types.Message, state: FSMContext):
    await state.clear()

    buttons = [
        ButtonSchema(
            text='выбирать',
            callback_data=RandomCallback(callback_name='setup', initial_choice='manual'),
        ),
        ButtonSchema(
            text='испытать удачу ☠️',
            callback_data=RandomCallback(callback_name='setup', initial_choice='random'),
        ),
    ]

    await message.answer(
        text='<b>Что предпочитаете?</b>',
        parse_mode='HTML',
        reply_markup=get_inline_keyboard(buttons),
    )
