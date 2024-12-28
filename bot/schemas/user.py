from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
