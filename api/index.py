# Vercel serverless entrypoint.
import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào sys.path để Vercel tìm thấy package `app`
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# Vercel's @vercel/python runtime serves the ASGI `app` callable found here.
# All routing is funneled to this file by vercel.json.
from app.main import app  # noqa: F401  (re-exported for Vercel to discover)
