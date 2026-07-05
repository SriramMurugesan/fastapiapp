from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.llm_service import llm_response
from services.langchai_service import ask_career_chatbot_response

router = APIRouter(prefix="/chat",tags=["Chat"])

# @router.post("/ask",response_model=ChatResponse)    
# def chat_ask(request:ChatRequest):
#     ans = llm_response(request.message)
#     return ChatResponse(response=ans)


@router.post("/ask_career",response_model=ChatResponse)
def ask_career_chatbot(request:ChatRequest):
    ans = ask_career_chatbot_response(request.message, request.session_id)
    return ChatResponse(response=ans)   