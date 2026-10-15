# Plan de evidencias pendientes para el Capítulo III

Este archivo distingue artefactos de diseño de evidencia de campo o experimental. No debe usarse como sustituto de la aplicación real de los instrumentos.

## Observación 3: justificación de pesos
1. Mantener los pesos definidos antes de la evaluación (30 %, 25 %, 20 %, 15 %, 10 %).
2. Documentar que son una decisión metodológica, no una exigencia atribuida al cliente sin evidencia.
3. Si un referente del proceso valida prioridades, guardar fecha, rol del participante, preguntas y respuestas autorizadas.

## Observación 4: matriz empírica
1. Obtener permiso para usar un corpus técnico; registrar inventario, versión y hash de cada documento.
2. Crear y validar al menos 50 consultas representativas con respuestas de referencia y fuente exacta.
3. Ejecutar A, B y C con corpus, consultas, modelo generador y embeddings iguales; registrar configuración, versiones, entorno y logs.
4. Repetir mediciones de latencia y registrar costo real por consulta.
5. Ejecutar `python scripts/evaluar_matriz.py ruta/mediciones_candidatos.json`.
6. No completar celdas N/D con estimaciones, ejemplos o valores de otro sistema.

## Observaciones 6 y 7: metodología y levantamiento
1. Aplicar entrevistas E-01/E-02 solo con autorización y consentimiento cuando corresponda.
2. Registrar la observación del proceso manual con definición clara del inicio y fin del tiempo medido.
3. Completar inventario documental con nombre, versión, fecha, página, estado y autorización de uso.
4. Adjuntar los instrumentos diligenciados y codificar participantes sin exponer datos personales o confidenciales.
5. Si no se puede acceder a usuarios o manuales, declarar la limitación y no afirmar que el levantamiento fue realizado.

## Precaución
Los documentos internos, tickets, datos personales, claves API y manuales restringidos no deben subirse a un repositorio público. Para pruebas académicas públicas, usar documentos de libre acceso o datos sintéticos claramente identificados como tales; estos no sustituyen la validación del caso real.
