from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int

    class Config:
        orm_mode = True
