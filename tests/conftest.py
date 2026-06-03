"""Shared pytest fixtures.

- `db`: an isolated in-memory SQLite session for unit-testing the service layer.
- `client`: a FastAPI TestClient backed by a fresh seeded in-memory DB, with the
  app's `get_db` dependency overridden so tests never touch the real rentflow.db.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401 — register models on Base.metadata
from app.db import Base


def _make_engine():
    # StaticPool + shared in-memory DB so every connection sees the same schema/data.
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture
def db():
    engine = _make_engine()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.api.deps import get_db
    from app.main import app
    from app.services.seeder import seed_initial_data

    engine = _make_engine()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as s:
        seed_initial_data(s)

    def override_get_db():
        s = Session()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
