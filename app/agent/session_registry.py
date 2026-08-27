from strands import Agent
from strands.session import S3SessionManager
from app.agent.rag_tool import college_handbook_lookup
from app.services.prompt_service import PromptService
from app.core.config import settings
from app.core.logging import logger

def get_or_create_agent(session_id: str) -> Agent:
    """
    Creates a new Strands Agent for a given session ID using S3SessionManager.
    Conversation history is automatically managed via the S3 bucket.
    """
    logger.info(f"Creating new Agent with S3SessionManager for session: {session_id}")
    prompt_service = PromptService()
    system_prompt = prompt_service.get_system_prompt()
    
    session_manager = S3SessionManager(
        session_id=session_id,
        bucket=settings.S3_BUCKET,
        prefix="chat-sessions/",
        region_name=settings.AWS_REGION
    )
    
    return Agent(
        agent_id=session_id,
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[college_handbook_lookup],
        session_manager=session_manager
    )
