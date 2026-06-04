from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.api.web import router as web_router
from app.core.config import settings
from app.db import Base, SessionLocal, engine
from app.services.seeder import seed_initial_data

# Khởi tạo schema (idempotent). Trên production nên quản schema bằng Alembic,
# nhưng create_all an toàn vì chỉ tạo bảng còn thiếu.
Base.metadata.create_all(bind=engine)

# Seed dữ liệu mẫu chỉ khi được bật (mặc định True cho dev). Tắt trên production
# bằng SEED_SAMPLE_DATA=false để không chèn 12 phòng giả vào DB thật.
if settings.SEED_SAMPLE_DATA:
    with SessionLocal() as db:
        seed_initial_data(db)

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(web_router)
