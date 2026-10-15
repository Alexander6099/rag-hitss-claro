"""Resume mediciones reales desde JSON; no genera datos ni resultados ficticios."""
import json, sys
from pathlib import Path
import numpy as np

def summarize(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    latencies = [float(r["latency_ms"]) for r in rows if r.get("latency_ms") is not None]
    if not latencies:
        raise ValueError("No hay mediciones latency_ms en el archivo.")
    out = {
        "n_observaciones_con_latencia": len(latencies),
        "latencia_media_ms": round(float(np.mean(latencies)), 2),
        "latencia_mediana_ms": round(float(np.median(latencies)), 2),
        "latencia_p95_ms": round(float(np.percentile(latencies, 95)), 2),
        "nota": "Estadísticas descriptivas del archivo de entrada."
    }
    for field in ("answer_f1", "context_recall"):
        vals = [float(r[field]) for r in rows if r.get(field) is not None]
        if vals:
            out[field + "_media"] = round(float(np.mean(vals)), 4)
            out[field + "_n"] = len(vals)
    flags = [r["citation_correct"] for r in rows if isinstance(r.get("citation_correct"), bool)]
    if flags:
        out["citas_correctas_pct"] = round(100 * sum(flags) / len(flags), 2)
        out["citas_n"] = len(flags)
    return out

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/calcular_metricas.py ruta/mediciones.json")
    print(json.dumps(summarize(sys.argv[1]), indent=2, ensure_ascii=False))
