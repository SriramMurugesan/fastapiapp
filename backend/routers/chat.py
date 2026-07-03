from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse, AIProvider
from services.aiservices import stream_chat_gpt,stream_chat_gemini,stream_chat_ollama,stream_chat_grok,chat_response_grok,chat_response_openai,chat_response_gemini,chat_response_ollama
from langchainservice import chat_response_langchain

router = APIRouter(prefix="/chat",tags=["chat"])

AI_HANDLERS = {
    AIProvider.gpt: chat_response_openai,
    AIProvider.gemini: chat_response_gemini,
    AIProvider.ollama: chat_response_ollama,
    AIProvider.grok: chat_response_grok,
}
STREAM_HANDLERS = {
    AIProvider.gpt: stream_chat_gpt,
    AIProvider.gemini: stream_chat_gemini,
    AIProvider.ollama: stream_chat_ollama,
    AIProvider.grok: stream_chat_grok,
}

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    handler = AI_HANDLERS.get(request.ai)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {request.ai}")
    response = handler(request.query)
    return ChatResponse(response=response)
@router.post("/stream")
def stream_chat(request: ChatRequest):
    handler = STREAM_HANDLERS.get(request.ai)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {request.ai}")
    return StreamingResponse(handler(request.query),media_type="text/event-stream")
@router.post("/career", response_model=ChatResponse)
def langchain_chat(request: ChatRequest):
    response = chat_response_langchain(
        request.query,
        request.ai.value
    )

    return ChatResponse(response=response)