from aiogram.fsm.state import State, StatesGroup


class RandomState(StatesGroup):
    zero_module = State()
    core_module = State()


class BaseModuleState(StatesGroup):
    first_fysm_level = State()
    first_game_type = State()


class DenseModuleState(StatesGroup):
    first_fysm_level = State()
    first_game_type = State()
    second_fysm_level = State()
    second_game_type = State()


class GrandModuleState(StatesGroup):
    first_fysm_level = State()
    first_game_type = State()
    second_fysm_level = State()
    second_game_type = State()
    third_fysm_level = State()
    third_game_type = State()


class MortalModuleState(StatesGroup):
    first_fysm_level = State()
    first_game_type = State()
    second_fysm_level = State()
    second_game_type = State()
    third_fysm_level = State()
    third_game_type = State()
    fourth_fysm_level = State()
    fourth_game_type = State()
