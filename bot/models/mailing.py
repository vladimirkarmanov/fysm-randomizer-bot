from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from models.base import Base


class Mailing(Base):
    __tablename__ = 'mailing'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1024), comment='Название рассылки (для админа)')
    text = Column(Text, comment='Текст рассылки')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
