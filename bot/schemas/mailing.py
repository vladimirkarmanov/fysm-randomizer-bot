from datetime import datetime

from pydantic import BaseModel


class MailingCreateSchema(BaseModel):
    name: str
    text: str

    class Config:
        from_attributes = True
        validate_default = True
        arbitrary_types_allowed = True


class MailingGetSchema(BaseModel):
    id: int
    name: str
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        validate_default = True
        arbitrary_types_allowed = True
