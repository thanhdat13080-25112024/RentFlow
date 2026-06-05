from fastapi import APIRouter

from app.api.v1.endpoints import bills, bootstrap, electricity, rooms, settings

api_router = APIRouter()

# Dự án mở, dữ liệu chỉ là mẫu → mọi endpoint công khai, không cần đăng nhập.
api_router.include_router(bootstrap.router, prefix="/bootstrap", tags=["bootstrap"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(electricity.router, prefix="/electricity", tags=["electricity"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
