import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment or .env file.")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.3
    }
)

def generate_questions(text: str, count: int = 5):
    prompt = f"""
Luo tarkalleen {count} monivalintakysymystä seuraavasta tekstistä JSON-muodossa.

Vastausmuoto on täsmälleen tämä:

{{
  "questions": [
    {{
      "question": "Kysymysteksti",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A"
    }}
  ]
}}

Älä lisää JSONin ulkopuolelle mitään muuta sisältöä.  
Käytä suomen kieltä.

Teksti:
{text}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text  # tämä toimii kun response_mime_type=application/json
    except Exception as e:
        print("Gemini API error:", e)
        return []

    try:
        data = json.loads(raw)
    except Exception as e:
        print("JSON parse error:", e)
        print("Raw response:", raw)
        return []

    questions = data.get("questions")
    if not isinstance(questions, list):
        print("JSON lacks 'questions' field:", data)
        return []

    return questions