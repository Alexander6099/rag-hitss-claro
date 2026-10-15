from __future__ import annotations

import logging
import os
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from backend.app.schemas import QueryRequest, QueryResponse
from backend.app.services.rag import ProviderUnavailable, answer_question, ingest_pdf

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Asistente técnico RAG — Prototipo académico",
    version="1.0.0",
    description=("Prototipo de recuperación híbrida y generación fundamentada. "
                 "Su validez técnica depende del corpus autorizado, la configuración y las pruebas documentadas."),
)


class IngestResponse(BaseModel):
    document_id: int
    document: str
    pages_with_text: int
    chunks_created: int


@app.get("/", response_class=HTMLResponse, tags=["web"])
def index():
    return """<!doctype html><html lang='es'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>Asistente técnico RAG</title><style>body{font:16px system-ui;max-width:850px;margin:40px auto;padding:0 18px;color:#222}textarea,input,button{font:inherit;padding:10px;width:100%;box-sizing:border-box;margin:6px 0}button{cursor:pointer}pre{white-space:pre-wrap;background:#f4f4f4;padding:14px;border-radius:8px}small{color:#555}</style>
    <h1>Asistente técnico documental</h1><p>Prototipo académico. Usa únicamente documentos autorizados y verifica las fuentes antes de aplicar procedimientos.</p>
    <label>Token de acceso (si está configurado)</label><input id='token' type='password' placeholder='Token API'>
    <label>Pregunta técnica</label><textarea id='q' rows='4' placeholder='Escribe tu consulta técnica…'></textarea><button onclick='ask()'>Consultar</button>
    <h2>Resultado</h2><pre id='out'>Aquí aparecerá la respuesta y sus fuentes.</pre>
    <hr><h2>Ingesta de PDF (administración)</h2><input id='pdf' type='file' accept='application/pdf'><input id='version' placeholder='Versión del documento (opcional)'><button onclick='upload()'>Cargar PDF</button><pre id='ingestout'></pre>
    <script>function headers(){let t=document.getElementById('token').value;return t?{'Authorization':'Bearer '+t}:{};} async function ask(){let out=document.getElementById('out');out.textContent='Consultando…';try{let r=await fetch('/api/v1/query',{method:'POST',headers:{'Content-Type':'application/json',...headers()},body:JSON.stringify({question:document.getElementById('q').value})});out.textContent=JSON.stringify(await r.json(),null,2)}catch(e){out.textContent='Error de conexión: '+e}}
    async function upload(){let f=document.getElementById('pdf').files[0];if(!f){alert('Selecciona un PDF');return}let d=new FormData();d.append('file',f);d.append('version',document.getElementById('version').value);let o=document.getElementById('ingestout');o.textContent='Procesando…';try{let r=await fetch('/api/v1/documents',{method:'POST',headers:headers(),body:d});o.textContent=JSON.stringify(await r.json(),null,2)}catch(e){o.textContent='Error: '+e}}</script></html>"""


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy", "service": "rag-api"}


def _authorize(authorization: str | None, required: bool = False) -> None:
    expected = os.getenv("API_ACCESS_TOKEN", "").strip()
    if not expected:
        if required:
            raise HTTPException(status_code=503, detail="Configura API_ACCESS_TOKEN antes de habilitar la ingesta.")
        return
    if not authorization or authorization != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="Token de acceso inválido o ausente.")


@app.post("/api/v1/documents", response_model=IngestResponse, tags=["documents"])
def upload_document(file: UploadFile = File(...), version: str = Form(""), authorization: str | None = Header(default=None)):
    _authorize(authorization, required=True)
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail="El archivo debe ser PDF.")
    data = file.file.read()
    try:
        return ingest_pdf(file.filename or "documento.pdf", data, version or None)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ProviderUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc), headers={"Retry-After": "30"}) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail="Servicio de ingesta no disponible; revisa la configuración del entorno.") from exc
    except Exception as exc:
        logger.error("Fallo de ingesta (%s)", type(exc).__name__)
        raise HTTPException(status_code=503, detail="No se pudo guardar el PDF. Comprueba la conexión con Gemini y la base de datos.") from exc


@app.post("/api/v1/query", response_model=QueryResponse, tags=["query"])
def query(request: QueryRequest, authorization: str | None = Header(default=None)):
    _authorize(authorization)
    try:
        result = answer_question(request.question)
        return QueryResponse(**result)
    except ProviderUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc), headers={"Retry-After": "30"}) from exc
    except RuntimeError as exc:
        logger.exception("Consulta RAG no completada: %s", exc)
        raise HTTPException(status_code=503, detail="No se pudo completar la consulta. Revisa los logs del backend para ver la causa; no se muestran detalles sensibles en la respuesta.") from exc
    except Exception as exc:
        # Keep the full diagnostic on the server, never return provider secrets to the browser.
        logger.exception("Error inesperado durante la consulta RAG: %s", exc)
        raise HTTPException(status_code=503, detail="No se pudo completar la consulta. Revisa los logs del backend para ver la causa; no se muestran detalles sensibles en la respuesta.") from exc
