"""
Модуль содержит функционал роутера для чата
"""
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from backend.db.orm import SyncOrm
from backend.chat.models import ReviewModel
from backend.auth.schemas import UserSchema
from backend.auth.auth_jwt import get_current_active_auth_user

sync_orm = SyncOrm()

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


@chat_router.get('/last_message/')
async def get_last_messages(user_email: str, user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    """
    Функция возвращает последние сообщение клинета
    :param user_email: почта пользователя
    :return: JSON объект. 'data' - Список со всеми сообщениями
    """
    messages: list = sync_orm.select_last_messages(user_email)
    return {
        'data': messages,
        'status': 'ok'
    }


@chat_router.post('/add_review')
async def add_review(review: ReviewModel, user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    """
    Функция принимает отзыв пользователя и записывает его в БД
    """

    sync_orm.insert_user_review_to_db(**review.dict())
    return {
        'data': None,
        'status': 'ok'
    }


@chat_router.get('/user_reviews')
async def get_user_reviews(offset: int = 0,
                           user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    result = sync_orm.get_user_reviews(offset)
    return {
        'data': result,
        'status': 'ok'
    }



