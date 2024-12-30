from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.sql import func

from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255), nullable=True, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
