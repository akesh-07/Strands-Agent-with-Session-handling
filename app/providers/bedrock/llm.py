import json
from app.providers.bedrock.client import get_bedrock_client
from app.core.config import settings
from app.core.logging import logger

class BedrockLLM:
    def __init__(self):
        """Initializes the Bedrock LLM client with the configured model ID."""
        self.client = get_bedrock_client()
        self.model_id = settings.BEDROCK_CHAT_MODEL

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Sends prompts to the Amazon Nova Lite model and returns the generated answer."""
        try:
            # Amazon Nova Lite input format format via Converse API
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_prompt}]
                    }
                ],
                system=[
                    {"text": system_prompt}
                ],
                inferenceConfig={
                    "maxTokens": 500,
                    "temperature": 0.0
                }
            )
            return response['output']['message']['content'][0]['text']
        except Exception as e:
            logger.error(f"Error generating text from LLM: {e}")
            raise
