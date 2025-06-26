# services/gpt_metadata_extraction.py

import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_metadata_from_query(query: str) -> dict:
    prompt = f"""
Extract metadata filters from this query: "{query}"

Return a JSON with only applicable keys:
- employee_name
- story_type
- project_type
- status
- point
- hours
- story_id
- task_name
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print("Metadata parsing error:", e)
        return {}
