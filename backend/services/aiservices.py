from openai import OpenAI
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# ==========================
# Environment Variables
# ==========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINIAPIKEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")

# ==========================
# Clients
# ==========================

# OpenAI
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Gemini
gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)

# Grok (xAI)
grok_client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# Ollama
ollama_client = OpenAI(
    base_url=OLLAMA_HOST,
    api_key="ollama"
)

# ==========================================================
# OpenAI
# ==========================================================

def chat_response_openai(query: str):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content


# ==========================================================
# Gemini
# ==========================================================

def chat_response_gemini(query: str):
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query
    )

    return response.text


# ==========================================================
# Grok
# ==========================================================

def chat_response_grok(query: str):
    response = grok_client.chat.completions.create(
        model="grok-3",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content


# ==========================================================
# Ollama
# ==========================================================

def chat_response_ollama(query: str):
    response = ollama_client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content


# ==========================================================
# Streaming OpenAI
# ==========================================================

def stream_chat_gpt(query: str):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            yield content


# ==========================================================
# Streaming Gemini
# ==========================================================

def stream_chat_gemini(query: str):
    response = gemini_client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=query
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


# ==========================================================
# Streaming Grok
# ==========================================================

def stream_chat_grok(query: str):
    response = grok_client.chat.completions.create(
        model="grok-3",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            yield content


# ==========================================================
# Streaming Ollama
# ==========================================================

def stream_chat_ollama(query: str):
    response = ollama_client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            yield content