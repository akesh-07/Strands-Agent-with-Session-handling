from app.core.logging import logger
from app.services.retrieval_service import RetrievalService
from app.services.prompt_service import PromptService
from app.providers.bedrock.llm import BedrockLLM
from app.models.response import AnswerResponse

class RAGService:
    def __init__(self):
        """Initializes dependencies required for the Retrieval-Augmented Generation pipeline."""
        self.retrieval_service = RetrievalService()
        self.prompt_service = PromptService()
        self.llm = BedrockLLM()

    def ask_question(self, question: str) -> AnswerResponse:
        """Processes a user question by retrieving context and generating an answer via the LLM."""
        logger.info(f"Answering question: {question}")
        
        # 1. Retrieve chunks
        chunks = self.retrieval_service.retrieve_context(question)
        
        # 2. Prepare context string
        context_parts = []
        
        for i, chunk in enumerate(chunks):
            # Include source info in the context provided to the LLM to help with grounding
            context_part = f"[Source {i+1}: {chunk.metadata.filename}, Page {chunk.metadata.page_number}]\n{chunk.text}"
            context_parts.append(context_part)
                
        context_str = "\n\n".join(context_parts)
        
        # 3. Build prompts
        system_prompt = self.prompt_service.get_system_prompt()
        rag_prompt = self.prompt_service.build_rag_prompt(context_str, question)
        
        # 4. Generate answer
        answer = self.llm.generate(system_prompt, rag_prompt)
        
        return AnswerResponse(answer=answer)
