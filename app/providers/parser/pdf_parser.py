import fitz
import os
from typing import List, Tuple
from app.core.logging import logger
from app.core.exceptions import EmptyPDFException

class PDFParser:
    @staticmethod
    def extract_text(file_path: str) -> List[Tuple[int, str]]:
        """
        Extract text from PDF preserving page numbers.
        Returns a list of (page_number, text)
        """
        logger.info(f"Extracting text from {file_path}")
        extracted_pages = []
        try:
            doc = fitz.open(file_path)
            if doc.page_count == 0:
                raise EmptyPDFException(os.path.basename(file_path))
            
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text.strip():
                    # 1-indexed page numbers
                    extracted_pages.append((page_num + 1, text))
            doc.close()
            return extracted_pages
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise
