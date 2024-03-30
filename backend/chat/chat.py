"""
Модуль с реализацией чата техподдержки
"""

from fastapi import WebSocket, WebSocketDisconnect
from backend.db.orm import SyncOrm
from backend.chat.router import chat_router
from backend.app.logger_file import logger

sync_orm = SyncOrm()


class ConnectionManager:
    """
    Класс хранит активные websocket соединения
    """

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, websocket: WebSocket, user_email: str):
        del self.active_connections[user_email]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


def parse_data(data: dict) -> str:
    """
    Функция парсит данные, полученние через websocket
    :param data: полученный словарь с данными
    :return: сообщение, введенное пользователем
    """
    user_name = data['user_name']
    user_email = data['user_email']
    message = data['message']
    sync_orm.insert_message_to_db(
        user_name=user_name,
        role='user',
        user_email=user_email,
        message=message
    )
    return message


@chat_router.websocket('/ws/{user_email}')
async def websocket_endpoint(user_email: str, websocket: WebSocket) -> None:
    """
    Функция обрабатывает поступившые сообщения через websocket
    """
    await manager.connect(websocket, user_email)
    try:
        while True:
            # Ожидание ввода (сообщения)
            data = await websocket.receive_json()
            message = parse_data(data)
            logger.info(f'The user {user_email} wrote the message: {message}')
            await manager.send_personal_message(message, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_email)


# @chat_router.post('/test')
# async def test_func(user_email: str, message: str):
#     if manager.active_connections.get(user_email):
#         await manager.send_personal_message(message, manager.active_connections[user_email])
#     return {
#         'data': None,
#         'status': 'ok'
#     }

