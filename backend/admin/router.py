import sys
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))
from fastapi import APIRouter, Depends

from app.logger_file import logger
from auth.auth_jwt import get_current_active_auth_user
from auth.schemas import UserSchema
from db.orm import SyncOrm

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)
sync_orm = SyncOrm()
BASE_DIR = Path(__file__).parent


@admin_router.get('/user_reviews')
async def get_user_reviews(offset: int = 0,
                           user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    result = sync_orm.get_user_reviews(offset)
    logger.info(f'The administrator has made a request for user reviews. {offset=}')
    return {
        'data': result,
        'status': 'ok'
    }


@admin_router.get('/last_message/')
async def get_last_messages(offset: int = 0,
                            user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    """
    Функция возвращает последние сообщение клинета
    :return: JSON объект. 'data' - Список со всеми сообщениями
    """
    messages: list = sync_orm.select_last_messages(offset)
    logger.info(f'The administrator has made a request to receive the latest messages. {offset=}')
    return {
        'data': messages,
        'status': 'ok'
    }


