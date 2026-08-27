import json
from app.providers.bedrock.client import get_bedrock_client
from app.core.config import settings
from app.core.logging import logger

class BedrockEmbeddings:
    def __init__(self):
        """Initializes Bedrock Embeddings with the configured model ID."""
        self.client = get_bedrock_client()
        self.model_id = settings.BEDROCK_EMBED_MODEL

    def embed_text(self, text: str) -> list[float]:
        """Generates and returns vector embeddings for a given input text."""
        try:
            body = json.dumps({"inputText": text})
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept='application/json',
                contentType='application/json'
            )
            response_body = json.loads(response.get('body').read())
            return response_body.get('embedding')
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
