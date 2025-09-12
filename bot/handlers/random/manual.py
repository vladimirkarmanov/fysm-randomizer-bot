import random

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from callbacks.fysm import RandomCallback
from constants.fysm import core_practice_modules
from keyboards.random import get_core_module_buttons, get_fysm_level_buttons, get_zero_module_buttons
from states.random import BaseModuleState, DenseModuleState, GrandModuleState, ManualChoiceState, MortalModuleState
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message

router = Router()


@router.callback_query(
    RandomCallback.filter(F.callback_name == 'setup'),
    RandomCallback.filter(F.initial_choice == 'manual'),
)
async def setup_manual_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.set_state(ManualChoiceState.zero_module)
    await update_text_message(
        message=callback.message,
        new_value='<b>Выберите тип включения</b>',
        keyboard=get_inline_keyboard(get_zero_module_buttons('zero_module')),
    )
    await callback.answer()


@router.callback_query(ManualChoiceState.zero_module, RandomCallback.filter(F.callback_name == 'zero_module'))
async def zero_module_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(zero_module=callback_data.zero_module)
    await state.set_state(ManualChoiceState.core_module)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Выберите режим</b>',
            keyboard=get_inline_keyboard(get_core_module_buttons('core_module')),
        )
        await callback.answer()


@router.callback_query(ManualChoiceState.core_module, RandomCallback.filter(F.callback_name == 'core_module'))
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
