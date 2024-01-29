from aiogram import F
from aiogram import types, Router
from aiogram.filters import Command

from callbacks.fysm import FYSMLevelCallback, CoreModuleCallback
from commands.base import commands
from constants.fysm import (
    core_practice_modules,
)
from core.deps import get_settings
from keyboards.common import get_inline_keyboard
from schemas.keyboard import ButtonSchema
from utils.message import update_text_message
from services.randomizer import randomizer_service


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

    text = randomizer_service.get_random_practice(core_module_name, fysm_level)
    await update_text_message(message=callback.message,
                              new_value=text,
                              keyboard=None)

    await callback.answer()
