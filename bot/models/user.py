from sqlalchemy import BigInteger, Column

from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
