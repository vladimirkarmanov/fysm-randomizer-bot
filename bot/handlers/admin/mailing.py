from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from constants.commands import admin
from core.decorators import db_session
from schemas.mailing import MailingCreateSchema
from services.mailing import MailingService
from states.mailing import MailingCreateState

router = Router()


@router.message(Command(admin['mailing'].command))
@router.message(F.text == admin['mailing'].button_text)
async def create_mailing_handler(message: types.Message, state: FSMContext):
    await state.set_state(MailingCreateState.name)
    await message.answer('<b>Введите название рассылки</b>', parse_mode='HTML')


@router.message(MailingCreateState.name)
async def mailing_name_handler(message: types.Message, state: FSMContext):
    mailing_name = message.text
    if not mailing_name:
        await message.answer('<b>Отправляйте только текст!</b>', parse_mode='HTML')
        return

    await state.set_state(MailingCreateState.text)
    await state.update_data(name=message.text)
    await message.answer('<b>Введите текст рассылки</b>', parse_mode='HTML')


@router.message(MailingCreateState.text)
@db_session(commit=True)
async def mailing_text_handler(message: types.Message, state: FSMContext, *, db_session: AsyncSession):
    state_data = await state.get_data()
    name = state_data['name']
    text = message.text
    mailing_service = MailingService(db_session)

    if not text:
        await message.answer('<b>Отправляйте только текст!</b>', parse_mode='HTML')
        return

    mailing = await mailing_service.create(MailingCreateSchema(name=name, text=text))

    if mailing:
        await message.answer('<b>Рассылка успешно создана!</b>', parse_mode='HTML')
    else:
        await message.answer('<b>Произошла ошибка!</b>', parse_mode='HTML')

    await state.clear()
