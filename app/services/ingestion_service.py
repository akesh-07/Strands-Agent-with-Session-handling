import os
import time
from app.core.logging import logger
from app.core.exceptions import MissingPDFDirectoryException
from app.providers.parser.pdf_parser import PDFParser
from app.providers.parser.text_cleaner import TextCleaner
from app.providers.parser.chunker import TextChunker
from app.providers.bedrock.embeddings import BedrockEmbeddings
from app.core.config import settings
from app.vectorstore.faiss_store import FAISSStore
from app.vectorstore.opensearch_store import OpenSearchStore
from app.models.response import IngestResponse

class IngestionService:
    def __init__(self):
        """Initializes the ingestion service dependencies."""
        self.raw_dir = "data/raw"
        self.embeddings = BedrockEmbeddings()
        if settings.USE_OPENSEARCH:
            self.vector_store = OpenSearchStore()
        else:
            self.vector_store = FAISSStore()

    def ingest_all(self) -> IngestResponse:
        """Orchestrates parsing PDFs, chunking text, embedding, and indexing into FAISS."""
        start_time = time.time()
        
        if not os.path.exists(self.raw_dir):
            raise MissingPDFDirectoryException()
            
        pdf_files = [f for f in os.listdir(self.raw_dir) if f.lower().endswith('.pdf')]
        
        total_chunks = 0
        all_chunks = []
        all_vectors = []
        
        for filename in pdf_files:
            file_path = os.path.join(self.raw_dir, filename)
            logger.info(f"Processing {filename}")
            
            # Extract text
            pages = PDFParser.extract_text(file_path)
            
            # Clean text
            cleaned_pages = [(page_num, TextCleaner.clean(text)) for page_num, text in pages]
            
            # Chunk text
            chunks = TextChunker.chunk_text(cleaned_pages, filename)
            total_chunks += len(chunks)
            all_chunks.extend(chunks)
            
            # Generate embeddings
            for chunk in chunks:
                vector = self.embeddings.embed_text(chunk.text)
                all_vectors.append(vector)
                
        # Store in FAISS
        if all_vectors:
            self.vector_store.add_vectors(all_vectors, all_chunks)
            self.vector_store.save_index()
            
        duration = time.time() - start_time
        logger.info(f"Ingestion completed. {len(pdf_files)} PDFs, {total_chunks} chunks.")
        
        return IngestResponse(
            number_of_pdfs=len(pdf_files),
            chunks_created=total_chunks,
            indexing_duration_seconds=duration
        )
