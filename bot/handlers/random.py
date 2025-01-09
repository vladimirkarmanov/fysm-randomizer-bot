from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.fysm import CoreModuleCallback, FYSMLevelCallback, GameTypeCallback, ZeroModuleCallback
from constants.commands import menu, side_menu
from constants.fysm import core_practice_modules
from core.decorators import db_session
from schemas.keyboard import ButtonSchema
from schemas.user import UserCreateSchema, UserUpdateSchema
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
            text='Статика', callback_data=ZeroModuleCallback(callback_name='zero_module', zero_module='static')
        ),
        ButtonSchema(
            text='Статодинамика', callback_data=ZeroModuleCallback(callback_name='zero_module', zero_module='dynamic')
        ),
        ButtonSchema(
            text='Доверяю рандому 🔥',
            callback_data=ZeroModuleCallback(callback_name='zero_module', zero_module='random'),
        ),
    ]
    await message.answer(text='Выберите тип включения', parse_mode='HTML', reply_markup=get_inline_keyboard(buttons))


@router.callback_query(ZeroModuleCallback.filter(F.callback_name == 'zero_module'))
async def random_fysm_level(callback: types.CallbackQuery, callback_data: ZeroModuleCallback):
    zero_module = callback_data.zero_module

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
    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message, new_value='Выберите уровень FYSM', keyboard=get_inline_keyboard(buttons)
        )


@router.callback_query(FYSMLevelCallback.filter(F.callback_name == 'fysm_level'))
async def game_type(callback: types.CallbackQuery, callback_data: FYSMLevelCallback):
    zero_module = callback_data.zero_module
    fysm_level = callback_data.fysm_level

    buttons = [
        ButtonSchema(
            text='Центр',
            callback_data=GameTypeCallback(
                callback_name='game_type', zero_module=zero_module, fysm_level=fysm_level, game_type='center'
            ),
        ),
        ButtonSchema(
            text='Верх',
            callback_data=GameTypeCallback(
                callback_name='game_type', zero_module=zero_module, fysm_level=fysm_level, game_type='top'
            ),
        ),
        ButtonSchema(
            text='Низ',
            callback_data=GameTypeCallback(
                callback_name='game_type', zero_module=zero_module, fysm_level=fysm_level, game_type='bottom'
            ),
        ),
        ButtonSchema(
            text='Все',
            callback_data=GameTypeCallback(
                callback_name='game_type', zero_module=zero_module, fysm_level=fysm_level, game_type='all'
            ),
        ),
    ]
    if isinstance(callback.message, types.Message):
        await update_text_message(
            message=callback.message, new_value='Выберите вид алгоритмов', keyboard=get_inline_keyboard(buttons)
        )


@router.callback_query(GameTypeCallback.filter(F.callback_name == 'game_type'))
async def random_core_module(callback: types.CallbackQuery, callback_data: GameTypeCallback):
    zero_module = callback_data.zero_module
    fysm_level = callback_data.fysm_level
    game_type = callback_data.game_type

    buttons = []
    for module_name in core_practice_modules.keys():
        buttons.append(
            ButtonSchema(
                text=module_name,
                callback_data=CoreModuleCallback(
                    callback_name='core_module',
                    zero_module=zero_module,
                    fysm_level=fysm_level,
                    game_type=game_type,
                    core_module=module_name,
                ),
            )
        )
    buttons.append(
        ButtonSchema(
            text='Доверяю рандому 🔥',
            callback_data=CoreModuleCallback(
                callback_name='core_module',
                zero_module=zero_module,
                fysm_level=fysm_level,
                game_type=game_type,
                core_module='random',
            ),
        )
    )
    if isinstance(callback.message, types.Message):
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
    game_type = callback_data.game_type
    core_module = callback_data.core_module

    text = RandomizerService().get_random_practice(
        zero_module=zero_module,
        fysm_level=fysm_level,
        game_type=game_type,
        core_module=core_module,
    )

    if isinstance(callback.message, types.Message):
        await update_text_message(message=callback.message, new_value=text, keyboard=None)

    await callback.answer()
    await UserService(db_session).get_or_create(
        UserCreateSchema(id=callback.from_user.id, username=callback.from_user.username)
    )
    await UserService(db_session).update(
        id=callback.from_user.id,
        user_schema=UserUpdateSchema(username=callback.from_user.username, last_activity_at=datetime.now()),
    )
