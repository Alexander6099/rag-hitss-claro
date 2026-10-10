from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

class Citation(BaseModel):
    document: str
    page: int | None = None
    paragraph: int | None = None

class QueryResponse(BaseModel):
    status: str
    answer: str
    citations: list[Citation] = []
    abstained: bool = True
    message: str
