from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_safe_failure_response():
    response = client.post(
        "/credit/evaluate",
        json={}  
    )

    assert response.status_code in [400, 422]
