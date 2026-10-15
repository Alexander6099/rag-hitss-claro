CREATE EXTENSION IF NOT EXISTS vector;
<<<<<<< HEAD

=======
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
CREATE TABLE IF NOT EXISTS documents (
  id BIGSERIAL PRIMARY KEY,
  document_name TEXT NOT NULL,
  version TEXT,
  source_uri TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
<<<<<<< HEAD

=======
-- Confirmar la dimensión del modelo de embeddings antes de almacenar vectores.
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
CREATE TABLE IF NOT EXISTS chunks (
  id BIGSERIAL PRIMARY KEY,
  document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  page_number INTEGER,
  paragraph_number INTEGER,
  chunk_text TEXT NOT NULL,
  embedding VECTOR(1536),
<<<<<<< HEAD
  search_vector TSVECTOR GENERATED ALWAYS AS (to_tsvector('simple', coalesce(chunk_text, ''))) STORED,
=======
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_documents_active ON documents(is_active);
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);
<<<<<<< HEAD
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_chunks_search_vector ON chunks USING gin(search_vector);

=======
>>>>>>> 0135657e4a1604629e0c75ae104686f4497fde13
CREATE TABLE IF NOT EXISTS query_logs (
  id BIGSERIAL PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT,
  abstained BOOLEAN NOT NULL DEFAULT FALSE,
  latency_ms DOUBLE PRECISION,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
