from aiogram.filters.callback_data import CallbackData


class FYSMLevelCallback(CallbackData, prefix="fysm_level"):
    callback_name: str
    level: str


class CoreModuleCallback(CallbackData, prefix="core_module"):
    callback_name: str
    prev_callback_data: str
    module_name: str
