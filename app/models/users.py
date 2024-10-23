from sqlalchemy import String, ForeignKey, JSON, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.datebase import Base


class UserTelegram(Base):
    __tablename__ = 'user_telegram'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    username: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100), default=None, nullable=True)
    last_name: Mapped[str| None] = mapped_column(String(100), default=None, nullable=True)
    admin: Mapped[bool] = mapped_column(default=False)
