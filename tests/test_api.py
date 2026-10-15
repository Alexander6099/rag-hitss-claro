from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

<<<<<<< HEAD
def test_web_frontend_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Asistente técnico documental" in response.text

def test_query_validates_short_questions():
    response = client.post("/api/v1/query", json={"question": "a"})
    assert response.status_code == 422

def test_document_upload_requires_configured_token(monkeypatch):
    monkeypatch.setenv("API_ACCESS_TOKEN", "test-secret")
    response = client.post("/api/v1/documents", files={"file": ("test.pdf", b"fake", "application/pdf")})
    assert response.status_code == 401

def test_query_provider_error_does_not_expose_secrets(monkeypatch):
    from backend.app import main
    monkeypatch.delenv("API_ACCESS_TOKEN", raising=False)
    def fail(_question):
        raise RuntimeError("OPENAI_API_KEY=secret-token")
    monkeypatch.setattr(main, "answer_question", fail)
    response = client.post("/api/v1/query", json={"question": "¿Cómo verificar una incidencia?"})
    assert response.status_code == 503
    assert "secret-token" not in response.text


def test_upload_receives_form_version(monkeypatch):
    from backend.app import main
    monkeypatch.setenv("API_ACCESS_TOKEN", "test-secret")
    received = []

    def ingest(filename, data, version):
        received.append((filename, data, version))
        return dict(document_id=1, document=filename, pages_with_text=1, chunks_created=2)

    monkeypatch.setattr(main, "ingest_pdf", ingest)
    response = client.post("/api/v1/documents", headers={"Authorization": "Bearer test-secret"},
                           files={"file": ("test.pdf", b"pdf", "application/pdf")}, data={"version": "v2"})
    assert response.status_code == 200
    assert received == [("test.pdf", b"pdf", "v2")]


def test_transient_provider_failure_is_explained(monkeypatch):
    from backend.app import main
    monkeypatch.delenv("API_ACCESS_TOKEN", raising=False)

    def fail(_question):
        raise main.ProviderUnavailable("Gemini no está disponible temporalmente.")

    monkeypatch.setattr(main, "answer_question", fail)
    response = client.post("/api/v1/query", json={"question": "¿Cuál es la IP?"})
    assert response.status_code == 503
    assert "Gemini" in response.json()["detail"]
    assert response.headers["Retry-After"] == "30"
=======
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
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
