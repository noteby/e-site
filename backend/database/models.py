from sqlalchemy import Column
from sqlalchemy import Boolean, DateTime, Integer, String

from .engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=36), unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
