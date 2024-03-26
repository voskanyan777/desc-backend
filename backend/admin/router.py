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


@admin_router.post('/admin_message')
async def admin_message(user_email: str, message: str,
                        user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    sync_orm.insert_message_to_db(
        user_name='admin',
        role='admin',
        user_email=user_email,
        message=message
    )
    if manager.active_connections.get(user_email):
        await manager.send_personal_message(message, manager.active_connections[user_email])
    return {
        'data': None,
        'status': 'ok'
    }
