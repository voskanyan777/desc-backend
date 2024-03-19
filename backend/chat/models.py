from typing import Annotated
from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    # Модель отзыва
    user_name: str = Field(max_length=70)
    user_email: Annotated[str, Field(max_length=90)]
    user_reviews: str | None = None
    user_star_rating: Annotated[int, Field(ge=0, le=5)] | None = None
