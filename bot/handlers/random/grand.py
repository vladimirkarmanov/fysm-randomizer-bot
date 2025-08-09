from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.fysm import RandomCallback
from core.decorators import db_session
from keyboards.random import get_fysm_level_buttons, get_game_type_buttons
from services.randomizer import RandomizerService
from states.random import GrandModuleState
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message
from utils.user import log_user_activity

router = Router()


@router.callback_query(GrandModuleState.first_fysm_level, RandomCallback.filter(F.callback_name == 'fysm_level'))
async def first_fysm_level_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(first_fysm_level=callback_data.fysm_level)
    await state.set_state(GrandModuleState.first_game_type)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 1:</b> выберите вид алгоритма',
            keyboard=get_inline_keyboard(get_game_type_buttons('game_type')),
        )
        await callback.answer()


@router.callback_query(GrandModuleState.first_game_type, RandomCallback.filter(F.callback_name == 'game_type'))
async def first_game_type_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(first_game_type=callback_data.game_type)
    await state.set_state(GrandModuleState.second_fysm_level)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 2:</b> выберите уровень FYSM',
            keyboard=get_inline_keyboard(get_fysm_level_buttons('fysm_level')),
        )
        await callback.answer()


@router.callback_query(GrandModuleState.second_fysm_level, RandomCallback.filter(F.callback_name == 'fysm_level'))
async def second_fysm_level_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(second_fysm_level=callback_data.fysm_level)
    await state.set_state(GrandModuleState.second_game_type)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 2:</b> выберите вид алгоритма',
            keyboard=get_inline_keyboard(get_game_type_buttons('game_type')),
        )
        await callback.answer()


@router.callback_query(GrandModuleState.second_game_type, RandomCallback.filter(F.callback_name == 'game_type'))
async def second_game_type_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(second_game_type=callback_data.game_type)
    await state.set_state(GrandModuleState.third_fysm_level)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 3:</b> выберите уровень FYSM',
            keyboard=get_inline_keyboard(get_fysm_level_buttons('fysm_level')),
        )
        await callback.answer()


@router.callback_query(GrandModuleState.third_fysm_level, RandomCallback.filter(F.callback_name == 'fysm_level'))
async def third_fysm_level_callback(callback: types.CallbackQuery, callback_data: RandomCallback, state: FSMContext):
    await state.update_data(third_fysm_level=callback_data.fysm_level)
    await state.set_state(GrandModuleState.third_game_type)

    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message,
            new_value='<b>Алгоритм 3:</b> выберите вид алгоритма',
            keyboard=get_inline_keyboard(get_game_type_buttons('game_type')),
        )
        await callback.answer()


@router.callback_query(GrandModuleState.third_game_type, RandomCallback.filter(F.callback_name == 'game_type'))
@db_session(commit=True)
async def third_game_type_callback(
    callback: types.CallbackQuery,
    callback_data: RandomCallback,
    state: FSMContext,
    *,
    db_session: AsyncSession,
):
    state_data = await state.get_data()

    text = RandomizerService().get_random_practice(
        zero_module=state_data.get('zero_module'),
        first_fysm_level=state_data.get('first_fysm_level'),
        first_game_type=state_data.get('first_game_type'),
        second_fysm_level=state_data.get('second_fysm_level'),
        second_game_type=state_data.get('second_game_type'),
        third_fysm_level=state_data.get('third_fysm_level'),
        third_game_type=callback_data.game_type,
    )

    if isinstance(callback.message, types.Message):
        await update_text_message(message=callback.message, new_value=text, keyboard=None)

    await log_user_activity(db_session, id=callback.from_user.id, username=callback.from_user.username)
    await callback.answer()
