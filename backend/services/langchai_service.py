import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Load .env from the backend directory explicitly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

# Prompt template with memory placeholder
prompt_with_memory = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful career guidance assistant."),
    ("placeholder", "{chat_history}"),
    ("human", "{user_query}")
])

# Chain: prompt -> LLM
chain_with_memory = prompt_with_memory | llm

# In-memory store for session histories
store = {}

def get_history(session_id: str) -> ChatMessageHistory:
    """Get or create conversation history for a given session."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Runnable with message history - automatically manages chat history per session
chat_with_memory = RunnableWithMessageHistory(
    runnable=chain_with_memory,
    get_session_history=get_history,
    input_messages_key="user_query",
    history_messages_key="chat_history"
)

def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
    """Send a question to the career chatbot with session-based memory."""
    response = chat_with_memory.invoke(
        {"user_query": question},
        {"configurable": {"session_id": session_id}}
    )
    return response.content