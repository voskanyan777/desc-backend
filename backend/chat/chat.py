from fastapi import WebSocket, WebSocketDisconnect, APIRouter

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


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
            await manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
