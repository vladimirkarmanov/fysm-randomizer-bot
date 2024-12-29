import logging
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import Settings, settings

logger = logging.getLogger(__name__)


def create_engines(settings: Settings) -> tuple[Engine, AsyncEngine]:
    sync_engine: Engine = create_engine(settings.SYNC_DATABASE_URL)
    async_engine: AsyncEngine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
    return sync_engine, async_engine


def create_sessions(
    engine: Engine, async_engine: AsyncEngine
) -> tuple[Callable[[], Session], Callable[[], AsyncSession]]:
    create_async_session: Callable[[], AsyncSession] = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    create_session: Callable[[], Session] = sessionmaker(bind=engine, expire_on_commit=False)
    return create_session, create_async_session


engine, async_engine = create_engines(settings)
create_session, create_async_session = create_sessions(engine, async_engine)
