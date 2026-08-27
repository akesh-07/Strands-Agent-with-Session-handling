from typing import List, Tuple
from app.core.config import settings
from app.core.logging import logger
from app.models.document import Chunk, ChunkMetadata

class TextChunker:
    @staticmethod
    def chunk_text(pages: List[Tuple[int, str]], filename: str) -> List[Chunk]:
        """
        Splits text into chunks of specified token size and overlap.
        For simplicity, using simple word count as token proxy.
        """
        logger.info(f"Chunking text for {filename}")
        chunks = []
        chunk_size = settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP

        for page_num, text in pages:
            words = text.split()
            if not words:
                continue
            
            i = 0
            chunk_index = 0
            while i < len(words):
                end = min(i + chunk_size, len(words))
                chunk_words = words[i:end]
                chunk_text = " ".join(chunk_words)
                
                chunk_id = f"{filename}_p{page_num}_c{chunk_index}"
                chunks.append(Chunk(
                    text=chunk_text,
                    metadata=ChunkMetadata(
                        filename=filename,
                        page_number=page_num,
                        chunk_id=chunk_id
                    )
                ))
                
                i += (chunk_size - overlap)
                chunk_index += 1
                
        return chunks
