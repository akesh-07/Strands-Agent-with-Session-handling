from fastapi import APIRouter, HTTPException
from app.models.response import IngestResponse
from app.services.ingestion_service import IngestionService
from app.core.exceptions import AppBaseException

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
def ingest_documents():
    """
    Description

    Trigger the ingestion pipeline to process all PDFs in the raw data directory.

    Request Body / Parameters:
    - None

    Returns:
    - Statistics about the ingestion process including number of PDFs processed, chunks created, and duration.
    - HTTP status code 200 on success.
    """
    service = IngestionService()
    try:
        response = service.ingest_all()
        return response
    except AppBaseException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
