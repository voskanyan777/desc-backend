"""
Главный файл всей системы, именно здесь
происходит запуск backend части
"""

import uvicorn
from fastapi import FastAPI
from backend.chat.chat import chat_router
from backend.db.orm import SyncOrm

app = FastAPI()
app.include_router(chat_router)


@app.on_event('startup')
async def server_start():
    syncOrm = SyncOrm()
    syncOrm.drop_tables()
    syncOrm.create_tables()

if __name__ == '__main__':
    uvicorn.run(app)