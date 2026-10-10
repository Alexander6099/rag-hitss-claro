"""Valida estructura del banco; no simula ni calcula métricas de RAG."""
import json
from pathlib import Path

DATA_PATH = Path(__file__).with_name("gold_standard_queries.json")

def main():
    queries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(queries, list) or not queries:
        raise ValueError("El banco debe ser una lista no vacía.")
    ids = [q.get("id") for q in queries]
    if any(not qid for qid in ids) or len(ids) != len(set(ids)):
        raise ValueError("Faltan IDs o existen IDs duplicados.")
    if any(not q.get("pregunta") for q in queries):
        raise ValueError("Hay preguntas vacías.")
    print(f"Preguntas cargadas: {len(queries)}")
    print("Validación estructural completada.")
    print("Fuentes y respuestas técnicas requieren verificación humana.")
    print("No se ejecutó RAG ni se calcularon métricas.")

if __name__ == "__main__":
    main()
