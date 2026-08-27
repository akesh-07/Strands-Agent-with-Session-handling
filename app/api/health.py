import os
from fastapi import APIRouter
from app.core.config import settings
from app.models.response import HealthResponse
from app.providers.bedrock.client import get_bedrock_client

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Description

    Check the health status of the API, Bedrock connection, and FAISS index.

    Request Body / Parameters:
    - None

    Returns:
    - The health status of the application components.
    - HTTP status code 200 on success.
    """
    bedrock_status = "ok"
    faiss_status = "ok"
    
    # Check Bedrock
    try:
        client = get_bedrock_client()
        # Just verifying the client was created successfully
    except Exception:
        bedrock_status = "error"
        
    # Check FAISS index
    if not os.path.exists(settings.FAISS_INDEX_PATH) or not os.path.exists(settings.METADATA_PATH):
        faiss_status = "missing"
        
    return HealthResponse(
        status="ok",
        bedrock=bedrock_status,
        faiss=faiss_status
    )