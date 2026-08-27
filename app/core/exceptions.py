from fastapi import HTTPException

class AppBaseException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class MissingPDFDirectoryException(AppBaseException):
    def __init__(self):
        super().__init__(status_code=404, detail="PDF directory not found.")

class EmptyPDFException(AppBaseException):
    def __init__(self, filename: str):
        super().__init__(status_code=400, detail=f"PDF {filename} is empty.")

class BedrockAuthException(AppBaseException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Bedrock Auth Error: {detail}")

class MissingFAISSIndexException(AppBaseException):
    def __init__(self):
        super().__init__(status_code=404, detail="FAISS index not found. Run ingestion first.")

class InvalidRequestPayloadException(AppBaseException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
