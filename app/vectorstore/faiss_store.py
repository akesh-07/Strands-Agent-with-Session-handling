import os
import pickle
import faiss
import numpy as np
from typing import List
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import MissingFAISSIndexException
from app.models.document import Chunk

class FAISSStore:
    def __init__(self):
        """Initializes paths and state variables for the FAISS vector store."""
        self.index_path = settings.FAISS_INDEX_PATH
        self.metadata_path = settings.METADATA_PATH
        self.index = None
        self.metadata = []

    def create_index(self, dimension: int):
        """Creates a new empty FAISS index with the specified dimension."""
        logger.info(f"Creating new FAISS index with dimension {dimension}")
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def load_index(self):
        """Loads an existing FAISS index and its metadata from disk."""
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            raise MissingFAISSIndexException()
        
        logger.info(f"Loading FAISS index from {self.index_path}")
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)

    def save_index(self):
        """Saves the current FAISS index and metadata to disk."""
        if self.index is None:
            return
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        logger.info("Saved FAISS index and metadata")

    def add_vectors(self, vectors: List[List[float]], chunks: List[Chunk]):
        """Adds a list of embeddings and their corresponding chunks to the index."""
        if self.index is None:
            if not vectors:
                return
            dimension = len(vectors[0])
            self.create_index(dimension)
            
        vectors_np = np.array(vectors).astype('float32')
        self.index.add(vectors_np)
        self.metadata.extend(chunks)
        logger.info(f"Added {len(vectors)} vectors to FAISS index")

    def similarity_search(self, query_vector: List[float], top_k: int = None) -> List[Chunk]:
        """Searches the index for the most similar chunks to the given query vector."""
        if self.index is None:
            try:
                self.load_index()
            except MissingFAISSIndexException:
                return []
                
        if top_k is None:
            top_k = settings.TOP_K

        query_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.metadata):
                results.append(self.metadata[i])
                
        return results
