from strands import Agent
from strands.session import S3SessionManager
from app.tools.rag_tool import college_handbook_lookup
from app.tools.refund_tool import check_refund_documents_and_eligibility
from app.tools.complaint_tool import log_anonymous_anti_ragging_complaint
from app.services.prompt_service import PromptService
from app.core.config import settings
from app.core.logging import logger

def _get_session_manager(session_id: str) -> S3SessionManager:
    return S3SessionManager(
        session_id=session_id,
        bucket=settings.S3_BUCKET,
        prefix="chat-sessions/",
        region_name=settings.AWS_REGION
    )

def create_router_agent() -> Agent:
    """Creates a stateless Router Agent to classify user queries."""
    prompt_service = PromptService()
    system_prompt = prompt_service.get_router_prompt()
    
    return Agent(
        agent_id="router",
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[]
    )

def create_academic_agent(session_id: str) -> Agent:
    """Creates the Academic Specialist Agent."""
    logger.info(f"Creating Academic Agent for session: {session_id}")
    prompt_service = PromptService()
    system_prompt = prompt_service.get_system_prompt()
    
    return Agent(
        agent_id=session_id,
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[college_handbook_lookup],
        session_manager=_get_session_manager(session_id)
    )

def create_refund_agent(session_id: str) -> Agent:
    """Creates the Finance & Refund Specialist Agent."""
    logger.info(f"Creating Refund Agent for session: {session_id}")
    prompt_service = PromptService()
    system_prompt = prompt_service.get_refund_prompt()
    
    return Agent(
        agent_id=session_id,
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[check_refund_documents_and_eligibility],
        session_manager=_get_session_manager(session_id)
    )

def create_anti_ragging_agent(session_id: str) -> Agent:
    """Creates the Student Safety Specialist Agent."""
    logger.info(f"Creating Anti-Ragging Agent for session: {session_id}")
    prompt_service = PromptService()
    system_prompt = prompt_service.get_anti_ragging_prompt()
    
    return Agent(
        agent_id=session_id,
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[log_anonymous_anti_ragging_complaint],
        session_manager=_get_session_manager(session_id)
    )

def create_reviewer_agent(session_id: str) -> Agent:
    """Creates a secondary Compliance Officer Agent to review drafts."""
    logger.info(f"Creating new Reviewer Agent for session: {session_id}")
    prompt_service = PromptService()
    system_prompt = prompt_service.get_reviewer_prompt()
    
    return Agent(
        agent_id=f"{session_id}-reviewer",
        model=settings.BEDROCK_CHAT_MODEL,
        system_prompt=system_prompt,
        tools=[] # The reviewer has no tools
    )
