import os
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
