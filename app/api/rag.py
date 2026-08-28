from fastapi import APIRouter, HTTPException
from app.models.request import QuestionRequest
from app.models.response import AnswerResponse
from app.agent.strands_agent import ask_agent
from app.core.exceptions import AppBaseException

router = APIRouter()

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Description

    Ask a question to the College RAG Assistant based on the ingested college guidelines.

    Request Body / Parameters:
    - request: The QuestionRequest object containing the user's session_id and question.

    Returns:
    - The generated answer from the LLM based on retrieved context.
    - HTTP status code 200 on success.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    if not request.session_id or not request.session_id.strip():
        raise HTTPException(status_code=400, detail="session_id cannot be empty.")
        
    try:
        # Call the Strands agent, passing session_id and question
        answer_text = await ask_agent(request.session_id, request.question)
        return AnswerResponse(answer=answer_text)
    except AppBaseException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))