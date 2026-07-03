from pydantic import BaseModel
from typing import List
from enum import Enum


class AIProvider(str, Enum):
    gpt = "gpt"
    gemini = "gemini"
    ollama = "ollama"
    grok = "grok"


class ChatRequest(BaseModel):
    ai: AIProvider
    query: str

class ChatResponse(BaseModel):
    response: str