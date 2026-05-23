from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.api.web import router as web_router
from app.core.config import settings
from app.db import Base, SessionLocal, engine
from app.services.seeder import seed_initial_data

# Khởi tạo schema + seed dữ liệu mẫu (chạy 1 lần khi DB rỗng)
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_initial_data(db)

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)
