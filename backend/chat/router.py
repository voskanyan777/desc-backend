"""
Модуль содержит функционал роутера для чата
"""
from fastapi import APIRouter
from backend.db.orm import SyncOrm

syncOrm = SyncOrm()

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


@chat_router.get('/last_message/{client_cookie}')
async def get_last_messages(client_cookie: str) -> dict:
    """
    Функция возвращает последние сообщение клинета
    :param client_cookie: Куки пользователя
    :return: JSON объект. 'data' - Список со всеми сообщениями
    """
    messages: list = syncOrm.select_last_messages(client_cookie)
    return {
        'data': messages,
        'status': 'success',
        'detail': None
    }
