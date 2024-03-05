from sqlalchemy import insert
from backend.db.models import Base
from backend.db.database import sync_engine, session_factory
from models import ReviewsOrm, ChatOrm


class SyncOrm(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def create_tables() -> None:
        """
        Метод создает все таблицы в базе данных
        :return:
        """
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_message_to_db(cookie: str, user_name: str, user_email: str, message: str) -> None:
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
            cookie=cookie,
            user_name=user_name,
            user_email=user_email,
            message=message
        )
        with session_factory() as session:
            session.add_all([message])
            session.commit()

    # @staticmethod
    # def insert_data():
    #     reviews = ReviewsOrm(
    #         user_name='Voskan',
    #         user_email='79999999999',
    #         user_reviews='good',
    #         user_star_rating=3
    #     )
    #     chat = ChatOrm(
    #         user_name='Voskan',
    #         user_email='79999999999',
    #         message='Как купить у вас услугу'
    #     )
    #     with session_factory() as session:
    #         session.add_all([reviews, chat])
    #         session.commit()
