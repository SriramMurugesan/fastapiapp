from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from services.langchai_service import ask_career_chatbot_response
from utils.logging_config import get_logger

router = APIRouter(prefix="/chat",tags=["Chat"])
logger = get_logger("routers.chat")

# @router.post("/ask",response_model=ChatResponse)    
# def chat_ask(request:ChatRequest):
#     ans = llm_response(request.message)
#     return ChatResponse(response=ans)


@router.post("/ask_career",response_model=ChatResponse)
def ask_career_chatbot(request: ChatRequest):
    logger.info(f"Chat request received: '{request.message}' | Session ID: '{request.session_id}'")
    try:
        ans = ask_career_chatbot_response(request.message, request.session_id)
        logger.info(f"Chat response generated successfully for Session ID: '{request.session_id}'")
        return ChatResponse(response=ans)   
    except Exception as e:
        logger.error(f"Failed to generate response for Session ID '{request.session_id}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Career chatbot service error: {str(e)}")