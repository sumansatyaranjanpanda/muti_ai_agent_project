from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agent
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    query: List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f'Received request for model: {request.model_name}')
    
    if request.model_name not in settings.MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agent(
            request.model_name,
            request.query,
            request.allow_search,
            request.system_prompt
        )
        logger.info(f"Successfully got response from AI agent: {request.model_name}")
        return {"response": response}
    
    except Exception as e:
        logger.error(f"Something error occurred during response generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(CustomException("Failed to get AI response", error_detail=e))
        )