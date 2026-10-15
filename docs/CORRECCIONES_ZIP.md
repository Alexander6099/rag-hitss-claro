# Correcciones realizadas sobre el ZIP recibido

- Se resolvieron los conflictos de fusión conservando la versión funcional (HEAD) en ocho archivos.
- Se eliminaron las referencias incorrectas a OpenAI en la documentación funcional.
- Se retiró `scripts/docker-compose.yml` por ser un Compose duplicado con ruta relativa incorrecta; usar el de la raíz.
- No se inventaron resultados experimentales, credenciales ni pruebas de integración.
- Las pruebas automatizadas usan mocks en varios escenarios: no equivalen a una ejecución real con PostgreSQL y Gemini.
- Para verificar el despliegue real, configurar `.env`, ejecutar `docker compose config` y `docker compose up --build`.
