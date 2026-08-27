import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ingestion_service import IngestionService
from app.core.logging import logger

def main():
    """CLI entry point to trigger the document ingestion process manually."""
    logger.info("Starting local document ingestion...")
    service = IngestionService()
    try:
        response = service.ingest_all()
        logger.info(f"Ingestion successful! Processed {response.number_of_pdfs} PDFs resulting in {response.chunks_created} chunks in {response.indexing_duration_seconds:.2f} seconds.")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")

if __name__ == "__main__":
    main()
