import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat.chat import chat_router
from db.orm import SyncOrm
from auth.auth_jwt import auth_router
from admin.router import admin_router
from logger_file import logger

app = FastAPI()
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(admin_router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
# )


@app.on_event('startup')
async def server_start():
    logger.info('API started')
    sync_orm = SyncOrm()
    sync_orm.drop_tables()
    sync_orm.create_tables()



if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
