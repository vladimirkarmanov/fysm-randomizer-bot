from aiogram import F, Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.fysm import CoreModuleCallback, FYSMLevelCallback, ZeroModuleCallback
from constants.commands import menu, side_menu
from constants.fysm import core_practice_modules
from core.decorators import db_session
from schemas.keyboard import ButtonSchema
from schemas.user import UserSchema
from services.randomizer import RandomizerService
from services.user import UserService
from utils.keyboard import get_inline_keyboard
from utils.message import update_text_message

router = Router()


@router.message(Command(side_menu['random'].command))
@router.message(F.text == menu['random'].button_text)
async def random_fysm_zero(message: types.Message):
    buttons = [
        ButtonSchema(
            text='Статика', callback_data=ZeroModuleCallback(callback_name='zero_module', module_name='static')
        ),
        ButtonSchema(
            text='Статодинамика', callback_data=ZeroModuleCallback(callback_name='zero_module', module_name='dynamic')
        ),
        ButtonSchema(
            text='Доверяю рандому 🔥',
            callback_data=ZeroModuleCallback(callback_name='zero_module', module_name='random'),
        ),
    ]
    await message.answer(text='Выберите тип включения', parse_mode='HTML', reply_markup=get_inline_keyboard(buttons))


@router.callback_query(ZeroModuleCallback.filter(F.callback_name == 'zero_module'))
async def random_fysm_level(callback: types.CallbackQuery, callback_data: FYSMLevelCallback):
    zero_module = callback_data.module_name

    buttons = [
        ButtonSchema(
            text='FYSM 1',
            callback_data=FYSMLevelCallback(callback_name='fysm_level', zero_module=zero_module, fysm_level='level_1'),
        ),
        ButtonSchema(
            text='FYSM 2',
            callback_data=FYSMLevelCallback(callback_name='fysm_level', zero_module=zero_module, fysm_level='level_2'),
        ),
        ButtonSchema(
            text='FYSM 1 + FYSM 2',
            callback_data=FYSMLevelCallback(
                callback_name='fysm_level', zero_module=zero_module, fysm_level='level_1_and_2'
            ),
        ),
    ]
    await update_text_message(
        message=callback.message, new_value='Выберите уровень FYSM', keyboard=get_inline_keyboard(buttons)
    )


@router.callback_query(FYSMLevelCallback.filter(F.callback_name == 'fysm_level'))
async def random_core_module(callback: types.CallbackQuery, callback_data: FYSMLevelCallback):
    zero_module = callback_data.zero_module
    fysm_level = callback_data.fysm_level

    buttons = []
    for module_name in core_practice_modules.keys():
        buttons.append(
            ButtonSchema(
                text=module_name,
                callback_data=CoreModuleCallback(
                    callback_name='core_module',
                    zero_module=zero_module,
                    fysm_level=fysm_level,
                    core_module=module_name,
                ),
            )
        )
    buttons.append(
        ButtonSchema(
            text='Доверяю рандому 🔥',
            callback_data=CoreModuleCallback(
                callback_name='core_module', zero_module=zero_module, fysm_level=fysm_level, core_module='random'
            ),
        )
    )
    await update_text_message(
        message=callback.message, new_value='Выберите режим', keyboard=get_inline_keyboard(buttons)
    )


@router.callback_query(CoreModuleCallback.filter(F.callback_name == 'core_module'))
@db_session(commit=True)
async def random_fysm_response(
    callback: types.CallbackQuery,
    callback_data: CoreModuleCallback,
    *,
    db_session: AsyncSession,
):
    zero_module = callback_data.zero_module
    fysm_level = callback_data.fysm_level
    core_module = callback_data.core_module

    text = RandomizerService().get_random_practice(zero_module, fysm_level, core_module)
    await update_text_message(message=callback.message, new_value=text, keyboard=None)
    await callback.answer()

    await UserService(db_session).get_or_create(
        UserSchema(id=callback.from_user.id, username=callback.from_user.username)
    )
