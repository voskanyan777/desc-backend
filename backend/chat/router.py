"""
Модуль содержит функционал роутера для чата
"""
from fastapi import APIRouter
from pydantic import EmailStr
from backend.db.orm import SyncOrm
from backend.chat.models import ReviewModel

syncOrm = SyncOrm()

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


@chat_router.get('/last_message/')
async def get_last_messages(user_email: str) -> dict:
    """
    Функция возвращает последние сообщение клинета
    :param user_email: почта пользователя
    :return: JSON объект. 'data' - Список со всеми сообщениями
    """
    messages: list = syncOrm.select_last_messages(user_email)
    return {
        'data': messages,
        'status': 'success',
        'detail': None
    }


@chat_router.post('/add_review')
async def add_review(review: ReviewModel):
    syncOrm.insert_user_review_to_db(review.user_name, review.user_email, review.user_reviews, review.user_star_rating)
    return {
        'data': None,
        'status': 'success',
        'detail': None
    }
