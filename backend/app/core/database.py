"""Database connection and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from .config import settings

# Tạo engine với UTF-8 encoding cho PostgreSQL
engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={
        'client_encoding': 'utf-8',
    }
)

# Đảm bảo tất cả kết nối sử dụng UTF-8
@event.listens_for(engine, 'connect')
def receive_connect(dbapi_conn, connection_record):
    """Set client encoding to UTF-8 for each connection."""
    if hasattr(dbapi_conn, 'set_client_encoding'):
        dbapi_conn.set_client_encoding('UTF-8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()