# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app (dev mode with auto-reload)
python main.py
# or
uvicorn app.main:app --reload

# Access at http://localhost:8000
# Default login: admin / admin123 (set in .env)

# Database migrations
alembic upgrade head                                    # Apply pending migrations
alembic revision --autogenerate -m "describe change"   # Generate new migration from model diff
alembic downgrade -1                                    # Roll back one migration
```

## Architecture

**RentFlow** is a single-admin property management app. All state lives server-side in SQLite; the frontend is Jinja2-rendered HTML with Alpine.js for interactivity — there is no separate SPA build step.

### Request flow

```
Browser → FastAPI (app/main.py)
  ├── GET /       → index.html if logged in, else redirect → /login (app/api/web.py)
  ├── GET /login  → renders login.html (redirects → / if already logged in)
  └── /api/* → api_router (app/api/v1/router.py)
       ├── /auth  → endpoints/auth.py  (public: login/logout)
       └── /rooms, /bills, /electricity, /settings → endpoints/*.py  (require JWT cookie)
```

Auth is cookie-based JWT. `get_current_user` in `app/core/security.py` reads the `access_token` cookie (and the non-raising `get_subject_from_token` helper is shared with the web routes). In `app/api/v1/router.py` the rooms/bills/electricity/settings routers are registered with `dependencies=[Depends(get_current_user)]`, so they return 401 without a valid cookie. `GET /` and `GET /login` enforce the same check at the page level via `app/api/web.py`. The frontend treats 401 by not rendering data; an expired session is fully resolved by reloading `/` (which redirects to `/login`).

### Key files

| File | Purpose |
|------|---------|
| `app/core/config.py` | `Settings` class (pydantic-settings, reads `.env`) |
| `app/db/` | `base.py` (`Base`), `session.py` (engine, `SessionLocal`, `get_db()`), `__init__.py` re-exports them |
| `app/models/*.py` | One model per file (`room.py`, `electricity_reading.py`, `monthly_bill.py`, `setting.py`); `__init__.py` exports `Room`, `ElectricityReading`, `MonthlyBill`, `Setting` |
| `app/schemas/*.py` | One group per file (`bill.py`, `electricity.py`, `room.py`, `setting.py`); import via `from app.schemas import ...` |
| `app/services/billing.py` | `update_bill()` — creates or recalculates a bill for one room/month; **calls `db.commit()` itself** |
| `app/services/seeder.py` | `seed_initial_data()` — seeds default settings and sample rooms on first run |

### Billing logic

`update_bill(db, room, month, year)` is the core business function. It:
1. Looks up `ElectricityReading` for the room+month
2. Calculates `electricity_fee` (meter: `usage × unit_price`, fixed: `room.fixed_electricity_fee`)
3. Creates or updates a `MonthlyBill` record — **only updates if `status == "unpaid"`**, never overwrites paid/prepaid bills
4. Calls `db.commit()` itself (so when called in a loop, e.g. `/api/bills/`, it commits per iteration)

This function is called from GET endpoints (`/api/bills/`) to auto-create bills on first access.

### Frontend

All UI is in `app/templates/`. The single Alpine.js component `app(initialMonth, initialYear)` is defined in `app/static/js/app.js`. It holds all state (bills, rooms, modals) and communicates with the backend via `fetch()` calls to `/api/*`.

`TRANSLATIONS` object at the top of `app.js` handles i18n for vi/en/ko/ja/zh — add keys there when adding new UI text.

## Environment

Requires a `.env` file in the project root (copy from `.env.example`):

```
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password
```

`SECRET_KEY` must be stable across restarts — if it changes, all existing JWT cookies become invalid and users are logged out.

Set `ENVIRONMENT=production` to enable `secure=True` on the auth cookie (requires HTTPS).

## Database

Schema is managed by both `Base.metadata.create_all()` (on startup) and Alembic. When adding a new column to a model, create a migration with `alembic revision --autogenerate` rather than relying solely on `create_all`.

The `settings` table stores runtime config (electricity unit price, bank details) edited via the Settings UI tab — do not hardcode these values in app code.

## Harness: RentFlow

**Mục tiêu:** Đội agent chuyên biệt cho phát triển full-stack (API + UI), thiết kế UI, và review/sửa lỗi trên RentFlow.

**Trigger:** Yêu cầu phát triển tính năng (API + UI), chỉnh giao diện/dashboard, hoặc review/debug → dùng skill `rentflow-orchestrator`. Câu hỏi đơn giản trả lời trực tiếp.

Agent ở `.claude/agents/` (rentflow-backend, -frontend, -qa, -reviewer); skill tương ứng + orchestrator ở `.claude/skills/`. Chế độ: sub-agent (môi trường không có team tools).

**Changelog:**
| Ngày | Thay đổi | Đối tượng | Lý do |
|------|----------|-----------|-------|
| 2026-06-03 | Khởi tạo harness | toàn bộ (4 agent + 5 skill) | Hỗ trợ full-stack / UI / review theo yêu cầu |
