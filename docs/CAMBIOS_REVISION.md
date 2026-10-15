# Cambios de la revisión del prototipo

## Cambios técnicos
- Se sustituyó la respuesta fija de “no implementado” por un flujo inicial de ingesta PDF, embeddings, recuperación densa y léxica, fusión RRF y generación condicionada al contexto.
- Se agregó una interfaz web mínima para consultas e ingesta.
- Se agregó protección configurable por token Bearer para la ingesta; no reemplaza autenticación corporativa con JWT/SSO/roles.
- Se agregó un índice vectorial HNSW y un índice GIN para la búsqueda léxica en PostgreSQL.
- Se agregó abstención por umbral configurable, registro básico de consulta y medición de latencia.
- Se agregó un script para calcular métricas de comparación y análisis de sensibilidad desde registros reales, sin rellenar valores ausentes.
- Se actualizaron Docker Compose, variables de entorno, README y estado de implementación.
- Se agregaron pruebas unitarias para validaciones y funciones auxiliares.

## Verificación ejecutada
- `python -m pytest -q`: 10 pruebas pasan en el entorno de revisión.
- `python tests/poc_gold_standard.py`: valida la estructura de los tres ejemplos; explícitamente no ejecuta RAG ni calcula métricas.
- `py_compile`: compilación sintáctica de los módulos principales.

## Lo que no se afirma
- No se probó la conexión a una base PostgreSQL real en este entorno.
- No se ejecutaron llamadas reales al proveedor LLM/embeddings porque dependen de credenciales y configuración externas.
- No se midió la calidad sobre manuales autorizados ni se compararon experimentalmente A, B y C.
- No se implementaron OCR, jerarquía padre-hijo, JWT/SSO/roles completos, auditoría inmutable ni medición del TMR.
