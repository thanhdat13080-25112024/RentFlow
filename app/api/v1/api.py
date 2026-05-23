from fastapi import APIRouter, Depends
from app.api.v1.endpoints import rooms, bills, electricity, settings, auth
from app.core.security import get_current_user

api_router = APIRouter()

# Public routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routes
api_router.include_router(
    rooms.router, 
    prefix="/rooms", 
    tags=["rooms"], 
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    bills.router, 
    prefix="/bills", 
    tags=["bills"], 
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    electricity.router, 
    prefix="/electricity", 
    tags=["electricity"], 
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    settings.router, 
    prefix="/settings", 
    tags=["settings"], 
    dependencies=[Depends(get_current_user)]
)
