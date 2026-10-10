# Sistema web de asistencia inteligente basado en RAG — Global Hitss Perú (cuenta Claro)

**Estado actual: prototipo de estructura técnica; pipeline RAG completo todavía no integrado.**

Este repositorio contiene una API inicial, esquema de base de datos, banco de preguntas de ejemplo, validación estructural y utilidades para resumir mediciones reales. No prueba que Advanced RAG haya sido evaluado.

## Arquitectura prevista
- API: Python 3.11 + FastAPI.
- Framework RAG: LangChain, pendiente de integración.
- Embeddings previstos: `text-embedding-3-small`, dimensión declarada 1536; confirmar la dimensión real.
- Almacenamiento previsto: PostgreSQL 16 + pgvector.
- Reranker: Cross-Encoder multilingüe, pendiente de selección/integración y evaluación.
- Modelo generativo previsto: GPT-4o-mini mediante API; requiere credenciales y revisión de seguridad.
- Pruebas: pytest. Playwright no está configurado.
- Banco: `tests/gold_standard_queries.json`, solo tres ejemplos iniciales; fuentes pendientes de verificación.

## Ejecución local
1. Instalar Python 3.11.
2. Crear entorno: `py -3.11 -m venv .venv`
3. Activar en Windows: `.venv\\Scripts\\activate`
4. Instalar: `pip install -r requirements.txt`
5. Ejecutar API: `uvicorn backend.app.main:app --reload`
6. Abrir `http://127.0.0.1:8000/docs`.

`/health` verifica la API. `/api/v1/query` se abstiene porque aún no existe recuperación ni generación integradas.

## Pruebas
- `pytest -q`
- `python tests/poc_gold_standard.py`

El segundo comando valida la estructura del banco; no ejecuta RAG ni calcula métricas.

## Resumen de mediciones
Cuando existan observaciones reales, preparar un JSON siguiendo `docs/mediciones_reales_ejemplo.json` y ejecutar:
`python scripts/calcular_metricas.py ruta/al/archivo.json`

No presentar datos ilustrativos como resultados reales. Registrar corpus, versión del código, hardware, configuración, consultas, evaluadores y procedimiento.

## Evidencia académica
Consultar `docs/ESTADO_IMPLEMENTACION.md`. Los umbrales RNF son objetivos propuestos hasta que se verifiquen. Los nombres de PDF del banco son ejemplos: comprobar que las fuentes existen y que sustentan las respuestas antes de usarlas como gold standard.
