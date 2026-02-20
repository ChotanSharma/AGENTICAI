import os
from dotenv import load_dotenv
from typing import List
import json
from litellm import completion

# Load API key from .env
load_dotenv()   
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# all python functions to be used as the tools by the agent

def list_files() -> List[str]:
    """Lists all files in the given directory."""
    try:
        files = os.listdir(".")
        return files
    except FileNotFoundError:
        return [f"Error: Files not found in current directory."]
    except Exception as e:
        return [f"Error: {str(e)}"]
    
def read_file(file_name: str) -> str:
    """Reads the contents of a file."""
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return f"Error: File '{file_name}' not found."
    except Exception as e:
        return f"Error: {str(e)}"
    
def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    print(f"Termination message: {message}")

# Mapping function names to actual functions
tool_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate
}

# Define the tools with their specifications
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files in the current directory.",
            "parameters": {"type":"object", "properties": {}, "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type":"object", 
                "properties": {
                    "file_name": {"type": "string"}}, 
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation. No further actions or interactions are possible after this. Prints the provided message for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        }
    }
]

# Define the agent's system rules
agent_rules = [
    {
        "role": "system",
        "content": 
        """
You are a file management agent that can list and read files in the current directory.
You must use the provided functions to interact with the file system.
Follow these rules strictly:
When you are done, terminate the conversation by using the "terminate" tool 
and I will provide the results to the user.
"""
    }
]

#Initialize conversation with system rules
iterations = 0
max_iterations = 10

user_task = input("What would you like to do with the agent?").strip()

memory = [{"role": "user", "content":user_task}]

# Agent interaction loop
while iterations < max_iterations:
    messages = agent_rules + memory

    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        tools=tools,
        max_tokens=1024,
        api_key=OPENAI_API_KEY
    )

    if response.choices[0].message.tool_calls:
        tool = response.choices[0].message.tool_calls[0]
        tool_name = tool.function.name
        tool_args = json.loads(tool.function.arguments)

        action ={
            "tool_name": tool_name,
            "args": tool_args
        }

        if tool_name == "terminate":
            print(f"Termination message: {tool_args['message']}")
            break
        elif tool_name in tool_functions:
            try: 
                result = {"result": tool_functions[tool_name](**tool_args)}
                print(f"Result: {result}")
            except Exception as e:
                result = {"error": f"Error executing tool '{tool_name}': {str(e)}"}
        else:
            result = {"error": f"Tool '{tool_name}' not recognized."}

        print(f"Executing tool: {tool_name} with arguments {tool_args}")
        memory.extend([
            {"role": "assistant",
             "content": json.dumps(action)},
             {"role": "user", "content": json.dumps(result)}
        ])
    else:
        result = response.choices[0].message.content
        print(f"Agent response: {result}")
        break
    iterations += 1


