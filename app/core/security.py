from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import HTTPException, Request, status
from jose import jwt

from app.core.config import settings

_pwd_context = None


def get_pwd_context():
    global _pwd_context
    if _pwd_context is None:
        from passlib.context import CryptContext
        _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return _pwd_context


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_pwd_context().verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return get_pwd_context().hash(password)

def get_subject_from_token(token: Optional[str]) -> Optional[str]:
    """Giải mã JWT từ cookie, trả về 'sub' (username) nếu hợp lệ, ngược lại None.

    Không ném lỗi — dùng được cả cho API guard (get_current_user) lẫn trang web
    (web.py quyết định redirect thay vì trả 401)."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None

async def get_current_user(request: Request):
    subject = get_subject_from_token(request.cookies.get("access_token"))
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return subject
