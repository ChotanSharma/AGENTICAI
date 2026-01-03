from litellm import completion
from typing import List, Dict

import os
from dotenv import load_dotenv

from programmingPrompt import generate_response

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

# Function to extract code block from the response
"""
Extracts and returns the code inside a Markdown-style
triple-backtick (```) code block from a response string.
"""
def extract_code_block(response: str) -> str:
   # Check if the response contains a Markdown code block delimiter
   # If no triple backticks are found, there is no code block to extract,
   # so return the original response unchanged.

   if not '```' in response:
      return response

    # We take index 1 to get only the code block content,   
   code_block = response.split('```')[1].strip ()

   # Check for "python" at the start and remove
   if code_block.startswith("python"):
      code_block = code_block[6:]

   return code_block


def develop_custom_function():
    # Get user input for function description
    print("\nWhat kind of function would you like to create?")
    print("Example: 'A function that calculates the factorial of a number'")
    print("Your description: ", end='')
    function_description = input().strip() # Get user input

    # Initialize conversation with system prompt
    messages = [
        {"role": "system", "content": "You are a Python expert helping to develop a function."}
    ]

    # First prompt - Basic function
    messages.append({
        "role": "user",
        "content": f"Write a Python function that {function_description}. Output the function in a ```python code block```."
    })
    initial_function = generate_response(messages)

    # Parse the response to get the function code
    initial_function = extract_code_block(initial_function)

    # printing the response of initial function
    print("\n=== Initial Function ===")
    print(initial_function)

    # Add assistant's response to conversation
    messages.append({"role": "assistant", "content": "\`\`\`python\n\n"+initial_function+"\n\n\`\`\`"})

    # Second prompt - Add documentation
    messages.append({
      "role": "user",
      "content": "Add comprehensive documentation to this function, including description, parameters, "
                 "return value, examples, and edge cases. Output the function in a ```python code block```."
    })
    
    documented_function = generate_response(messages)
    documented_function = extract_code_block(documented_function)
    print("\n=== Documented Function ===")
    print(documented_function)

    # Add documentation response to conversation
    messages.append({"role": "assistant", "content": "\`\`\`python\n\n"+documented_function+"\n\n\`\`\`"})

    # Third prompt - Add test cases
    messages.append({
        "role": "user",
        "content": "Add unittest test cases for this function, including tests for basic functionality, "
            "edge cases, error cases, and various input scenarios. Output the code in a \`\`\`python code block\`\`\`."
    })
   
    test_cases = generate_response(messages)
    # We will likely run into random problems here depending on if it outputs JUST the test cases or the
    # test cases AND the code. This is the type of issue we will learn to work through with agents in the course.
    test_cases = extract_code_block(test_cases)
    print("\n=== Test Cases ===")
    print(test_cases)

    # Generate filename from function description
    filename = function_description.lower()
    filename = ''.join(c for c in filename if c.isalnum() or c.isspace())
    filename = filename.replace(' ', '_')[:30] + '.py'

    # Save the documented function and test cases to a file
    with open(filename, 'w') as f:
        f.write("# Documented Function\n")
        f.write(documented_function + "\n\n")
        f.write("# Test Cases\n")
        f.write(test_cases + "\n")
    
    return documented_function, test_cases, filename


# Example usage
if __name__ == "__main__":
    function_code, tests, filename = develop_custom_function()
    print(f"\nFinal code has been saved to {filename}")

