import uvicorn
from fastapi import FastAPI
from backend.chat.chat import chat_router
from backend.db.orm import SyncOrm

app = FastAPI()
app.include_router(chat_router)

if __name__ == '__main__':
    syncOrm = SyncOrm()
    syncOrm.drop_tables()
    syncOrm.create_tables()
    uvicorn.run(app)
