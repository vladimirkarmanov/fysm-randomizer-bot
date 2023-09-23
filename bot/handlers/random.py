from random import choice, sample

from aiogram import F
from aiogram import types, Router
from aiogram.filters import Command

from callbacks.fysm import FYSMLevelCallback, CoreModuleCallback
from commands.base import commands
from constants.fysm import (
    zero_modules,
    zero_modes,
    core_practice_modules,
    games,
    core_practice_modes,
    zero_games,
)
from core.deps import get_settings
from keyboards.common import get_inline_keyboard
from schemas.keyboard import ButtonSchema
from utils.message import update_text_message

router = Router()
settings = get_settings()


@router.message(Command(commands['random'].command))
@router.message(F.text == 'Рандом')
async def random_fysm_level(message: types.Message):
    buttons = [ButtonSchema(text='FYSM 1',
                            callback_data=FYSMLevelCallback(callback_name='fysm_level', level='level_1')),
               ButtonSchema(text='FYSM 1 + Эпизоды',
                            callback_data=FYSMLevelCallback(callback_name='fysm_level', level='level_1_episodes')),
               ButtonSchema(text='FYSM 2',
                            callback_data=FYSMLevelCallback(callback_name='fysm_level', level='level_2'))]
    await message.answer(text='Ваш уровень FYSM?',
                         parse_mode='HTML',
                         reply_markup=get_inline_keyboard(buttons))


@router.callback_query(FYSMLevelCallback.filter(F.callback_name == 'fysm_level'))
async def random_core_module(callback: types.CallbackQuery, callback_data: FYSMLevelCallback):
    fysm_level = callback_data.level

    buttons = []
    for module_name in core_practice_modules.keys():
        buttons.append(ButtonSchema(text=module_name,
                                    callback_data=CoreModuleCallback(callback_name='core_module',
                                                                     prev_callback_data=fysm_level,
                                                                     module_name=module_name)))
    buttons.append(ButtonSchema(text='доверяю рандому 🔥',
                                callback_data=CoreModuleCallback(callback_name='core_module',
                                                                 prev_callback_data=fysm_level,
                                                                 module_name='random')))
    await update_text_message(message=callback.message,
                              new_value='Выберите режим',
                              keyboard=get_inline_keyboard(buttons))


@router.callback_query(CoreModuleCallback.filter(F.callback_name == 'core_module'))
async def random_fysm_level(callback: types.CallbackQuery, callback_data: CoreModuleCallback):
    core_module_name = callback_data.module_name
    fysm_level = callback_data.prev_callback_data

    zero_module = choice(zero_modules)
    zero_mode = choice(zero_modes[zero_module['name']])
    zero_game = choice(zero_games[zero_module['name']])
    if core_module_name == 'random':
        core_module_name = choice(list(core_practice_modules.keys()))

    core_practice_module = core_practice_modules[core_module_name]
    number_of_games = core_practice_module['number_of_games']

    games_for_practice = sample(games[fysm_level], number_of_games)
    modes_for_practice = [choice(core_practice_modes) for _ in range(number_of_games)]

    core_practice = ''
    for game, mode in zip(games_for_practice, modes_for_practice):
        core_practice += f'{game} - {mode}\n'

    text = (f'<b>Включение:</b>\n{zero_game} - {zero_mode}\n\n'
            f'<b>Основная часть:</b>\n{core_practice}')
    await update_text_message(message=callback.message,
                              new_value=text,
                              keyboard=None)

    await callback.answer()
