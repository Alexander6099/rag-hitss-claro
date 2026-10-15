# Sistema web de asistencia inteligente basado en RAG — prototipo académico

API web para consultar documentos PDF autorizados mediante recuperación densa con pgvector, recuperación léxica de PostgreSQL y fusión Reciprocal Rank Fusion. Se puede activar un Cross-Encoder mediante `RERANKER_MODEL`. Las respuestas generadas usan el contexto recuperado y muestran metadatos de las fuentes; el sistema se abstiene cuando la señal densa está por debajo del umbral configurado.

**Límite importante:** este repositorio no contiene manuales operativos de Claro/Global Hitss ni un Gold Standard validado. No se deben presentar las preguntas de ejemplo como datos reales ni afirmar que se han medido F1, Context Recall, TMR, precisión de citas o latencia bajo carga. La implementación del pipeline tampoco equivale a una evaluación empírica de los candidatos A, B y C.

## Componentes
- FastAPI y una interfaz web mínima en `/`.
- PostgreSQL 16 + pgvector (HNSW) y búsqueda léxica con `tsvector`/GIN.
- Embeddings y generación con Google Gemini API (requiere conexión a Internet y una clave válida).
- Fusión de rankings; Cross-Encoder opcional configurado por variable de entorno.
- Ingesta de PDF con metadatos de documento, versión, página y fragmento.
- Registro básico de consultas y pruebas automatizadas.

## Inicio con Docker
1. Copiar `.env.example` a `.env`.
2. Configurar `POSTGRES_PASSWORD` con una contraseña segura y `GEMINI_API_KEY` con una clave válida de Google AI Studio.
3. Definir `API_ACCESS_TOKEN` con un secreto aleatorio para habilitar la carga de documentos.
4. Ejecutar `docker compose up --build`.
5. Abrir `http://127.0.0.1:8000` o la documentación en `http://127.0.0.1:8000/docs`.
6. Cargar solo PDF cuyo uso esté autorizado. Los PDF escaneados requieren OCR, todavía no incluido.

La configuración predeterminada usa `gemini-embedding-001` con `EMBEDDING_DIMENSIONS=1536`, compatible con `VECTOR(1536)` del esquema SQL. Si cambias la dimensión, también debes migrar el esquema de PostgreSQL y volver a indexar todos los documentos con los mismos embeddings. Para iniciar localmente: instalar dependencias, configurar variables de entorno, ejecutar `database/init.sql` en PostgreSQL con pgvector y lanzar `uvicorn backend.app.main:app --reload`.

## Pruebas
`pytest -q`

Las pruebas actuales validan la API y la protección básica de carga; no llaman a Gemini ni a una base de datos real. Para evaluar recuperación y generación hacen falta un corpus autorizado, consultas verificadas, respuestas de referencia, configuración registrada y ejecuciones repetibles.

## Seguridad y limitaciones
- Cada petición a Gemini tiene un timeout de 20 segundos; los timeouts también se reintentan. La recuperación y la generación son operaciones separadas, por lo que una consulta completa puede tardar más que una petición individual.
- Si Gemini devuelve 429 o un error transitorio 500/502/503/504, se realizan hasta tres intentos por operación, con pausas de uno y dos segundos. Si persiste, la API devuelve 503 con un mensaje de disponibilidad/cuota y `Retry-After: 30`. Una consulta fallida no elimina los PDF ya cargados; no hace falta volver a subirlos.
- No subir `.env`, claves, tokens ni documentos internos al repositorio.
- El token de acceso es una protección básica de prototipo, no sustituye SSO/JWT corporativo, gestión de roles ni una auditoría de seguridad.
- No hay OCR, interfaz de administración avanzada, control corporativo de roles, aislamiento multiusuario ni despliegue productivo.
- El umbral de recuperación es configurable y no está calibrado. Las citas enumeran fuentes recuperadas; la verificación humana de que cada afirmación está respaldada sigue siendo necesaria.
- Si `RERANKER_MODEL` está vacío, el sistema no ejecuta Cross-Encoder; usa la fusión de rankings híbridos.

## Matriz comparativa de candidatos
Cuando existan datos reales para A, B y C, registra un JSON por consulta con `candidate`, `query_id`, `answer_f1`, `context_recall`, `latency_ms` (lista con repeticiones), `citation_correct` y `cost_usd`. Luego ejecuta:

`python scripts/evaluar_matriz.py ruta/mediciones_candidatos.json`

El script exige al menos 50 consultas únicas por candidato y rechaza datos faltantes; no inventa puntuaciones. C3 es una valoración teórica predefinida (A=5, B=4, C=3) y debe explicarse como tal. La comparación solo es válida si las consultas, el corpus, los modelos y el entorno son comparables.

Para activar el Cross-Encoder fuera del contenedor base, instala `pip install -r requirements-reranker.txt` y configura `RERANKER_MODEL` con un identificador de modelo compatible. La selección del modelo y su calidad para español técnico deben evaluarse antes de reportar resultados.
