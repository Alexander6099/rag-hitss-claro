# Configuración de Gemini

## 1. Variables de entorno

En el archivo `.env` de la raíz, conserva las variables de PostgreSQL y `API_ACCESS_TOKEN`. Añade estas variables (no compartas la clave):

```dotenv
GEMINI_API_KEY=PEGA_AQUI_TU_CLAVE_PRIVADA
GEMINI_CHAT_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=1536
```

La dimensión 1536 debe mantenerse mientras `database/init.sql` declare `embedding VECTOR(1536)`.

## 2. Reconstruir el backend

Desde PowerShell, en la carpeta del proyecto:

```powershell
docker compose up -d --build
```

Comprueba `http://127.0.0.1:8000/health` y espera `{"status":"healthy","service":"rag-api"}`. Esto solo comprueba que la API está activa, no que la clave o los modelos estén funcionando.

## 3. Importante sobre documentos ya cargados

Los vectores de OpenAI y Gemini no son intercambiables aunque ambos tengan dimensión 1536. Los documentos indexados con OpenAI deben volver a indexarse con Gemini antes de realizar búsquedas fiables.

Antes de borrar o reemplazar datos, haz una copia de seguridad si necesitas conservar el corpus. Para limpiar el corpus de prueba existente y volver a cargar los PDF con Gemini, abre PowerShell en la raíz y ejecuta:

```powershell
docker compose exec db psql -U $env:POSTGRES_USER -d $env:POSTGRES_DB -c "TRUNCATE TABLE documents RESTART IDENTITY CASCADE;"
```

Si PowerShell no tiene `POSTGRES_USER`/`POSTGRES_DB` como variables de sesión, usa los valores de esas variables que figuran en tu `.env` (no la contraseña). Este comando elimina los documentos indexados y sus fragmentos; no lo ejecutes si necesitas conservarlos sin una copia de seguridad.

Después, abre la web, introduce tu `API_ACCESS_TOKEN` y vuelve a cargar los PDF autorizados. No cargues manuales internos sin permiso de uso.

## 4. Límites del nivel gratuito

Gemini API depende de los límites vigentes del proyecto y del modelo en Google AI Studio. Una clave válida no garantiza disponibilidad ilimitada ni que todos los modelos estén incluidos en el nivel gratuito. Si Google devuelve un error de cuota, revisa la cuota y disponibilidad de tu proyecto en AI Studio.

## Recuperación ante límites de cuota de embeddings

La consulta intenta primero recuperar fragmentos por similitud vectorial. Si Gemini rechaza únicamente la generación del embedding de la pregunta (por ejemplo, con `429 RESOURCE_EXHAUSTED`), el backend registra una advertencia y usa la búsqueda léxica de PostgreSQL como alternativa. Si encuentra evidencia léxica, puede continuar con la generación de respuesta; la generación de texto sigue dependiendo de la cuota y configuración del modelo `GEMINI_CHAT_MODEL`.

Los errores de consulta no muestran detalles internos al navegador. La excepción completa se registra en los logs del backend para diagnóstico. Para verlos, ejecutar `docker compose logs --since=10m backend`.

Si aparece `401 Unauthorized`, revisa que el campo “Token de acceso” de la interfaz coincida exactamente con `API_ACCESS_TOKEN` en tu archivo `.env`. No compartas ese token ni la clave `GEMINI_API_KEY`.
