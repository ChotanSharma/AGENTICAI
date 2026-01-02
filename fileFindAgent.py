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
    "terminate_agent": terminate
}