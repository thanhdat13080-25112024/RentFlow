from fastapi import APIRouter
from app.api.v1.endpoints import rooms, bills, electricity, settings

api_router = APIRouter()

api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(electricity.router, prefix="/electricity", tags=["electricity"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
