"""Advanced RAG prototype: PDF ingestion, hybrid retrieval, optional reranking and grounded generation.

This module never fabricates source locations. It abstains when the retrieval signal is weak
or when the configured provider/corpus is unavailable.
"""
from __future__ import annotations

import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


class ProviderUnavailable(RuntimeError):
    """A transient provider failure after bounded retries."""


def _provider_call(operation, **kwargs):
    for attempt in range(3):
        try:
            return operation(**kwargs)
        except Exception as exc:
            import httpx
            code = getattr(exc, "code", None)
            if not isinstance(exc, httpx.TimeoutException) and str(code) not in {"429", "500", "502", "503", "504"}:
                raise
            if attempt == 2:
                raise ProviderUnavailable(
                    "Gemini no está disponible temporalmente o agotó su cuota. "
                    "Intenta de nuevo en unos minutos; si persiste, revisa la cuota de la API."
                ) from exc
            time.sleep(2 ** attempt)


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_name: str
    version: str | None
    page_number: int | None
    paragraph_number: int | None
    chunk_text: str
    dense_score: float = 0.0
    lexical_score: float = 0.0
    hybrid_score: float = 0.0
    rerank_score: float | None = None

    def citation(self) -> dict[str, Any]:
        return {
            "document": self.document_name,
            "version": self.version,
            "page": self.page_number,
            "paragraph": self.paragraph_number,
        }


def _db_connect():
    import psycopg2
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL no está configurada.")
    return psycopg2.connect(url, connect_timeout=5)


def _safe_provider_error(exc: Exception) -> str:
    """Return a useful provider error without leaking credentials."""
    message = str(exc)
    message = re.sub(r"(?i)(api[_ -]?key|authorization|bearer)\s*[:=]?\s*[^\s,;]+", r"\1=[REDACTED]", message)
    message = re.sub(r"AIza[0-9A-Za-z_-]{20,}", "[REDACTED_API_KEY]", message)
    return message[:500]


def _gemini_client():
    """Create a Google Gemini client from the environment configuration."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY no está configurada.")
    from google import genai
    # Timeout is expressed in milliseconds. Keep retries in one place above.
    return genai.Client(api_key=key, http_options={"timeout": 20000, "retry_options": {"attempts": 1}})


def _embed(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Create Gemini embeddings with the dimension expected by the pgvector schema."""
    if not texts:
        return []
    client = _gemini_client()
    model = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    response = _provider_call(client.models.embed_content,
        model=model,
        contents=texts,
        config={"task_type": task_type, "output_dimensionality": dimensions},
    )
    embeddings = getattr(response, "embeddings", None) or []
    vectors = [list(item.values) for item in embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError("Gemini no devolvió un embedding por cada texto enviado.")
    if any(len(vector) != dimensions for vector in vectors):
        raise RuntimeError(
            f"La dimensión devuelta por Gemini no coincide con EMBEDDING_DIMENSIONS={dimensions}."
        )
    return vectors


def _chunk_page(text: str, max_chars: int = 1400, overlap: int = 180) -> list[tuple[int, str]]:
    """Create bounded chunks while retaining approximate paragraph order within a page."""
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        paragraphs = [re.sub(r"\s+", " ", text).strip()] if text.strip() else []
    chunks: list[tuple[int, str]] = []
    current = ""
    start_paragraph = 1
    for idx, paragraph in enumerate(paragraphs, start=1):
        candidate = f"{current}\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append((start_paragraph, current))
        carry = current[-overlap:] if current else ""
        current = f"{carry} {paragraph}".strip()
        start_paragraph = idx
        while len(current) > max_chars:
            chunks.append((start_paragraph, current[:max_chars]))
            current = current[max_chars - overlap:]
    if current:
        chunks.append((start_paragraph, current))
    return chunks


def ingest_pdf(filename: str, pdf_bytes: bytes, version: str | None = None) -> dict[str, Any]:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Solo se aceptan archivos PDF.")
    if not pdf_bytes or len(pdf_bytes) > int(os.getenv("MAX_PDF_BYTES", str(20 * 1024 * 1024))):
        raise ValueError("El PDF está vacío o supera el tamaño máximo permitido.")
    try:
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages: list[tuple[int, str]] = []
        for page_no, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append((page_no, text))
    except Exception as exc:
        raise ValueError(f"No se pudo leer el PDF: {exc}") from exc
    if not pages:
        raise ValueError("El PDF no contiene texto extraíble. Se requiere OCR para documentos escaneados.")

    prepared: list[tuple[int, int, str]] = []
    for page_no, page_text in pages:
        for paragraph_no, chunk_text in _chunk_page(page_text):
            if chunk_text.strip():
                prepared.append((page_no, paragraph_no, chunk_text))
    vectors: list[list[float]] = []
    batch_size = 64
    for start in range(0, len(prepared), batch_size):
        vectors.extend(_embed([row[2] for row in prepared[start:start + batch_size]], task_type="RETRIEVAL_DOCUMENT"))

    with _db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents(document_name, version, source_uri, is_active) "
                "VALUES (%s, %s, %s, TRUE) RETURNING id",
                (filename, version, filename),
            )
            document_id = cur.fetchone()[0]
            from psycopg2.extras import execute_values
            records = [
                (document_id, page_no, paragraph_no, chunk_text, "[" + ",".join(f"{float(v):.8f}" for v in vector) + "]")
                for (page_no, paragraph_no, chunk_text), vector in zip(prepared, vectors)
            ]
            execute_values(
                cur,
                "INSERT INTO chunks(document_id, page_number, paragraph_number, chunk_text, embedding) VALUES %s",
                records,
                template="(%s, %s, %s, %s, %s::vector)",
                page_size=100,
            )
    return {"document_id": document_id, "document": filename, "pages_with_text": len(pages), "chunks_created": len(prepared)}


def _retrieve(question: str, limit: int = 20) -> list[RetrievedChunk]:
    # Gemini's embedding quota can be exhausted independently of text generation.
    # In that case, keep the service useful by falling back to PostgreSQL full-text search.
    vector_literal = None
    try:
        query_vector = _embed([question], task_type="RETRIEVAL_QUERY")[0]
        vector_literal = "[" + ",".join(f"{float(v):.8f}" for v in query_vector) + "]"
    except Exception as exc:
        logger.warning(
            "No se pudo generar embedding de consulta; se usará recuperación léxica. Error: %s",
            _safe_provider_error(exc),
        )

    from psycopg2.extras import RealDictCursor
    with _db_connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            dense_rows = []
            if vector_literal is not None:
                cur.execute(
                    """SELECT c.id AS chunk_id, d.document_name, d.version, c.page_number,
                              c.paragraph_number, c.chunk_text,
                              (1 - (c.embedding <=> %s::vector))::float AS dense_score
                       FROM chunks c JOIN documents d ON d.id=c.document_id
                       WHERE d.is_active=TRUE AND c.embedding IS NOT NULL
                       ORDER BY c.embedding <=> %s::vector LIMIT %s""",
                    (vector_literal, vector_literal, limit),
                )
                dense_rows = [dict(r) for r in cur.fetchall()]
            cur.execute(
                """SELECT c.id AS chunk_id, d.document_name, d.version, c.page_number,
                          c.paragraph_number, c.chunk_text,
                          ts_rank_cd(c.search_vector, plainto_tsquery('simple', %s))::float AS lexical_score
                   FROM chunks c JOIN documents d ON d.id=c.document_id
                   WHERE d.is_active=TRUE AND c.search_vector @@ plainto_tsquery('simple', %s)
                   ORDER BY lexical_score DESC LIMIT %s""",
                (question, question, limit),
            )
            lexical_rows = [dict(r) for r in cur.fetchall()]

    # Reciprocal Rank Fusion avoids combining incompatible raw score scales.
    fused: dict[int, dict[str, Any]] = {}
    for rank, row in enumerate(dense_rows, start=1):
        item = fused.setdefault(row["chunk_id"], row.copy())
        item["dense_rank"] = rank
        item["hybrid_score"] = item.get("hybrid_score", 0.0) + 1.0 / (60 + rank)
    for rank, row in enumerate(lexical_rows, start=1):
        item = fused.setdefault(row["chunk_id"], row.copy())
        item["lexical_score"] = row.get("lexical_score", 0.0)
        item["lexical_rank"] = rank
        item["hybrid_score"] = item.get("hybrid_score", 0.0) + 1.0 / (60 + rank)
    ordered = sorted(fused.values(), key=lambda x: x.get("hybrid_score", 0.0), reverse=True)[:limit]

    # Cross-Encoder is optional because it requires downloading a separate model.
    reranker_name = os.getenv("RERANKER_MODEL", "").strip()
    if reranker_name and ordered:
        try:
            from sentence_transformers import CrossEncoder
            model = CrossEncoder(reranker_name)
            pairs = [(question, row["chunk_text"]) for row in ordered]
            scores = model.predict(pairs)
            for row, score in zip(ordered, scores):
                row["rerank_score"] = float(score)
            ordered.sort(key=lambda x: x.get("rerank_score", float("-inf")), reverse=True)
        except Exception as exc:
            raise RuntimeError(f"No se pudo inicializar el reranker configurado: {exc}") from exc

    return [RetrievedChunk(
        chunk_id=row["chunk_id"], document_name=row["document_name"], version=row.get("version"),
        page_number=row.get("page_number"), paragraph_number=row.get("paragraph_number"),
        chunk_text=row["chunk_text"], dense_score=float(row.get("dense_score") or 0.0),
        lexical_score=float(row.get("lexical_score") or 0.0), hybrid_score=float(row.get("hybrid_score") or 0.0),
        rerank_score=row.get("rerank_score")
    ) for row in ordered[:5]]


def answer_question(question: str) -> dict[str, Any]:
    start = time.perf_counter()
    chunks = _retrieve(question)
    min_dense = float(os.getenv("MIN_RETRIEVAL_SCORE", "0.35"))
    # If dense retrieval is unavailable, lexical matches can still ground an answer.
    # When dense scores exist, preserve the normal minimum-score abstention threshold.
    has_dense_scores = any(c.dense_score > 0 for c in chunks)
    weak_dense = has_dense_scores and max(c.dense_score for c in chunks) < min_dense
    no_lexical_evidence = not chunks or max((c.lexical_score for c in chunks), default=0.0) <= 0
    if not chunks or weak_dense or (not has_dense_scores and no_lexical_evidence):
        result = {
            "status": "abstained", "answer": "No encontré evidencia documental suficiente para responder con seguridad.",
            "citations": [], "abstained": True,
            "message": "Verifica la consulta o escala el caso según el procedimiento vigente.",
        }
    else:
        context = "\n\n".join(
            f"[Fuente: {c.document_name}; versión: {c.version or 'no indicada'}; página: {c.page_number or 'no indicada'}; párrafo: {c.paragraph_number or 'no indicado'}]\n{c.chunk_text}"
            for c in chunks
        )
        client = _gemini_client()
        model = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
        system_instruction = (
            "Eres un asistente técnico de consulta documental. Responde en español usando exclusivamente el contexto. "
            "No inventes códigos, procedimientos, versiones, páginas ni párrafos. Añade una cita [documento, página, párrafo] "
            "a cada afirmación técnica. Si el contexto no contiene evidencia suficiente o hay contradicción, indícalo y abstente."
        )
        response = _provider_call(client.models.generate_content,
            model=model,
            contents=f"Consulta: {question}\n\nContexto recuperado:\n{context}",
            config={"temperature": 0, "system_instruction": system_instruction},
        )
        answer = (getattr(response, "text", None) or "").strip()
        if not answer:
            answer = "No se pudo generar una respuesta verificable con el contexto recuperado."
        result = {
            "status": "answered", "answer": answer,
            "citations": [c.citation() for c in chunks], "abstained": False,
            "message": "Verifica las fuentes citadas antes de aplicar instrucciones al incidente.",
        }
    result["latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
    _log_query(question, result)
    return result


def _log_query(question: str, result: dict[str, Any]) -> None:
    try:
        with _db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO query_logs(question, answer, abstained, latency_ms) VALUES (%s, %s, %s, %s)",
                    (question, result.get("answer"), result.get("abstained", True), result.get("latency_ms")),
                )
    except Exception:
        # A logging outage must not turn an otherwise safe answer into a fabricated failure.
        pass
