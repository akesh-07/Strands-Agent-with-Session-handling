from strands.tools import tool
from app.services.retrieval_service import RetrievalService
from app.core.logging import logger

@tool
def college_handbook_lookup(query: str) -> str:
    """
    Search the college handbook for information relevant to the user's query.
    Always use this tool when the user asks a question about college guidelines, rules, or policies.
    """
    logger.info(f"Running college_handbook_lookup for query: {query}")
    retrieval_service = RetrievalService()
    
    try:
        chunks = retrieval_service.retrieve_context(query)
        
        if not chunks:
            return "No relevant information found in the college handbook."
            
        context_parts = []
        for i, chunk in enumerate(chunks):
            # Include source info in the context
            context_part = f"[Source {i+1}: {chunk.metadata.filename}, Page {chunk.metadata.page_number}]\n{chunk.text}"
            context_parts.append(context_part)
            
        return "\n\n".join(context_parts)
    except Exception as e:
        logger.error(f"Error in college_handbook_lookup tool: {e}")
        return f"Error retrieving information: {str(e)}"
