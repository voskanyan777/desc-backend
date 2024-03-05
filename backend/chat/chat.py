from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from backend.db.orm import SyncOrm

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

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


@chat_router.get('/')
def cget():
    return "asd"


@chat_router.websocket('/ws/{client_cookie}')
async def websocket_endpoint(websocket: WebSocket, client_cookie: str):
    await manager.connect(websocket)
    try:
        while True:
            # Ожидание ввода (сообщения)
            data = await websocket.receive_text()
            syncOrm.insert_message_to_db(
                cookie=client_cookie,
                user_name='Some name',
                user_email='some@mail.ru',
                message=data
            )
            await manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
