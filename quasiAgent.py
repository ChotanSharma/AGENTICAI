from litellm import completion
from typing import List, Dict

import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()   
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def quasi_agent(messages: List[Dict[str, str]]) -> str:
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024,
        api_key=OPENAI_API_KEY
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are an expert software engineer that prefers python programming."},
        {"role": "user", "content": "Write a function that takes a list of integers and returns the sum of the even numbers in the list."},
        {"role": "assistant", "content": response},
        {"role": "user", "content": "Provide comments for parsing the codes."}
    ]
    response = quasi_agent(messages)
    print(response)

