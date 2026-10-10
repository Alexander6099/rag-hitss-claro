# Anexo de apoyo al Capítulo III: RNF, historias de usuario y aceptación

> Los umbrales son objetivos de diseño propuestos, no resultados medidos. Deben justificarse y comprobarse con un protocolo reproducible.

## Requisitos no funcionales propuestos

| ID | Característica | Criterio propuesto | Evidencia necesaria |
|---|---|---|---|
| RNF01 | Rendimiento | P95 ≤ 5 000 ms bajo carga definida | Mediciones reales, entorno y tamaño de muestra |
| RNF02 | Capacidad | Objetivo inicial de 20 usuarios concurrentes | Prueba de carga reproducible |
| RNF03 | Disponibilidad | Objetivo de 99,5 % en periodo definido | Monitoreo durante periodo acordado |
| RNF04 | Respuesta sustentada | Abstenerse si la evidencia no supera el umbral calibrado | Casos positivos/negativos y evaluación |
| RNF05 | Seguridad | HTTPS/TLS en despliegue, secretos fuera del código y control de acceso | Configuración y pruebas de seguridad |

Evitar prometer “cero alucinaciones”: es un objetivo de reducción de respuestas no sustentadas, no una garantía absoluta.

## Historias de usuario propuestas

- **HU01:** Como analista N1, quiero consultar una pregunta técnica en lenguaje natural para localizar más rápido información aplicable al incidente.
- **HU02:** Como analista N1, quiero visualizar la fuente documental y su ubicación para verificar la respuesta.
- **HU03:** Como analista N1, quiero que el sistema indique cuándo no encuentra evidencia suficiente para evitar usar una respuesta no sustentada y poder escalar el caso.

## Criterio BDD de ejemplo — HU02

- **Dado** que el corpus contiene un documento vigente con página y párrafo registrados,
- **cuando** el sistema responde utilizando un fragmento de ese documento,
- **entonces** presenta el nombre de la fuente y la ubicación recuperada.
- **Alternativo:** si no hay página o párrafo, muestra solo los metadatos existentes; nunca inventa una ubicación.

## Definition of Done propuesto

1. Código revisado y versionado.
2. Pruebas automatizadas ejecutadas y resultado guardado.
3. Escenarios BDD críticos documentados.
4. Requisitos no funcionales evaluados mediante protocolo definido.
5. Ningún umbral se declara cumplido sin evidencia reproducible.
