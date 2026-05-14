import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.services.gemini_langchain import gemini_generate_text

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print("API Key loaded:", api_key is not None)

try:
    text = gemini_generate_text("say hi", api_key=api_key)
    print(text)
except Exception:
    import traceback

    traceback.print_exc()
