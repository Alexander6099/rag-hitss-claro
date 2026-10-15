# Sistema web de asistencia inteligente basado en RAG

**Prototipo académico para la consulta de documentación técnica — Global Hitss Perú / Cuenta Claro**

## 1. Descripción del proyecto

Este repositorio contiene un prototipo de asistente inteligente basado en generación aumentada por recuperación (Retrieval-Augmented Generation, RAG), orientado a facilitar la consulta de información contenida en documentos técnicos PDF.

El sistema permite incorporar documentos, extraer y segmentar su contenido, almacenarlo en una base de datos y recuperar fragmentos relevantes para responder consultas formuladas en lenguaje natural.

Las respuestas se generan mediante Google Gemini utilizando el contexto recuperado e incluyen referencias documentales que facilitan la identificación de las fuentes consultadas.

El proyecto se desarrolla con fines académicos y corresponde a un prototipo funcional, no a una plataforma corporativa desplegada en producción.

## 2. Objetivo

Desarrollar un prototipo de sistema web basado en RAG que facilite la búsqueda y recuperación de información técnica mediante consultas en lenguaje natural, integrando procesamiento documental, recuperación híbrida y generación de respuestas contextualizadas.

## 3. Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje de programación | Python |
| Backend | FastAPI |
| Interfaz | HTML y JavaScript |
| Base de datos | PostgreSQL 16 |
| Búsqueda vectorial | pgvector |
| Modelo de inteligencia artificial | Google Gemini |
| Procesamiento de PDF | pypdf |
| Contenedores | Docker y Docker Compose |
| Pruebas de software | pytest |

## 4. Arquitectura del sistema

El prototipo utiliza una arquitectura compuesta por las siguientes capas:

1. **Interfaz web:** permite incorporar documentos y realizar consultas.
2. **API REST:** recibe solicitudes, valida entradas y coordina las operaciones del sistema.
3. **Procesamiento documental:** extrae el texto de archivos PDF y lo divide en fragmentos.
4. **Almacenamiento:** registra documentos, fragmentos y consultas en PostgreSQL.
5. **Recuperación híbrida:** combina búsqueda vectorial y búsqueda de texto completo.
6. **Generación de respuestas:** utiliza Google Gemini para elaborar respuestas basadas en los fragmentos recuperados.

La recuperación híbrida combina resultados mediante Reciprocal Rank Fusion (RRF). El sistema contempla la posibilidad de incorporar un reranker Cross-Encoder mediante configuración adicional.

## 5. Funcionalidades implementadas

- Incorporación de documentos PDF.
- Extracción y segmentación de texto.
- Generación de embeddings.
- Almacenamiento de fragmentos en PostgreSQL con pgvector.
- Recuperación de información mediante búsqueda híbrida.
- Consultas en lenguaje natural.
- Generación de respuestas con Google Gemini.
- Presentación de referencias documentales.
- Registro básico de consultas.
- Manejo de errores relacionados con el servicio de generación.

## 6. Estructura principal del repositorio

```text
rag-hitss-claro/
├── backend/
│   └── app/
│       ├── main.py
│       └── services/
│           └── rag.py
├── database/
│   └── init.sql
├── docs/
├── scripts/
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 7. Requisitos previos

Para ejecutar el proyecto se requiere:

- Docker y Docker Compose.
- Acceso a Internet.
- Una clave de API válida de Google Gemini.
- Un archivo de configuración de variables de entorno.

## 8. Instalación y ejecución

### Paso 1. Obtener el repositorio

```bash
git clone https://github.com/Alexander6099/rag-hitss-claro.git
cd rag-hitss-claro
```

### Paso 2. Configurar las variables de entorno

Crear el archivo `.env` tomando como referencia `.env.example`.

Configurar las variables necesarias, especialmente:

```env
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=CAMBIAR_POR_UNA_CONTRASENA_SEGURA
POSTGRES_DB=rag_db
GEMINI_API_KEY=COLOCAR_CLAVE_PERSONAL
API_ACCESS_TOKEN=COLOCAR_TOKEN_SEGURO
```

Los valores anteriores son ejemplos de configuración. No deben utilizarse como credenciales reales ni publicarse claves privadas en GitHub.

### Paso 3. Iniciar los servicios

```bash
docker compose up --build
```

### Paso 4. Acceder a la aplicación

Interfaz web:

http://127.0.0.1:8000

Documentación interactiva de la API:

http://127.0.0.1:8000/docs

## 9. Funcionamiento del sistema

El proceso general de consulta comprende las siguientes etapas:

1. El usuario incorpora un documento PDF.
2. El sistema extrae y segmenta el contenido.
3. Se generan representaciones vectoriales de los fragmentos.
4. Los fragmentos y sus metadatos se almacenan en PostgreSQL.
5. El usuario formula una pregunta.
6. El sistema recupera fragmentos mediante búsqueda híbrida.
7. Google Gemini genera una respuesta utilizando el contexto recuperado.
8. La interfaz presenta la respuesta y sus referencias documentales.

## 10. Pruebas y validación

El proyecto contempla pruebas de software mediante pytest.

Para ejecutar las pruebas configuradas en el repositorio:

```bash
pytest -q
```

Durante la verificación funcional del prototipo se han documentado escenarios de incorporación de archivos PDF, recuperación de información con referencias y manejo de incidencias del proveedor de inteligencia artificial.

Estas verificaciones permiten examinar las funcionalidades centrales del prototipo. No representan, por sí solas, una evaluación experimental completa de precisión, rendimiento bajo carga o comparación entre arquitecturas RAG.

## 11. Documentación utilizada

La implementación permite procesar documentos PDF de contenido técnico estructurado para verificar las operaciones de extracción, segmentación, indexación y recuperación de información.

La incorporación de documentación debe respetar las condiciones de acceso y uso de cada fuente. El repositorio no requiere publicar documentación interna de las organizaciones mencionadas en el contexto académico del
