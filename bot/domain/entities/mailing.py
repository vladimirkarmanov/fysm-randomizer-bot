from dataclasses import dataclass
from datetime import datetime


@dataclass
class Mailing:
    id: int
    name: str
    text: str
    created_at: datetime
    updated_at: datetime | None
