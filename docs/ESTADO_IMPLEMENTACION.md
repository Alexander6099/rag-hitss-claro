# Estado de implementación y límites de evidencia

<<<<<<< HEAD
Revisión del repositorio: 15-10-2026.

## Implementado en el prototipo
- API FastAPI y una interfaz web mínima para consultar y cargar PDF.
- Validación de consultas y respuesta HTTP controlada ante errores de configuración.
- Ingesta de PDF con extracción de texto por página; conserva nombre, versión, página y número aproximado de fragmento.
- Generación de embeddings mediante API de OpenAI y almacenamiento en PostgreSQL + pgvector.
- Recuperación densa por similitud de coseno y recuperación léxica mediante PostgreSQL Full Text Search; fusión de rankings RRF.
- Generación de respuesta condicionada al contexto recuperado y abstención si la mayor similitud densa no supera el umbral configurable.
- Registro básico de pregunta, respuesta, abstención y latencia.
- Pruebas automatizadas de API y funciones auxiliares.
- Script para resumir mediciones y script para calcular la matriz comparativa desde datos medidos.

## Parcial, opcional o pendiente
- Cross-Encoder: opcional; requiere instalar `requirements-reranker.txt`, configurar `RERANKER_MODEL` y validar el modelo en español técnico.
- Autenticación: token Bearer configurable para el prototipo; no implementa JWT corporativo, SSO ni separación completa de roles.
- OCR para PDF escaneados: pendiente.
- Chunking jerárquico padre-hijo y tratamiento atómico de tablas: pendiente.
- Umbrales de abstención calibrados sobre un Gold Standard: pendiente; el umbral actual es configurable y provisional.
- Auditoría inmutable que registre usuario, fragmentos recuperados, citas y decisión: pendiente; el registro actual es básico.
- Feedback del analista, vínculo con ticket y medición del TMR: pendiente.
- Frontend de administración avanzado y controles de acceso productivos: pendiente.
- Comparación ejecutada de los candidatos A/B/C: pendiente.

## Evidencia que no existe todavía
- No se ha incorporado un corpus operativo autorizado de Global Hitss/Claro.
- Las preguntas y fuentes de ejemplo del archivo `tests/gold_standard_queries.json` están marcadas como pendientes de verificación; no son un Gold Standard válido.
- No hay resultados experimentales acreditados de F1, Context Recall, exactitud de citas, latencia P95, costo por 1.000 consultas ni TMR.
- No se han aportado entrevistas diligenciadas, observaciones cronometradas ni inventario real del corpus.

## Consecuencia para la tesis
Describir el repositorio como **prototipo académico en desarrollo**, no como sistema productivo. El hecho de que pasen las pruebas automatizadas no demuestra que el RAG sea preciso ni que el candidato B haya ganado la comparación. Incorporar resultados únicamente después de ejecutar pruebas reproducibles con documentos autorizados, consultas etiquetadas, configuraciones registradas y procedencia verificable.
=======
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
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
