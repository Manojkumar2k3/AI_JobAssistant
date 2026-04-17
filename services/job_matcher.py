from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def match_resume_with_jd(resume_text: str, job_description: str):
    raw_output = ""

    try:
        prompt = f"""
You are an AI system.

STRICTLY return ONLY valid JSON.
DO NOT explain anything.
DO NOT add extra text.
DO NOT use markdown.

Format EXACTLY like this:

{{
  "match_score": 75,
  "missing_skills": ["skill1", "skill2"],
  "strengths": ["skill1", "skill2"]
}}

Resume:
{resume_text[:1500]}

Job Description:
{job_description}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw_output = response.choices[0].message.content

        # CLEANING (Robust)
        cleaned = raw_output.strip()

        # Remove markdown ``` blocks
        if "```" in cleaned:
            parts = cleaned.split("```")
            cleaned = parts[-1]

        # Remove 'json' keyword
        cleaned = cleaned.replace("json", "").strip()

        # Extract only JSON part
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        cleaned = cleaned[start:end]

        # Convert to dict
        data = json.loads(cleaned)

        return data

    except Exception as e:
        return {
            "error": "Parsing failed",
            "details": str(e),
            "raw": raw_output
        }
    
