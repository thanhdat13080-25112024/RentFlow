"""API-level tests: auth gating, validation, and key endpoint shapes."""


def _login(client):
    return client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})


def test_protected_api_requires_auth(client):
    # No cookie → 401 (trailing slash avoids the 307 redirect).
    assert client.get("/api/rooms/").status_code == 401


def test_login_then_access(client):
    assert _login(client).status_code == 200
    r = client.get("/api/rooms/")
    assert r.status_code == 200
    assert len(r.json()) >= 1  # seeded rooms


def test_login_wrong_password(client):
    r = client.post("/api/auth/login", json={"username": "admin", "password": "nope"})
    assert r.status_code == 401


def test_validation_rejects_bad_month(client):
    _login(client)
    r = client.post("/api/bills/mark-paid", json={"room_id": 1, "month": 99, "year": 2026})
    assert r.status_code == 422


def test_receivables_shape(client):
    _login(client)
    r = client.get("/api/bills/receivables")
    assert r.status_code == 200
    body = r.json()
    assert {"total", "count", "rooms"} <= set(body.keys())


def test_revenue_excludes_vacant(client):
    _login(client)
    r = client.get("/api/bills/revenue/summary")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_export_csv_headers(client):
    _login(client)
    r = client.get("/api/bills/export?month=6&year=2026")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "attachment" in r.headers["content-disposition"]
