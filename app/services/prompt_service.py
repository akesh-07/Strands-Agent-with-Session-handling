import os
from app.core.logging import logger

class PromptService:
    def __init__(self):
        """Initializes paths and caches for prompt templates."""
        self.system_prompt_path = "prompts/system_prompt.txt"
        self.rag_prompt_path = "prompts/rag_prompt.txt"
        self._system_prompt_cache = None
        self._rag_prompt_cache = None

    def get_system_prompt(self) -> str:
        """Loads and returns the system prompt instructing the AI's behavior."""
        if self._system_prompt_cache is None:
            self._system_prompt_cache = self._load_prompt(self.system_prompt_path)
        return self._system_prompt_cache

    def get_rag_prompt_template(self) -> str:
        """Loads and returns the base template for the RAG user query."""
        if self._rag_prompt_cache is None:
            self._rag_prompt_cache = self._load_prompt(self.rag_prompt_path)
        return self._rag_prompt_cache

    def build_rag_prompt(self, context: str, question: str) -> str:
        """Injects the retrieved context and user question into the RAG template."""
        template = self.get_rag_prompt_template()
        return template.replace("{context}", context).replace("{question}", question)

    def _load_prompt(self, path: str) -> str:
        """Reads a prompt file from disk and returns its contents."""
        if not os.path.exists(path):
            logger.error(f"Prompt file {path} not found.")
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
