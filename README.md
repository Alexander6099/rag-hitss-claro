# Sistema Web RAG de Asistencia Inteligente - Global Hitss Peru (Cuenta Claro)

Prototipo del Sistema Web de Asistencia Inteligente basado en una Arquitectura Advanced RAG para la consulta automatizada de normativas tecnicas en la mesa de ayuda de Global Hitss Peru.

## Arquitectura Tecnologica
- Backend / Orquestador RAG: Python 3.11, FastAPI, LangChain 0.2
- Embeddings: OpenAI text-embedding-3-small (Dimension d = 1,536)
- Base de Datos Vectorial: PostgreSQL 16 + pgvector 0.7
- Reranker: Cross-Encoder multilingue (bge-reranker-v2-m3)
- LLM Generador: GPT-4o-mini
- Testing: Playwright (E2E), PoC Gold Standard (50 queries)

## Ejecucion
python tests/poc_gold_standard.py
