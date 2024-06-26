import sys
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))


from fastapi import APIRouter
from db.orm import SyncOrm
from chat.models import ReviewModel
from app.logger_file import logger


sync_orm = SyncOrm()

# Индивидуальный роутер для чата
chat_router = APIRouter(
    prefix='/chat',
    tags=['chat']
)


@chat_router.post('/add_review')
async def add_review(review: ReviewModel) -> dict:
    """
    Функция принимает отзыв пользователя и записывает его в БД
    """

    sync_orm.insert_user_review_to_db(**review.dict())
    logger.info(f'Added user review. User: {review.user_email}')
    return {
        'data': None,
        'status': 'ok'
    }


@chat_router.get('/user_last_messages')
async def get_user_last_messages(user_email: str, offset: int) -> dict:
    messages = sync_orm.select_user_last_messages(user_email, offset)
    return {
        'data': messages,
        'status': 'ok'
    }
