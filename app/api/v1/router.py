from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1.endpoints import auth, bills, electricity, rooms, settings

api_router = APIRouter()

# Public: chỉ auth (login/logout) là không cần đăng nhập.
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected: mọi dữ liệu khách thuê yêu cầu cookie JWT hợp lệ.
_auth = [Depends(get_current_user)]
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"], dependencies=_auth)
api_router.include_router(bills.router, prefix="/bills", tags=["bills"], dependencies=_auth)
api_router.include_router(electricity.router, prefix="/electricity", tags=["electricity"], dependencies=_auth)
api_router.include_router(settings.router, prefix="/settings", tags=["settings"], dependencies=_auth)
