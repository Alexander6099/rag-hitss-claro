import pytest

from backend.app.services.rag import ProviderUnavailable, _provider_call


class ProviderError(Exception):
    def __init__(self, code):
        self.code = code


def test_temporary_failure_recovers(monkeypatch):
    monkeypatch.setattr("backend.app.services.rag.time.sleep", lambda _: None)
    calls = []

    def operation(**kwargs):
        calls.append(kwargs)
        if len(calls) < 3:
            raise ProviderError(503)
        return "respuesta"

    assert _provider_call(operation, model="test") == "respuesta"
    assert calls == [{"model": "test"}] * 3


def test_exhausted_retries_report_unavailability(monkeypatch):
    monkeypatch.setattr("backend.app.services.rag.time.sleep", lambda _: None)
    calls = []

    def operation():
        calls.append(1)
        raise ProviderError(429)

    with pytest.raises(ProviderUnavailable):
        _provider_call(operation)
    assert len(calls) == 3


def test_permanent_error_is_not_retried():
    calls = []

    def operation():
        calls.append(1)
        raise ProviderError(400)

    with pytest.raises(ProviderError):
        _provider_call(operation)
    assert len(calls) == 1


def test_timeout_returns_safe_error_after_retries(monkeypatch):
    import httpx
    monkeypatch.setattr("backend.app.services.rag.time.sleep", lambda _: None)
    calls = []

    def operation():
        calls.append(1)
        raise httpx.ReadTimeout("secret-provider-url")

    with pytest.raises(ProviderUnavailable) as error:
        _provider_call(operation)
    assert len(calls) == 3
    assert "secret-provider-url" not in str(error.value)
