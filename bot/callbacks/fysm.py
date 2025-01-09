from aiogram.filters.callback_data import CallbackData


class ZeroModuleCallback(CallbackData, prefix='zero_module'):  # type: ignore
    callback_name: str
    zero_module: str


class FYSMLevelCallback(CallbackData, prefix='fysm_level'):  # type: ignore
    callback_name: str
    zero_module: str
    fysm_level: str


class GameTypeCallback(CallbackData, prefix='game_type'):  # type: ignore
    callback_name: str
    zero_module: str
    fysm_level: str
    game_type: str


class CoreModuleCallback(CallbackData, prefix='core_module'):  # type: ignore
    callback_name: str
    zero_module: str
    fysm_level: str
    game_type: str
    core_module: str
