from backend.app.services.rag import RetrievedChunk, _chunk_page
from scripts.evaluar_matriz import _score_f1, _score_latency, _score_citations, _score_cost


def test_chunk_page_preserves_text_and_bounds_chunk_size():
    chunks = _chunk_page("Primer párrafo.\n\nSegundo párrafo." * 80, max_chars=300, overlap=40)
    assert chunks
    assert all(text for _, text in chunks)
    assert all(len(text) <= 300 for _, text in chunks)


def test_citation_uses_only_supplied_metadata():
    chunk = RetrievedChunk(1, "manual.pdf", "v2", 8, 3, "texto", dense_score=0.7)
    assert chunk.citation() == {"document": "manual.pdf", "version": "v2", "page": 8, "paragraph": 3}


def test_score_conversion_bands():
    assert _score_f1(0.90, 0.90) == 5
    assert _score_f1(0.90, 0.80) == 3
    assert _score_latency(5000) == 3
    assert _score_citations(98) == 5
    assert _score_cost(3) == 4


def test_retrieve_falls_back_to_lexical_search_when_embedding_quota_fails(monkeypatch):
    from backend.app.services import rag

    class FakeCursor:
        def __init__(self):
            self.calls = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def execute(self, _sql, _params):
            self.calls += 1

        def fetchall(self):
            return [{
                "chunk_id": 7,
                "document_name": "manual-prueba.pdf",
                "version": "v1",
                "page_number": 1,
                "paragraph_number": 1,
                "chunk_text": "El equipo ROUTER-TEST-01 usa la IP 192.168.1.1.",
                "lexical_score": 0.8,
            }]

    class FakeConnection:
        def __init__(self):
            self.cursor_obj = FakeCursor()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def cursor(self, **_kwargs):
            return self.cursor_obj

    import sys
    import types
    connection = FakeConnection()
    fake_psycopg2 = types.ModuleType("psycopg2")
    fake_extras = types.ModuleType("psycopg2.extras")
    fake_extras.RealDictCursor = object
    fake_psycopg2.extras = fake_extras
    monkeypatch.setitem(sys.modules, "psycopg2", fake_psycopg2)
    monkeypatch.setitem(sys.modules, "psycopg2.extras", fake_extras)
    monkeypatch.setattr(rag, "_embed", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("429 RESOURCE_EXHAUSTED")))
    monkeypatch.setattr(rag, "_db_connect", lambda: connection)

    chunks = rag._retrieve("¿Cuál es la IP de ROUTER-TEST-01?")

    assert len(chunks) == 1
    assert chunks[0].chunk_id == 7
    assert chunks[0].lexical_score == 0.8
    assert chunks[0].dense_score == 0.0
    assert connection.cursor_obj.calls == 1


def test_safe_provider_error_redacts_api_keys():
    from backend.app.services.rag import _safe_provider_error

    cleaned = _safe_provider_error(RuntimeError("API_KEY=AIza123456789012345678901234567890"))
    assert "AIza123456789012345678901234567890" not in cleaned
    assert "REDACTED" in cleaned
