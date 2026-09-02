from app.agents.session_registry import (
    create_router_agent, 
    create_academic_agent, 
    create_refund_agent, 
    create_anti_ragging_agent, 
    create_reviewer_agent
)
from app.services.prompt_service import PromptService
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
    
    # 1. Route the query
    router_agent = create_router_agent()
    logger.info(f"[USER]: {question}")
    router_response = await router_agent.invoke_async(question)
    category = _extract_text(router_response).strip().upper()
    logger.info(f"[ROUTER CLASSIFICATION]: {category}")
    
    # 2. Select specialist
    if "REFUND" in category:
        primary_agent = create_refund_agent(session_id)
    elif "SAFETY" in category:
        primary_agent = create_anti_ragging_agent(session_id)
    else:
        primary_agent = create_academic_agent(session_id)
        
    reviewer_agent = create_reviewer_agent(session_id)
    
    try:
        # 3. Domain specialist drafts a response
        response = await primary_agent.invoke_async(question)
        draft_text = _extract_text(response)
        logger.info(f"[PRIMARY AGENT DRAFT]:\n{draft_text}")
        
        # 2. Reviewer checks the draft
        prompt_service = PromptService()
        review_prompt = prompt_service.build_reviewer_task_prompt(draft_text)
        review_response = await reviewer_agent.invoke_async(review_prompt)
        review_text = _extract_text(review_response)
        logger.info(f"[COMPLIANCE OFFICER REVIEW]:\n{review_text}")
        
        # 3. Handle rejection (single retry)
        if "APPROVED" not in review_text:
            logger.info("[SYSTEM]: Draft rejected! Forcing Primary Agent to fix it...")
            fix_prompt = prompt_service.build_reviewer_fix_prompt(review_text)
            final_response = await primary_agent.invoke_async(fix_prompt)
            final_text = _extract_text(final_response)
            logger.info(f"[PRIMARY AGENT REVISED]:\n{final_text}")
            return final_text
            
        logger.info("[SYSTEM]: Draft approved! Sending to user.")
        return draft_text
        
    except Exception as e:
        logger.error(f"Error running Strands Agent: {e}")
        raise
