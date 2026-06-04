from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.api.web import router as web_router
from app.core.config import settings
from app.db import Base, SessionLocal, engine
from app.services.seeder import seed_initial_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo schema và seed dữ liệu.
    # Trên serverless (Vercel), code này chạy khi function "cold start".
    # Ta tránh chạy nếu đang dùng SQLite ở môi trường production vì filesystem là read-only.
    is_sqlite = settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    if not (is_sqlite and settings.ENVIRONMENT == "production"):
        try:
            Base.metadata.create_all(bind=engine)
            if settings.SEED_SAMPLE_DATA:
                with SessionLocal() as db:
                    seed_initial_data(db)
        except Exception as e:
            # Log lỗi nhưng không làm sập cả app để Vercel không báo Function Invocation Failed ngay lập tức
            print(f"Database initialization error: {e}")
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

static_dir = settings.BASE_DIR / "app" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)
