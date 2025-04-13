import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure Groq-compatible OpenAI client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def chat_with_groq(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=2048
    )
    return response.choices[0].message.content
