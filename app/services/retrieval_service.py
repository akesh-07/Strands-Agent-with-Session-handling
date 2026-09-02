from typing import List
from app.core.logging import logger
from app.providers.bedrock.embeddings import BedrockEmbeddings
from app.core.config import settings
from app.vectorstore.faiss_store import FAISSStore
from app.vectorstore.opensearch_store import OpenSearchStore
from app.models.document import Chunk

class RetrievalService:
    def __init__(self):
        """Initializes the Retrieval Service with embeddings and vector store clients."""
        self.embeddings = BedrockEmbeddings()
        if settings.USE_OPENSEARCH:
            self.vector_store = OpenSearchStore()
        else:
            self.vector_store = FAISSStore()
        
    def retrieve_context(self, question: str) -> List[Chunk]:
        """Retrieves the most relevant document chunks from the vector store for a given question."""
        logger.info(f"Retrieving context for question: {question}")
        
        # 1. Generate query embedding
        query_vector = self.embeddings.embed_text(question)
        
        # 2. Search FAISS
        chunks = self.vector_store.similarity_search(query_vector)
        
        return chunks
