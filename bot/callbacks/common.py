from typing import Literal

from aiogram.filters.callback_data import CallbackData


class PaginationCallback(CallbackData, prefix="pagination"):
    callback_name: Literal['prev', 'next']
