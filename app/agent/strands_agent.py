from app.agent.session_registry import create_agent, create_reviewer_agent
from app.core.logging import logger

def _extract_text(response) -> str:
    """Helper to extract text from the Bedrock response."""
    if hasattr(response, 'message') and hasattr(response.message, 'content'):
        texts = []
        for block in response.message.content:
            if hasattr(block, 'text'):
                texts.append(block.text)
            elif isinstance(block, dict) and 'text' in block:
                texts.append(block['text'])
        return "\n".join(texts) if texts else str(response.message.content)
    return str(response)

async def ask_agent(session_id: str, question: str) -> str:
    """
    Retrieves the primary and reviewer Agents and orchestrates the A2A flow.
    """
    logger.info(f"Invoking Strands Agent for session: {session_id}")
    
    primary_agent = create_agent(session_id)
    reviewer_agent = create_reviewer_agent(session_id)
    
    try:
        # 1. Primary agent drafts a response
        logger.info(f"[USER]: {question}")
        response = await primary_agent.invoke_async(question)
        draft_text = _extract_text(response)
        logger.info(f"[PRIMARY AGENT DRAFT]:\n{draft_text}")
        
        # 2. Reviewer checks the draft
        review_prompt = f"Please review this drafted response: '{draft_text}'. If it is safe and polite, reply exactly 'APPROVED'. If not, reply 'REJECTED: [reason]'."
        review_response = await reviewer_agent.invoke_async(review_prompt)
        review_text = _extract_text(review_response)
        logger.info(f"[COMPLIANCE OFFICER REVIEW]:\n{review_text}")
        
        # 3. Handle rejection (single retry)
        if "APPROVED" not in review_text:
            logger.info("[SYSTEM]: Draft rejected! Forcing Primary Agent to fix it...")
            fix_prompt = f"The compliance officer rejected your draft with this feedback: '{review_text}'. Please provide a revised response fixing these issues."
            final_response = await primary_agent.invoke_async(fix_prompt)
            final_text = _extract_text(final_response)
            logger.info(f"[PRIMARY AGENT REVISED]:\n{final_text}")
            return final_text
            
        logger.info("[SYSTEM]: Draft approved! Sending to user.")
        return draft_text
        
    except Exception as e:
        logger.error(f"Error running Strands Agent: {e}")
        raise
