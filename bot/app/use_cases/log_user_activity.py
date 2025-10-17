from dataclasses import dataclass
from datetime import datetime

from app.interfaces.uow import IUnitOfWork
from app.interfaces.use_case import UseCase
from domain.entities.user import User


@dataclass(frozen=True)
class UserInputDTO:
    telegram_id: int
    username: str | None


@dataclass(frozen=True)
class UserOutputDTO:
    id: int
    telegram_id: int
    username: str | None
    last_activity_at: datetime | None


class LogUserActivity(UseCase):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, data: UserInputDTO) -> UserOutputDTO:
        user = await self.uow.users.find_by_telegram_id(data.telegram_id)
        if not user:
            user = User(
                telegram_id=data.telegram_id,
                username=data.username,
                last_activity_at=datetime.now(),
            )
            await self.uow.users.save(user)
        else:
            user.sync_user_data(data.username)
            await self.uow.users.update(user)

        await self.uow.commit()
        return UserOutputDTO(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            last_activity_at=user.last_activity_at,
        )
