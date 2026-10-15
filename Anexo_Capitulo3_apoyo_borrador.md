# Anexo de apoyo al Capítulo III (borrador, no evidencia de validación)

Los criterios que siguen son propuestas de aceptación. No demuestran que se hayan alcanzado. El estado real del prototipo se describe en `docs/ESTADO_IMPLEMENTACION.md`.

## Requisitos no funcionales propuestos

| ID | Característica | Criterio propuesto | Evidencia necesaria |
|---|---|---|---|
| RNF01 | Rendimiento | P95 ≤ 5 000 ms bajo carga y entorno definidos | Mediciones reales y configuración reproducible |
| RNF02 | Capacidad | Objetivo inicial de 20 usuarios concurrentes | Prueba de carga reproducible |
| RNF03 | Disponibilidad | Objetivo de 99 % durante periodo definido | Monitoreo y registro de errores |
| RNF04 | Respuesta sustentada | Abstenerse si la evidencia no supera umbral calibrado | Gold Standard, casos negativos y revisión de citas |
| RNF05 | Seguridad | Secretos fuera del código y control de acceso adecuado al entorno | Pruebas de acceso y revisión de configuración |

No prometer “cero alucinaciones”. El objetivo es reducir respuestas no sustentadas y facilitar la verificación.

## Historias de usuario
- **HU01:** Como analista de Help Desk, quiero enviar una consulta técnica en lenguaje natural para localizar información aplicable al incidente.
- **HU02:** Como analista de Help Desk, quiero recibir una respuesta con fuente y ubicación para poder verificarla.
- **HU03:** Como analista de Help Desk, quiero que el sistema indique incertidumbre o se abstenga cuando no encuentre evidencia suficiente.
- **HU07:** Como usuario autorizado, quiero iniciar sesión con el rol que me corresponde para acceder solo a las funciones permitidas. Esta historia es requisito de diseño; el prototipo actual no implementa aún login JWT/roles corporativos.

## Criterio BDD de ejemplo — HU02
- **Dado** que el corpus autorizado contiene un fragmento con documento, página y párrafo registrados,
- **cuando** el sistema responde utilizando ese fragmento,
- **entonces** muestra los metadatos que realmente recuperó.
- **Alternativo:** si un metadato no existe, no inventa su valor.

## Definition of Done propuesto
1. Código versionado y configuración reproducible.
2. Pruebas automatizadas ejecutadas con resultado registrado.
3. Escenarios BDD críticos documentados.
4. RNF evaluados mediante protocolo definido.
5. Ningún umbral se declara cumplido sin evidencia reproducible.
