"""
Модуль содержит реализацию моделей таблиц в базе данных
"""
from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

written_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
user_name = Annotated[str, mapped_column(String(70), nullable=False)]
user_email = Annotated[str, mapped_column(String(90), nullable=False)]
intpk = Annotated[int, mapped_column(primary_key=True)]
message = Annotated[str, mapped_column(String(300), nullable=False)]

# Базовый класс
class Base(DeclarativeBase):
    pass


class ReviewsOrm(Base):
    """
    Модель таблицы, которая содержить отзывы пользователей
    """
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint('user_star_rating >= 0 AND user_star_rating <= 5'),
    )
    id: Mapped[intpk]
    user_name: Mapped[user_name]
    user_email: Mapped[user_email]
    user_reviews: Mapped[str] = mapped_column(nullable=True)
    user_star_rating: Mapped[int]
    written_at: Mapped[written_at]


class ChatOrm(Base):
    """
    Модель таблицы, которая содержить все сообщения пользователей
    """
    __tablename__ = "chat"
    __table_args__ = (
        CheckConstraint("role in ('user', 'admin')"),
    )
    id: Mapped[intpk]
    user_name: Mapped[user_name]
    role: Mapped[str] = mapped_column(nullable=False)
    user_email: Mapped[user_email]
    message: Mapped[message]
    written_at: Mapped[written_at]


class UserOrm(Base):
    """
    Таблица для хранения данных админа
    """
    __tablename__ = "users"
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
