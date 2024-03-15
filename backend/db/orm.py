"""
Модуль для работы с запросами в базу данных
"""
from sqlalchemy import insert, select
from backend.db.models import Base
from backend.db.database import sync_engine, session_factory
from backend.db.models import ReviewsOrm, ChatOrm


class SyncOrm(object):
    ''' Класс содержит методы для работы с бд'''

    # Реализация паттерна Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def drop_tables() -> None:
        """
        Метод удаляет все таблицы в базе данных
        :return: None
        """
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def create_tables() -> None:
        """
        Метод создает все таблицы в базе данных
        :return:
        """
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_message_to_db(user_name: str, user_email: str, message: str) -> None:
        """
        Метод добавляет сообщение пользоваеля из тех.поддержки
        в таблицу базы данных
        :param cookie: текущий куки пользователя
        :param user_name: имя пользователя
        :param user_email: электронная почта пользователя
        :param message: введенное сообщение
        :return: None
        """
        message = ChatOrm(
            user_name=user_name,
            user_email=user_email,
            message=message
        )
        with session_factory() as session:
            session.add_all([message])
            session.commit()

    @staticmethod
    def select_last_messages(user_email: str) -> list:
        """
        Метод делает выборку последних сообщении пользоваеля по его почте
        """
        with session_factory() as session:
            query = select(ChatOrm.message).where(ChatOrm.user_email == user_email)
            result = session.execute(query)
            result = result.all()
            messages = [row[0] for row in result]
            return messages

    @staticmethod
    def insert_user_review_to_db(user_name: str, user_email: str, user_reviews: str, user_star_rating: int) -> None:
        userReview = ReviewsOrm(
            user_name=user_name,
            user_email=user_email,
            user_reviews=user_reviews,
            user_star_rating=user_star_rating
        )
        with session_factory() as session:
            session.add_all([userReview])
            session.commit()
