from pathlib import Path

from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends

from backend.app.logger_file import logger
from backend.auth.auth_jwt import get_current_active_auth_user
from backend.auth.schemas import UserSchema
from backend.chat.chat import manager
from backend.db.orm import SyncOrm

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


@admin_router.post('/admin_message')
async def admin_message(user_email: str, message: str,
                        user: UserSchema = Depends(get_current_active_auth_user)) -> dict:
    sync_orm.insert_message_to_db(
        user_name='admin',
        role='admin',
        user_email=user_email,
        message=message
    )
    if manager.active_connections.get(user_email):
        await manager.send_personal_message(message, manager.active_connections[user_email])
    logger.info(f'The admin replied to the user {user_email} with the message: {message}')
    return {
        'data': None,
        'status': 'ok'
    }


@admin_router.get('/change_information')
async def change_html_information(tag: str, class_: str, new_value: str,
                                  user: UserSchema = Depends(get_current_active_auth_user)):
    with open(BASE_DIR / "index.html", "r") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    main_paragraph = soup.find(tag, class_=class_)

    main_paragraph.string = new_value

    with open(BASE_DIR / "index.html", "w") as file:
        file.write(str(soup))
    logger.info(
        f'The admin changed the information on the html page. {tag=}, {class_=}, {new_value=}')
    return {
        'data': None,
        'status': 'ok'
    }
