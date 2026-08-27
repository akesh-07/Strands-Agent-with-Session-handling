from typing import Dict
from strands import Agent
from app.agent.rag_tool import college_handbook_lookup
from app.services.prompt_service import PromptService
from app.core.config import settings
from app.core.logging import logger

# Global dictionary to hold agent instances in memory
agents: Dict[str, Agent] = {}

def get_or_create_agent(session_id: str) -> Agent:
    """
    Retrieves the Agent for a given session ID.
    If it does not exist, creates a new one and stores it in the global registry.
    """
    if session_id not in agents:
        logger.info(f"Creating new Agent for session: {session_id}")
        prompt_service = PromptService()
        system_prompt = prompt_service.get_system_prompt()
        
        agents[session_id] = Agent(
            model=settings.BEDROCK_CHAT_MODEL,
            system_prompt=system_prompt,
            tools=[college_handbook_lookup]
        )
    return agents[session_id]
