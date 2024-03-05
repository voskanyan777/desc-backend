import uvicorn
from fastapi import FastAPI
from backend.chat.chat import chat_router

app = FastAPI()
app.include_router(chat_router)

if __name__ == '__main__':
    uvicorn.run(app)
