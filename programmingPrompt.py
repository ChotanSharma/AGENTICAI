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
    {"role": "system", "content": "You are a helpful career assistant."},
    {"role": "user", "content": "Write a pitch for a candidate applying for a software engineering position at a tech company. The candidate has 5 years of experience in full-stack development, is proficient in Python and JavaScript, and has led several successful projects."}
]

response = generate_response(messages)
print(response)
