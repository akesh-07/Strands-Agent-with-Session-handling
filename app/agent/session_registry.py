from strands import Agent
from strands.session import S3SessionManager
from app.agent.rag_tool import college_handbook_lookup
from app.agent.refund_tool import check_refund_documents_and_eligibility
from app.agent.complaint_tool import log_anonymous_anti_ragging_complaint
from app.services.prompt_service import PromptService
from app.core.config import settings
from app.core.logging import logger

def create_agent(session_id: str) -> Agent:
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
        tools=[college_handbook_lookup, check_refund_documents_and_eligibility, log_anonymous_anti_ragging_complaint],
        session_manager=session_manager
    )

def create_reviewer_agent(session_id: str) -> Agent:
    """Creates a secondary Compliance Officer Agent to review drafts."""
    logger.info(f"Creating new Reviewer Agent for session: {session_id}")
    
    system_prompt = """You are a strict compliance officer for a college.
    Your job is to review the drafted responses written by the primary assistant.
    Ensure the response is polite, helpful, and does not leak personal or sensitive identifying information.
    If the response is good, reply ONLY with the exact word 'APPROVED'.
    If the response has issues, reply with 'REJECTED:' followed by the reason why it was rejected."""
    
    return Agent(
        agent_id=f"{session_id}-reviewer",
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[] # The reviewer has no tools
    )
