from fastapi import FastAPI

app = FastAPI(title="API RAG Global Hitss", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "RAG Assistant Global Hitss - Claro Peru"}
