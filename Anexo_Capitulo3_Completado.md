# RNF, Historias de Usuario y Criterios de Aceptacion (Capitulo 3)

## 3.5.4 Requisitos No Funcionales (ISO/IEC 25010)
- RNF01 (Latencia): P95 de tiempo de respuesta <= 5,000 ms.
- RNF02 (Concurrencia): Soporte de >= 20 usuarios concurrentes.
- RNF03 (Disponibilidad): Uptime >= 99.5% en horario 24x7.
- RNF04 (Cero Alucinacion): Abstencion 100% cuando s* < tau_min.
- RNF05 (Seguridad): Cifrado TLS 1.2+ y tokens JWT.

## 3.6 Historias de Usuario
- HU01: Como analista N1, quiero consultar en lenguaje natural para reducir el TMR.
- HU02: Como analista N1, quiero ver la cita exacta para verificar la fuente.
- HU03: Como analista N1, quiero alerta de informacion insuficiente para escalar a N2.

## 3.6.3 Definition of Done (DoD)
1. Codigo integrado en Git con commits semanticos.
2. Cobertura de pruebas >= 80%.
3. Escenarios Gherkin validados.
4. RNF01 verificado (P95 <= 5,000 ms).
