from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

_url = settings.SQLALCHEMY_DATABASE_URL
# check_same_thread chỉ áp dụng cho SQLite; Postgres sẽ báo lỗi nếu truyền vào.
_connect_args = {"check_same_thread": False} if _url.startswith("sqlite") else {}

# pool_pre_ping: trên serverless, kết nối Postgres có thể bị đóng giữa các lần
# gọi hàm (cold start) — ping trước khi dùng để tránh lỗi "connection closed".
engine = create_engine(_url, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
