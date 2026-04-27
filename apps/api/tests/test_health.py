"""Health check test — runs without a database connection."""

from fastapi.testclient import TestClient


def test_health(sync_client: TestClient) -> None:
    response = sync_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
