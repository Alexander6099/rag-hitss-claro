from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

    @field_validator("question")
    @classmethod
    def normalize_question(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("La consulta debe contener al menos 3 caracteres no vacíos.")
        return value

class Citation(BaseModel):
    document: str
    version: str | None = None
    page: int | None = None
    paragraph: int | None = None

class QueryResponse(BaseModel):
    status: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    abstained: bool = True
    message: str
    latency_ms: float | None = None
