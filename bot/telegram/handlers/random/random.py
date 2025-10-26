from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from callbacks.fysm import RandomCallback
from keyboards.random import get_fysm_level_buttons
from states.random import RandomChoiceState
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message

from app.services.randomizer_service import RandomizerService
from app.use_cases.log_user_activity import LogUserActivity, UserInputDTO
from infra.container import DIProtocol

router = Router()


@router.callback_query(
    RandomCallback.filter(F.callback_name == 'setup'),
    RandomCallback.filter(F.initial_choice == 'random'),
)
async def setup_random_callback(
    callback: types.CallbackQuery,
    callback_data: RandomCallback,
    state: FSMContext,
):
    await state.set_state(RandomChoiceState.fysm_level)
    await update_text_message(
        message=callback.message,
        new_value='<b>Выберите уровень FYSM</b>',
        keyboard=get_inline_keyboard(get_fysm_level_buttons('fysm_level')),
    )
    await callback.answer()


@router.callback_query(RandomChoiceState.fysm_level, RandomCallback.filter(F.callback_name == 'fysm_level'))
async def fysm_level_callback(
    callback: types.CallbackQuery,
    callback_data: RandomCallback,
    state: FSMContext,
    di: DIProtocol,
):
    fysm_level = callback_data.fysm_level
    text = RandomizerService().get_full_random_practice(fysm_level=fysm_level)

    if isinstance(callback.message, types.Message):
        await update_text_message(message=callback.message, new_value=text, keyboard=None)

    async with di.resolve('uow_cls')() as uow:
        await LogUserActivity(uow=uow).execute(
            UserInputDTO(telegram_id=callback.from_user.id, username=callback.from_user.username)
        )
    await callback.answer()
