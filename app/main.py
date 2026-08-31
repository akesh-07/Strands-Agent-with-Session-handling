from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import health, ingest, rag
from app.core.exceptions import AppBaseException
from app.core.logging import logger

import time

app = FastAPI(
    title="College RAG Assistant"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to manually log all incoming requests."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    client_host = request.client.host if request.client else "127.0.0.1"
    logger.info(f"{client_host} - \"{request.method} {request.url.path}\" {response.status_code} ({process_time:.3f}s)")
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("College RAG Assistant Server is starting up. Logging is active!")

# Exception handlers
@app.exception_handler(AppBaseException)
async def app_base_exception_handler(request: Request, exc: AppBaseException):
    """Handles custom AppBaseException by returning a properly formatted JSON response."""
    logger.error(f"App exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches all unhandled exceptions to prevent the server from crashing."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(ingest.router, tags=["Ingestion"])
app.include_router(rag.router, tags=["RAG"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
