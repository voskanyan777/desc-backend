"""
Главный файл всей системы, именно здесь
происходит запуск backend части
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.chat.chat import chat_router
from backend.db.orm import SyncOrm
from backend.auth.auth_jwt import router as auth_router

app = FastAPI()
app.include_router(chat_router)
app.include_router(auth_router)


@app.on_event('startup')
async def server_start():
    syncOrm = SyncOrm()
    # syncOrm.drop_tables()
    syncOrm.create_tables()


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
