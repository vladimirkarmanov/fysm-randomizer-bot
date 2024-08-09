from aiogram.filters.callback_data import CallbackData


class ZeroModuleCallback(CallbackData, prefix='zero_module'):
    callback_name: str
    module_name: str


class FYSMLevelCallback(CallbackData, prefix='fysm_level'):
    callback_name: str
    zero_module: str
    fysm_level: str


class CoreModuleCallback(CallbackData, prefix='core_module'):
    callback_name: str
    zero_module: str
    fysm_level: str
    core_module: str
