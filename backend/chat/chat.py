from fastapi import WebSocket, WebSocketDisconnect

from backend.app.logger_file import logger
from backend.chat.router import chat_router
from backend.db.orm import SyncOrm

sync_orm = SyncOrm()


class ConnectionManager(object):
    """
    Класс хранит активные websocket соединения
    """
    # Реализация паттерна Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_email: str):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, websocket: WebSocket, user_email: str):
        del self.active_connections[user_email]

    async def send_personal_message(self, message: str, websocket: WebSocket,
                                    user_email: str = None):
        if user_email is None:
            await websocket.send_text(message)
        else:
            await self.active_connections[user_email].send_text(message)

    async def send_admin_message(self, message: str, user_email: str):
        json = {
            'message': message,
            'user_email': user_email
        }
        await self.active_connections['admin'].send_json(json)


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
    logger.info(f'User {user_email} has joined the chat')
    try:
        while True:
            # Ожидание ввода (сообщения)
            data = await websocket.receive_json()
            message = parse_data(data)
            logger.info(f'The user {user_email} wrote the message: {message}')
            await manager.send_personal_message(message, websocket)
            await manager.send_admin_message(message, user_email)

    except WebSocketDisconnect:
        logger.info(f'User {user_email} has left the chat')
        manager.disconnect(websocket, user_email)


@chat_router.websocket('/ws/admin/{user_email}')
async def admin_websocket(user_email: str, websocket: WebSocket):
    await manager.connect(websocket, 'admin')
    logger.info(f'User {user_email} has joined the chat')
    try:
        while True:
            # {
            #    'message': 'message',
            #    'user_email': 'aaa@mail.ru'
            # }
            data = await websocket.receive_json()
            await manager.send_personal_message(data['message'], websocket, data['user_email'])

    except WebSocketDisconnect:
        logger.info(f'User {user_email} has left the chat')
        manager.disconnect(websocket, user_email)
    except Exception as e:
        logger.exception(f'Error: {e}')
