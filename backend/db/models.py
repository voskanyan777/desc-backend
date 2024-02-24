from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

written_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
user_name = Annotated[str, mapped_column(String(70), nullable=False)]
user_phone_number = Annotated[str, mapped_column(String(15), nullable=False)]
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class ReviewsOrm(Base):
    __tablename__ = "reviews"
    id: Mapped[intpk]
    user_name: Mapped[user_name]
    user_phone_number: Mapped[user_phone_number]
    user_reviews: Mapped[str]
    user_star_rating: Mapped[int]
    written_at: Mapped[written_at]


class ChatOrm(Base):
    __tablename__ = "chat"
    id: Mapped[intpk]
    user_name: Mapped[user_name]
    user_phone_number: Mapped[user_phone_number]
    message: Mapped[str] = mapped_column(String(300), nullable=False)
    written_at: Mapped[written_at]
