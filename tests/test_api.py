from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_does_not_claim_rag_is_implemented():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["rag_pipeline"] == "not_integrated"

def test_query_abstains_until_real_pipeline_exists():
    response = client.post("/api/v1/query",
        json={"question": "¿Cuál es el procedimiento de escalamiento FTTH?"})
    assert response.status_code == 200
    body = response.json()
    assert body["abstained"] is True
    assert body["citations"] == []
    assert body["status"] == "not_implemented"
