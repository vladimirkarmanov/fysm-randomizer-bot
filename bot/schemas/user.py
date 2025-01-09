from datetime import datetime
from functools import cached_property

from pydantic import BaseModel, computed_field


class UserSchema(BaseModel):
    id: int
    username: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_activity_at: datetime | None = None

    class Config:
        from_attributes = True
        validate_default = True
        arbitrary_types_allowed = True

    @computed_field  # type: ignore
    @cached_property
    def username_link(self) -> str:
        return f'@{self.username}' if self.username else ''
