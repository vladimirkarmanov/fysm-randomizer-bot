from aiogram.filters.callback_data import CallbackData


class RandomCallback(CallbackData, prefix='random'):  # type: ignore
    callback_name: str
    initial_choice: str | None = None
    zero_module: str | None = None
    core_module: str | None = None
    fysm_level: str | None = None
    game_type: str | None = None
