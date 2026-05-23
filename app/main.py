from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal, get_db
from app.api.v1.api import api_router
from app.services.database_seeder import init_data
from app.core.security import get_current_user

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
async def read_root(request: Request, month: int = None, year: int = None):
    # Kiểm tra auth qua cookie
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        from app.core.security import jwt
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return RedirectResponse(url="/login")

    now = datetime.now()
    if month is None: month = now.month
    if year is None: year = now.year
    return templates.TemplateResponse(
        request=request, name="index.html", context={"month": month, "year": year}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")
