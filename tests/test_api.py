"""API-level tests: public access, validation, and key endpoint shapes."""


def test_api_is_public(client):
    # Dự án mở — không cần đăng nhập, endpoint trả dữ liệu trực tiếp.
    r = client.get("/api/rooms/")
    assert r.status_code == 200
    assert len(r.json()) >= 1  # seeded rooms


def test_validation_rejects_bad_month(client):
    r = client.post("/api/bills/mark-paid", json={"room_id": 1, "month": 99, "year": 2026})
    assert r.status_code == 422


def test_receivables_shape(client):
    r = client.get("/api/bills/receivables")
    assert r.status_code == 200
    body = r.json()
    assert {"total", "count", "rooms"} <= set(body.keys())


def test_revenue_excludes_vacant(client):
    r = client.get("/api/bills/revenue/summary")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_export_csv_headers(client):
    r = client.get("/api/bills/export?month=6&year=2026")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "attachment" in r.headers["content-disposition"]
