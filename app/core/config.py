from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_SESSION_TOKEN: str | None = None
    BEDROCK_EMBED_MODEL: str = "amazon.titan-embed-text-v2:0"
    BEDROCK_CHAT_MODEL: str = "amazon.nova-lite-v1:0"
    FAISS_INDEX_PATH: str = "vector_store/faiss.index"
    METADATA_PATH: str = "vector_store/metadata.pkl"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 5
    LOG_LEVEL: str = "INFO"
    S3_BUCKET: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()

# Inject credentials into os.environ so that third-party libraries (like Strands and Boto3 defaults) can find them
import os
if settings.AWS_ACCESS_KEY_ID:
    os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
if settings.AWS_SECRET_ACCESS_KEY:
    os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
if settings.AWS_SESSION_TOKEN:
    os.environ["AWS_SESSION_TOKEN"] = settings.AWS_SESSION_TOKEN
if settings.AWS_REGION:
    os.environ["AWS_REGION"] = settings.AWS_REGION
