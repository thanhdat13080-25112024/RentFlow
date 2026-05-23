from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal, get_db
from app.api.v1.api import api_router
from app.services.init_db import init_data

# Khởi tạo database
Base.metadata.create_all(bind=engine)
# Seed data
with SessionLocal() as db:
    init_data(db)

app = FastAPI(title=settings.PROJECT_NAME)

# Templates & Static
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API Router
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None, db: Session = Depends(get_db)):
    now = datetime.now()
    if month is None: month = now.month
    if year is None: year = now.year
    return templates.TemplateResponse(
        request=request, name="index.html", context={"month": month, "year": year}
    )
