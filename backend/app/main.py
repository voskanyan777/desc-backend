"""
Главный файл всей системы, именно здесь
происходит запуск backend части
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.chat.chat import chat_router
from backend.db.orm import SyncOrm

app = FastAPI()
app.include_router(chat_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
)


@app.on_event('startup')
async def server_start():
    syncOrm = SyncOrm()
    syncOrm.drop_tables()
    syncOrm.create_tables()


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
