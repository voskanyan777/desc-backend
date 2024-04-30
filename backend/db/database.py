import sys
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,  # Логирование
)

session_factory = sessionmaker(sync_engine)

