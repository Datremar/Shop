from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:testpassword@localhost:5432/service_practice_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

_sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session_maker():
    return _sessionmaker
