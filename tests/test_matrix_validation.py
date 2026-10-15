import pytest
from scripts.evaluar_matriz import evaluate


def test_matrix_refuses_missing_empirical_data():
    with pytest.raises(ValueError, match="faltan datos"):
        evaluate([{"candidate": "A", "query_id": "Q01"}], minimum_queries=1)


def test_matrix_refuses_too_few_queries():
    row = {"candidate": "A", "query_id": "Q01", "answer_f1": 0.9,
           "context_recall": 0.9, "latency_ms": [100], "citation_correct": True, "cost_usd": 0.001}
    with pytest.raises(ValueError, match="se requieren al menos"):
        evaluate([row], minimum_queries=50)
