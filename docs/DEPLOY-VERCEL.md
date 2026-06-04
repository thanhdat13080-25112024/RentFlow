# Deploying RentFlow to Vercel

RentFlow was originally a stateful server app (uvicorn + a local SQLite file).
Vercel runs your code as **stateless serverless functions on a read-only
filesystem**, so two things had to change to avoid `FUNCTION_INVOCATION_FAILED`:

1. **No local file writes.** `SECRET_KEY` is read from an env var instead of
   being written to `.env` at startup (`app/core/config.py`).
2. **No local SQLite file.** The database moves to a managed Postgres
   (writes to the local disk would raise *"readonly database"*). The app reads
   `DATABASE_URL` from the environment; locally it still falls back to SQLite.

## What's in the repo for Vercel

| File | Role |
|------|------|
| `api/index.py` | Serverless entrypoint — exposes the FastAPI `app` to Vercel |
| `vercel.json`  | Routes every request to `api/index.py`, bundles the `app/` package |
| `requirements.txt` | Adds `psycopg2-binary` (Postgres driver) |

## One-time setup

### 1. Create a Postgres database (Neon — free tier, Vercel-friendly)
1. Sign up at <https://neon.tech> and create a project.
2. Copy the **pooled** connection string. It looks like:
   `postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require`

### 2. Create the schema in that database (run once, from your machine)
```bash
# point your local app at Neon and let Alembic build the tables
export DATABASE_URL="postgresql://...pooler...?sslmode=require"
alembic upgrade head
```
(The app also runs `create_all()` on startup as a safety net, but Alembic is the
source of truth — see `CLAUDE.md`.)

### 3. Import the project into Vercel
1. Push this branch to GitHub and "Import Project" in the Vercel dashboard, **or**
   run `vercel` with the CLI from the repo root.
2. Framework preset: **Other** (the `vercel.json` already describes the build).

### 4. Set Environment Variables in Vercel (Project → Settings → Environment Variables)

| Name | Value | Why |
|------|-------|-----|
| `DATABASE_URL` | your Neon pooled connection string | Postgres instead of SQLite |
| `SECRET_KEY` | output of `python -c "import secrets; print(secrets.token_urlsafe(32))"` | stable JWT signing; must NOT change between deploys or users get logged out |
| `ADMIN_USERNAME` | your admin login | — |
| `ADMIN_PASSWORD` | a strong password | don't ship the `admin123` default |
| `SEED_SAMPLE_DATA` | `false` | otherwise 12 fake rooms get inserted into your real DB |
| `ENVIRONMENT` | `production` | sets `secure=True` on the auth cookie (Vercel serves HTTPS) |

### 5. Deploy
Push to the connected branch (or `vercel --prod`). Visit the deployment URL and
log in with your admin credentials.

## Troubleshooting `FUNCTION_INVOCATION_FAILED`
Open **Vercel → your deployment → Logs** (or `vercel logs <url>`) and read the
Python traceback. Common causes:

- `readonly database` / `OSError: Read-only file system` → `DATABASE_URL` not set,
  so it fell back to SQLite. Set it.
- `could not connect to server` / SSL errors → wrong/missing `sslmode=require`,
  or using the non-pooled Neon host. Use the **pooled** string.
- `ModuleNotFoundError` → a dependency missing from `requirements.txt`.
- Login works then breaks after redeploy → `SECRET_KEY` is changing between
  deploys. Set it as a fixed env var.

## Note on data persistence
Never rely on the local SQLite file (`rentflow.db`) in production — each
serverless invocation may run on a fresh, wiped container. All durable state
must live in Postgres.
