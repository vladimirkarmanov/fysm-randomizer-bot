from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import registry
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Table

from domain.entities.mailing import Mailing
from domain.entities.user import User

mapper_registry = registry()

user_table = Table(
    'user',
    mapper_registry.metadata,
    Column('id', BigInteger, primary_key=True, index=True),
    Column('telegram_id', BigInteger, unique=True),
    Column('username', String(255), nullable=True, unique=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    Column('last_activity_at', DateTime(timezone=True)),
)


mailing_table = Table(
    'mailing',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String(1024), comment='Название рассылки (для админа)'),
    Column('text', Text, comment='Текст рассылки'),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
)


def start_sqlalchemy_mappers():
    mapper_registry.map_imperatively(User, user_table)
    mapper_registry.map_imperatively(Mailing, mailing_table)
