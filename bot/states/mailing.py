from aiogram.fsm.state import State, StatesGroup


class MailingCreateState(StatesGroup):
    name = State()
    text = State()
