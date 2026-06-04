# Vercel serverless entrypoint.
# Vercel's @vercel/python runtime serves the ASGI `app` callable found here.
# All routing is funneled to this file by vercel.json.
from app.main import app  # noqa: F401  (re-exported for Vercel to discover)
