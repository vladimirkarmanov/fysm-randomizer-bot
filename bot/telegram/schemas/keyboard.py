from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel, HttpUrl


class ButtonSchema(BaseModel):
    text: str
    callback_data: CallbackData | None = None
    url: HttpUrl | None = None
