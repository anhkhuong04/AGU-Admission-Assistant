from fastapi.testclient import TestClient

from agu_api.main import create_app


def test_health_returns_only_status() -> None:
    with TestClient(create_app()) as client:
        for _ in range(2):
            response = client.get("/api/v1/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}


def test_no_public_knowledge_or_approval_routes() -> None:
    app = create_app()
    assert set(app.openapi()["paths"]) == {"/api/v1/health"}
