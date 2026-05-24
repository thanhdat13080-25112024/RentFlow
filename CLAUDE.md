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
  ├── GET /  → renders index.html (auth-gated via cookie check)
  ├── GET /login → renders login.html
  └── /api/* → api_router (app/api/v1/api.py)
       ├── /auth  → endpoints/auth.py   (public)
       └── /rooms, /bills, /electricity, /settings  (all require JWT cookie)
```

Auth is cookie-based JWT. The `get_current_user` dependency in `app/core/security.py` reads the `access_token` cookie. All protected routers declare `dependencies=[Depends(get_current_user)]` in `app/api/v1/api.py`.

### Key files

| File | Purpose |
|------|---------|
| `app/core/config.py` | `Settings` class (pydantic-settings, reads `.env`) |
| `app/core/database.py` | SQLAlchemy engine, `SessionLocal`, `get_db()` dependency, `Base` |
| `app/models/entities.py` | All ORM models: `Room`, `ElectricityReading`, `MonthlyBill`, `Setting` |
| `app/schemas/data_transfer_objects.py` | All Pydantic request/response schemas |
| `app/services/billing.py` | `update_bill()` — creates or recalculates a bill for one room/month; **caller must commit** |
| `app/services/database_seeder.py` | `init_data()` — seeds default settings and 12 sample rooms on first run |

### Billing logic

`update_bill(db, room, month, year)` is the core business function. It:
1. Looks up `ElectricityReading` for the room+month
2. Calculates `electricity_fee` (meter: `usage × unit_price`, fixed: `room.fixed_electricity_fee`)
3. Creates or updates a `MonthlyBill` record — **only updates if `status == "unpaid"`**, never overwrites paid/prepaid bills
4. Calls `db.flush()` — the **caller must call `db.commit()`**

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
