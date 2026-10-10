from fastapi import FastAPI
from backend.app.schemas import QueryRequest, QueryResponse

app = FastAPI(
    title="API RAG Global Hitss - Prototipo",
    version="0.2.0",
    description="Esqueleto técnico. El pipeline RAG real aún no está integrado."
)

@app.get("/", tags=["health"])
def read_root():
    return {"status": "ok", "service": "RAG Assistant - prototipo",
            "rag_pipeline": "not_integrated"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}

@app.post("/api/v1/query", response_model=QueryResponse, tags=["query"])
def query(request: QueryRequest):
    # Abstención explícita: no inventar respuestas ni citas sin recuperación real.
    return QueryResponse(
        status="not_implemented",
        answer="La consulta RAG todavía no está conectada a un corpus documental.",
        citations=[],
        abstained=True,
        message="No se generó respuesta técnica: falta integrar recuperación y generación."
    )
