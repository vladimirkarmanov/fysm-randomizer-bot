import random

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.fysm import RandomCallback
from constants.commands import menu, side_menu
from constants.fysm import core_practice_modules
from core.decorators import db_session
from keyboards.random import get_core_module_buttons, get_fysm_level_buttons, get_zero_module_buttons
from schemas.keyboard import ButtonSchema
from services.randomizer import RandomizerService
from states.random import BaseModuleState, DenseModuleState, GrandModuleState, MortalModuleState, RandomState
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message
from utils.user import log_user_activity

router = Router()


@router.message(Command(side_menu['random'].command))
@router.message(F.text == menu['random'].button_text)
async def random_handler(message: types.Message, state: FSMContext):
    await state.clear()

    buttons = [
        ButtonSchema(
            text='Выбирать',
            callback_data=RandomCallback(callback_name='setup', initial_choice='manual'),
        ),
        ButtonSchema(
            text='Испытать удачу ☠️',
            callback_data=RandomCallback(callback_name='setup', initial_choice='random'),
        ),
    ]

    await message.answer(
        text='<b>Что предпочитаете?</b>',
        parse_mode='HTML',
        reply_markup=get_inline_keyboard(buttons),
    )


@router.callback_query(RandomCallback.filter(F.callback_name == 'setup'))
@db_session(commit=True)
async def setup_callback(
    callback: types.CallbackQuery,
    callback_data: RandomCallback,
    state: FSMContext,
    *,
    db_session: AsyncSession,
):
    if callback_data.initial_choice == 'random':
        text = RandomizerService().get_full_random_practice()

        if isinstance(callback.message, types.Message):
            await update_text_message(message=callback.message, new_value=text, keyboard=None)

        await log_user_activity(db_session, id=callback.from_user.id, username=callback.from_user.username)
        await callback.answer()
    else:
        await state.set_state(RandomState.zero_module)

        await update_text_message(
            message=callback.message,
            new_value='<b>Выберите тип включения</b>',
            keyboard=get_inline_keyboard(get_zero_module_buttons('zero_module')),
        )


@router.callback_query(RandomState.zero_module, RandomCallback.filter(F.callback_name == 'zero_module'))
async def zero_module_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(zero_module=callback_data.zero_module)
    await state.set_state(RandomState.core_module)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Выберите режим</b>',
            keyboard=get_inline_keyboard(get_core_module_buttons('core_module')),
        )
        await callback.answer()


@router.callback_query(RandomState.core_module, RandomCallback.filter(F.callback_name == 'core_module'))
async def core_module_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    core_module = callback_data.core_module
    await state.update_data(core_module=callback_data.core_module)

    if core_module == 'random':
        core_module = random.choice(list(core_practice_modules.keys()))

    games_count = core_practice_modules[core_module]['number_of_games']

    match games_count:
        case 1:
            await state.set_state(BaseModuleState.first_fysm_level)
        case 2:
            await state.set_state(DenseModuleState.first_fysm_level)
        case 3:
            await state.set_state(GrandModuleState.first_fysm_level)
        case 4:
            await state.set_state(MortalModuleState.first_fysm_level)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 1:</b> выберите уровень FYSM',
            keyboard=get_inline_keyboard(get_fysm_level_buttons('fysm_level')),
        )
        await callback.answer()
