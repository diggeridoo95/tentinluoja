import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Ladataan .env -> API-avaimen haku ympäristömuuttujasta
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Jos avainta ei löydy, nostetaan virhe. Sovellus ei voi jatkaa ilman avainta.
    raise RuntimeError("GEMINI_API_KEY is not set in environment or .env file.")

# Konfiguroidaan genai-kirjasto
genai.configure(api_key=API_KEY)

# Mallin nimi ja oletusparametrit
MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config={
        # Pyydetään vastausta JSON-muodossa, helpottaa parsimista
        "response_mime_type": "application/json",
        "temperature": 0.3
    }
)

def generate_questions(text: str, count: int = 5):
    """
    Rakentaa promptin ja kutsuu Geminin API:ta.
    - text: lähdeteksti josta kysymykset generoidaan
    - count: haluttujen kysymysten määrä
    Funktio odottaa, että malli palauttaa täsmällistä JSONia muodossa:
    {
      "questions": [
        { "question": "...", "options": ["A","B","C","D"], "correct_answer": "..." }
      ]
    }
    Palauttaa Python-listan kysymyksiä tai tyhjän listan virhetilanteessa.
    """
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
        # Kutsutaan mallia; response.text sisältää JSON-merkkijonon kun response_mime_type=application/json
        response = model.generate_content(prompt)
        raw = response.text
    except Exception as e:
        # Logataan virhe ja palautetaan tyhjä lista
        print("Gemini API error:", e)
        return []

    try:
        # Parsitaan JSON-string Pythoniksi
        data = json.loads(raw)
    except Exception as e:
        print("JSON parse error:", e)
        print("Raw response:", raw)
        return []

    # Oletetaan että data sisältää avaimen "questions" joka on lista
    questions = data.get("questions")
    if not isinstance(questions, list):
        print("JSON lacks 'questions' field:", data)
        return []

    return questions