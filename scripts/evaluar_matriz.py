"""Calcula la matriz comparativa a partir de mediciones reales y trazables.

Entrada: JSON con 50 o más consultas únicas por candidato A/B/C. Cada registro debe
contener candidate, query_id, answer_f1, context_recall, latency_ms (lista de repeticiones),
citation_correct (bool) y cost_usd. Este script no genera ni rellena datos faltantes.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np

WEIGHTS = {"C1": 0.30, "C2": 0.20, "C3": 0.10, "C4": 0.25, "C5": 0.15}
WEIGHT_SCHEMES = {
    "base": WEIGHTS,
    "equal": {"C1": 0.20, "C2": 0.20, "C3": 0.20, "C4": 0.20, "C5": 0.20},
    "efficiency": {"C1": 0.20, "C2": 0.35, "C3": 0.10, "C4": 0.10, "C5": 0.25},
    "quality": {"C1": 0.40, "C2": 0.10, "C3": 0.10, "C4": 0.30, "C5": 0.10},
}
THEORETICAL_C3 = {"A": 5, "B": 4, "C": 3}
CANDIDATES = ("A", "B", "C")


def _score_f1(f1: float, recall: float) -> int:
    if f1 >= 0.88: score = 5
    elif f1 >= 0.85: score = 4
    elif f1 >= 0.75: score = 3
    elif f1 >= 0.65: score = 2
    else: score = 1
    if recall < 0.85:
        score = min(score, 3)
    return score


def _score_latency(p95: float) -> int:
    if p95 <= 2000: return 5
    if p95 <= 3500: return 4
    if p95 <= 5000: return 3
    if p95 <= 8000: return 2
    return 1


def _score_citations(percent: float) -> int:
    if percent >= 98: return 5
    if percent >= 90: return 4
    if percent >= 75: return 3
    if percent >= 50: return 2
    return 1


def _score_cost(cost_per_1000: float) -> int:
    if cost_per_1000 <= 2: return 5
    if cost_per_1000 <= 3: return 4
    if cost_per_1000 <= 5: return 3
    if cost_per_1000 <= 8: return 2
    return 1


def evaluate(rows: list[dict], minimum_queries: int = 50) -> dict:
    if not isinstance(rows, list) or not rows:
        raise ValueError("El archivo debe contener mediciones reales no vacías.")
    by_candidate = {c: [] for c in CANDIDATES}
    for row in rows:
        candidate = row.get("candidate")
        if candidate not in by_candidate:
            raise ValueError(f"Candidato inválido: {candidate!r}; use A, B o C.")
        required = ("query_id", "answer_f1", "context_recall", "latency_ms", "citation_correct", "cost_usd")
        missing = [key for key in required if key not in row or row[key] is None]
        if missing:
            raise ValueError(f"Registro {candidate}/{row.get('query_id')}: faltan datos {missing}.")
        if not isinstance(row["latency_ms"], list) or not row["latency_ms"]:
            raise ValueError(f"Registro {candidate}/{row.get('query_id')}: latency_ms debe ser una lista de mediciones.")
        if not isinstance(row["citation_correct"], bool):
            raise ValueError("citation_correct debe ser booleano validado manualmente.")
        if not 0 <= float(row["answer_f1"]) <= 1 or not 0 <= float(row["context_recall"]) <= 1:
            raise ValueError("answer_f1 y context_recall deben estar entre 0 y 1.")
        if float(row["cost_usd"]) < 0 or any(float(ms) < 0 for ms in row["latency_ms"]):
            raise ValueError("Costo y latencias no pueden ser negativos.")
        by_candidate[candidate].append(row)

    output = {"weights": WEIGHTS, "candidates": {}, "winner": None,
              "warning": "Resultados calculados solo a partir de los registros de entrada; revisar procedencia y configuración antes de incluir en la tesis."}
    totals = {}
    for candidate, records in by_candidate.items():
        unique_ids = {r["query_id"] for r in records}
        if len(unique_ids) < minimum_queries:
            raise ValueError(f"Candidato {candidate}: hay {len(unique_ids)} consultas únicas; se requieren al menos {minimum_queries}.")
        f1 = float(np.mean([float(r["answer_f1"]) for r in records]))
        recall = float(np.mean([float(r["context_recall"]) for r in records]))
        latencies = [float(ms) for r in records for ms in r["latency_ms"]]
        p95 = float(np.percentile(latencies, 95))
        citation_pct = 100 * sum(r["citation_correct"] for r in records) / len(records)
        cost_per_1000 = 1000 * float(np.mean([float(r["cost_usd"]) for r in records]))
        scores = {
            "C1": _score_f1(f1, recall), "C2": _score_latency(p95),
            "C3": THEORETICAL_C3[candidate], "C4": _score_citations(citation_pct),
            "C5": _score_cost(cost_per_1000),
        }
        total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
        totals[candidate] = total
        output["candidates"][candidate] = {
            "n_queries": len(unique_ids), "f1_mean": round(f1, 4), "context_recall_mean": round(recall, 4),
            "latency_p95_ms": round(p95, 2), "citation_correct_pct": round(citation_pct, 2),
            "cost_usd_per_1000_queries": round(cost_per_1000, 4), "scores": scores,
            "weighted_total": round(total, 4),
        }
    output["winner"] = max(totals, key=totals.get)
    output["weighted_totals"] = {k: round(v, 4) for k, v in totals.items()}
    output["sensitivity"] = {}
    for scheme_name, scheme_weights in WEIGHT_SCHEMES.items():
        scenario = {
            candidate: round(sum(output["candidates"][candidate]["scores"][key] * scheme_weights[key] for key in scheme_weights), 4)
            for candidate in CANDIDATES
        }
        output["sensitivity"][scheme_name] = {
            "weights": scheme_weights,
            "totals": scenario,
            "winner": max(scenario, key=scenario.get),
        }
    return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/evaluar_matriz.py ruta/mediciones_candidatos.json")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(evaluate(data), indent=2, ensure_ascii=False))
