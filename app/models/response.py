from pydantic import BaseModel
from typing import List

class AnswerResponse(BaseModel):
    answer: str

class IngestResponse(BaseModel):
    number_of_pdfs: int
    chunks_created: int
    indexing_duration_seconds: float

class HealthResponse(BaseModel):
    status: str
    bedrock: str
    faiss: str
