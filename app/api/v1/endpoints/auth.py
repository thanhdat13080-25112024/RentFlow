from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(response: Response, data: LoginRequest):
    if data.username != settings.ADMIN_USERNAME or data.password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(subject=data.username)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=settings.ENVIRONMENT == "production",
    )
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
