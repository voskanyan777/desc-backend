from datetime import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class ReviewsOrm(Base):
    __tablename__ = "reviews"
    user_name: Mapped[str] = mapped_column(String(70), nullable=False)
    user_phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    user_reviews: Mapped[str]
    user_star_rating: Mapped[int]
    written_at: Mapped[Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]]
    


class ChatOrm(Base):
    __tablename__ = "chat"
    user_name: Mapped[str] = mapped_column(String(70), nullable=False)
    user_phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    message: Mapped[str] = mapped_column(String(300), nullable=False)
    written_at: Mapped[Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]]