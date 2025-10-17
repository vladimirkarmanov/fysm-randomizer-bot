from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property


@dataclass
class User:
    id: int = field(init=False)
    telegram_id: int
    username: str | None
    created_at: datetime = field(init=False)
    updated_at: datetime | None = field(init=False)
    last_activity_at: datetime

    @cached_property
    def telegram_link(self) -> str:
        return f'@{self.username}' if self.username else ''

    def sync_user_data(self, username: str | None) -> None:
        self.username = username
        self.last_activity_at = datetime.now()
