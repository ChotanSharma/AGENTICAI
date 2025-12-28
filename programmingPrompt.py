from dotenv import load_dotenv
import os

from litellm import Completion
from typing import List, Dict



load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")



