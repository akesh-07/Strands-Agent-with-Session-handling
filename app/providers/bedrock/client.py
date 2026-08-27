import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import BedrockAuthException

class BedrockClient:
    _instance = None

    def __new__(cls):
        """Initializes a Singleton Bedrock runtime client."""
        if cls._instance is None:
            cls._instance = super(BedrockClient, cls).__new__(cls)
            try:
                client_kwargs = {
                    "service_name": "bedrock-runtime",
                    "region_name": settings.AWS_REGION
                }
                
                # Use explicit credentials if provided in .env
                if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                    client_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                    client_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
                    
                    if settings.AWS_SESSION_TOKEN:
                        client_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
                
                cls._instance.client = boto3.client(**client_kwargs)
            except Exception as e:
                logger.error(f"Failed to initialize Bedrock client: {e}")
                raise BedrockAuthException(str(e))
        return cls._instance

    def get_client(self):
        """Returns the initialized Bedrock client."""
        return self.client

bedrock_client_singleton = BedrockClient()

def get_bedrock_client():
    """Helper function to fetch the Singleton Bedrock client instance."""
    return bedrock_client_singleton.get_client()
