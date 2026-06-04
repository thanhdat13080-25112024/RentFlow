import os
import secrets
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(".env")

def _get_or_create_secret_key() -> str:
    """Lấy SECRET_KEY theo thứ tự ưu tiên:
    1. Biến môi trường SECRET_KEY (cách dùng trên Vercel / production).
    2. Dòng SECRET_KEY= trong .env (dev cục bộ).
    3. Sinh mới và ghi vào .env để các lần restart sau dùng lại.

    Trên serverless (Vercel) hệ thống file ở chế độ read-only nên việc ghi .env
    sẽ ném OSError — ta bắt lỗi và dùng key tạm trong bộ nhớ. Vì vậy PHẢI đặt
    SECRET_KEY làm biến môi trường trên production để giữ JWT cookie ổn định."""
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("SECRET_KEY="):
                return line.split("=", 1)[1].strip()
    key = secrets.token_urlsafe(32)
    try:
        with _ENV_FILE.open("a", encoding="utf-8") as f:
            f.write(f"\nSECRET_KEY={key}\n")
    except OSError:
        # Read-only filesystem (serverless). Key chỉ sống trong process này.
        pass
    return key

class Settings(BaseSettings):
    PROJECT_NAME: str = "RentFlow"

    # Nguồn URL database. Ưu tiên DATABASE_URL (production/Vercel, Postgres);
    # nếu None thì dùng SQLALCHEMY_DATABASE_URL (dev cục bộ, SQLite).
    DATABASE_URL: str | None = None
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./rentflow.db"

    # Seed 12 phòng + hoá đơn mẫu khi DB rỗng. Bật cho dev; TẮT trên production
    # (đặt SEED_SAMPLE_DATA=false) để không chèn dữ liệu giả vào DB thật.
    SEED_SAMPLE_DATA: bool = True

    # Môi trường chạy: "development" (mặc định) hoặc "production".
    # production → cookie auth bật secure=True (yêu cầu HTTPS).
    ENVIRONMENT: str = "development"

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Auth settings
    SECRET_KEY: str = _get_or_create_secret_key()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Admin credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123" # Khuyên dùng đổi qua .env

    # Electricity settings — giá điện mặc định khi bảng settings chưa có
    # (seeder cũng dùng đúng giá trị này để đồng bộ một nguồn duy nhất).
    DEFAULT_ELECTRICITY_UNIT_PRICE: int = 3500

    # Bank settings
    BANK_NAME: str = "MB"
    BANK_ACCOUNT: str = ""
    ACCOUNT_HOLDER: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @model_validator(mode="after")
    def _resolve_database_url(self):
        """Nếu DATABASE_URL được set (production), dùng nó thay cho mặc định SQLite.
        Neon/Heroku trả scheme 'postgres://' nhưng SQLAlchemy cần 'postgresql://'."""
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            self.SQLALCHEMY_DATABASE_URL = url
        return self

settings = Settings()
