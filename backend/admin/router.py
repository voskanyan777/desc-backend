from fastapi import APIRouter, Depends
from backend.db.orm import SyncOrm
from backend.auth.schemas import UserSchema
from backend.auth.auth_jwt import get_current_active_auth_user
from backend.chat.chat import manager

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)
sync_orm = SyncOrm()


@admin_router.get('/user_reviews')
async def get_user_reviews(offset: int = 0,
                           user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    result = sync_orm.get_user_reviews(offset)
    return {
        'data': result,
        'status': 'ok'
    }


@admin_router.get('/last_message/')
async def get_last_messages(user_email: str) -> dict:
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
