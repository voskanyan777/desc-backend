from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    # Модель отзыва
    user_name: str = Field(max_length=70)
    user_email: str = Field(max_length=90)
    user_reviews: str
    user_star_rating: int = Field(ge=0, le=5)
