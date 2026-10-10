# Estado de implementación y límites de evidencia

Fecha de revisión: 2026-10-09.

## Incluido en esta estructura
- API FastAPI de salud.
- Endpoint de consulta que se abstiene porque no hay pipeline RAG.
- Esquema SQL inicial para documentos, chunks, vectores y logs.
- Configuración por variables de entorno.
- Validación estructural del banco de preguntas.
- Pruebas automatizadas básicas.
- Script para resumir métricas desde mediciones proporcionadas.

## No implementado o no verificado
- Ingesta real de PDF y extracción de página/párrafo.
- Embeddings y almacenamiento vectorial reales.
- Recuperación híbrida léxica/vectorial.
- Reranking con Cross-Encoder.
- Integración real con un LLM.
- Calibración de umbrales con un gold standard validado.
- Login, roles, JWT, auditoría de seguridad y despliegue productivo.
- Experimento con analistas, comparación contra búsqueda manual y medición de TMR.
- Existencia y exactitud de los PDF citados en el banco.
- Resultados empíricos de F1, Context Recall, citas, latencia o coste.

## Consecuencia para la tesis y el artículo
Describir el repositorio como **prototipo en desarrollo / esqueleto técnico** hasta integrar el pipeline. No afirmar que Advanced RAG fue implementado o evaluado en producción. Incorporar resultados solo tras ejecutar pruebas con documentos autorizados, consultas etiquetadas y protocolo documentado.
