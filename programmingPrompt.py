from dotenv import load_dotenv
import os

from litellm import completion
from typing import List, Dict

# Load API key from .env
load_dotenv()   
API_KEY = os.getenv("OPENAI_API_KEY")
print(API_KEY[:10] + "...")  # just to check

def generate_response(message) -> str:
    response = completion(
        model="openai/gpt-4o",
        messages=message,
        max_tokens=1024,
        api_key=API_KEY
    )
    return response.choices[0].message.content

#define messages
messages = [
    {"role": "system", "content": "You are a helpful programming assistant."},
    {"role": "user", "content": "Write a Python function that checks if a number is prime."}
]

response = generate_response(messages)
print(response)
