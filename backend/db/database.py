from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.db.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,  # Логирование
)

session_factory = sessionmaker(sync_engine)

