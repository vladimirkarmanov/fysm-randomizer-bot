from settings import settings


async def is_user_admin(user_id: int) -> bool:
    return user_id == settings.DEVELOPER_ID
