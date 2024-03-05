from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

written_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
user_name = Annotated[str, mapped_column(String(70), nullable=False)]
user_email = Annotated[str, mapped_column(String(90), nullable=False)]
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class ReviewsOrm(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint('user_star_rating >= 0 AND user_star_rating <= 5'),
    )
    id: Mapped[intpk]
    user_name: Mapped[user_name]
    user_email: Mapped[user_email]
    user_reviews: Mapped[str]
    user_star_rating: Mapped[int]
    written_at: Mapped[written_at]


class ChatOrm(Base):
    __tablename__ = "chat"
    id: Mapped[intpk]
    cookie: Mapped[str] = mapped_column(String(100), nullable=False)
    user_name: Mapped[user_name]
    user_email: Mapped[user_email]
    message: Mapped[str] = mapped_column(String(300), nullable=False)
    written_at: Mapped[written_at]


class UserOrm(Base):
    """
    Таблица для хранения данных админа
    """
    __tablename__ = "users"
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(String(), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=False)
    
