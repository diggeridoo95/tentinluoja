import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import traceback

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("GEMINI_API_KEY ei löydy. Lisää .env tai aseta ympäristömuuttuja.")
    sys.exit(2)

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print("genai.configure epäonnistui:", e)
    traceback.print_exc(limit=1)

MODEL = "models/gemini-2.0-flash"

def main():
    # 1) Yritä hakea mallin metadata (kevyt testi API-avaimelle)
    try:
        info = genai.get_model(MODEL)
        print("get_model onnistui. Mallin tiedot (rajattu):")
        # Tulosta tyypillisiä kenttiä, jos saat sellaisia
        try:
            print("name:", getattr(info, "name", info))
        except Exception:
            print(info)
        return 0
    except Exception as e:
        print("get_model epäonnistui:", repr(e))
        traceback.print_exc(limit=1)

    # 2) Jos get_model ei ole käytettävissä, listaa genai-attribuutit auttamaan debuggausta
    print("\ngenai - julkiset attribuutit (osittainen lista):")
    print(", ".join(x for x in dir(genai) if not x.startswith("_")))
    print("\nJos get_model ei löydy tai ei toimi, päivitä paketti:\n  pip install --upgrade google-generativeai google-ai-generativelanguage python-dotenv\n")
    return 1

if __name__ == "__main__":
    sys.exit(main())