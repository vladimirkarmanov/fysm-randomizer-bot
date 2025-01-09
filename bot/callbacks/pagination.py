from aiogram.filters.callback_data import CallbackData


class PaginationCallback(CallbackData, prefix='pagination'):  # type: ignore
    callback_name: str
    offset: int
