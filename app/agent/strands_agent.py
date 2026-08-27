from app.agent.session_registry import get_or_create_agent
from app.core.logging import logger

def ask_agent(session_id: str, question: str) -> str:
    """
    Retrieves the Agent for a given session and runs it.
    """
    logger.info(f"Invoking Strands Agent for session: {session_id}")
    
    agent = get_or_create_agent(session_id)
    
    try:
        response = agent(question)
        
        # Extract text from the model's final message
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            texts = []
            for block in response.message.content:
                if hasattr(block, 'text'):
                    texts.append(block.text)
                elif isinstance(block, dict) and 'text' in block:
                    texts.append(block['text'])
            return "\n".join(texts) if texts else str(response.message.content)
            
        return str(response)
    except Exception as e:
        logger.error(f"Error running Strands Agent: {e}")
        raise
