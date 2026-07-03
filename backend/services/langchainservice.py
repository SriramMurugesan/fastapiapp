from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")


prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
You are a helpful AI assistant.

Conversation History:
{history}

Human:
{input}

Assistant:
"""
)


def get_llm(provider: str):
    provider = provider.lower()

    if provider == "gpt":
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=OPENAI_API_KEY,
            temperature=0.7
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )

    elif provider == "grok":
        return ChatGroq(
            model="llama-3.3-70b-versatile",   # or another model supported by your Groq account
            api_key=GROK_API_KEY,
            temperature=0.7
        )

    elif provider == "ollama":
        return ChatOllama(
            model="llama3.2",
            base_url=OLLAMA_HOST,
            temperature=0.7
        )

    else:
        raise ValueError("Unsupported AI Provider")


def chat_response_langchain(query: str, provider: str):
    memory = ConversationBufferMemory()

    conversation = ConversationChain(
        llm=get_llm(provider),
        memory=memory,
        prompt=prompt,
        verbose=False
    )

    return conversation.predict(input=query)