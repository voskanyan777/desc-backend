from fastapi import WebSocket, WebSocketDisconnect
from backend.db.orm import SyncOrm
from backend.chat.routers import chat_router

syncOrm = SyncOrm()


class ConnectionManager:
    """
    Класс храни активные websocket соединения
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@chat_router.websocket('/ws/{client_cookie}')
async def websocket_endpoint(websocket: WebSocket, client_cookie: str):
    await manager.connect(websocket)
    try:
        while True:
            # Ожидание ввода (сообщения)
            data = await websocket.receive_json()
            user_name = data['user_name']
            user_email = data['user_email']
            message = data['message']
            syncOrm.insert_message_to_db(
                cookie=client_cookie,
                user_name=user_name,
                user_email=user_email,
                message=message
            )
            await manager.send_personal_message(message, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
