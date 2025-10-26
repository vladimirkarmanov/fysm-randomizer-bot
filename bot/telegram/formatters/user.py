from domain.entities.user import User
from infra.config.settings import get_settings

settings = get_settings()


def format_user_entity(entity: User) -> str:
    return (
        f'username: {entity.telegram_link}\n'
        f'created_at: {entity.created_at.astimezone(settings.timezone).strftime("%Y-%m-%d %H:%M:%S")}\n'
        f'last_activity_at: {entity.last_activity_at.astimezone(settings.timezone).strftime("%Y-%m-%d %H:%M:%S")}\n'
    )
