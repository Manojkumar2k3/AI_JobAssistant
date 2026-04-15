from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_skills(text: str):
    try:
        prompt = f"""
Extract:
- skills
- tools
- experience level

Return STRICTLY in JSON format:
{{
  "skills": [],
  "tools": [],
  "experience_level": ""
}}

Resume:
{text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return str(e)