from fastapi import APIRouter

from app.api.v1.endpoints import auth, bills, electricity, rooms, settings

api_router = APIRouter()

# Public routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])
api_router.include_router(electricity.router, prefix="/electricity", tags=["electricity"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
