from pydantic import BaseModel


class UserDataSchema(BaseModel):
    history: str
