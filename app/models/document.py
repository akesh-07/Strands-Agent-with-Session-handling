from pydantic import BaseModel

class ChunkMetadata(BaseModel):
    filename: str
    page_number: int
    chunk_id: str

class Chunk(BaseModel):
    text: str
    metadata: ChunkMetadata
