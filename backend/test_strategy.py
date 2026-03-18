import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.services.strategy import generate_strategic_response

result = generate_strategic_response(
    "Zomato", "Swiggy",
    {"sentiment": 65.0, "growth": 45.0, "risk": 0.15},
    {"sentiment": 55.0, "growth": 50.0, "risk": 0.20},
    "What are the key risks?",
    ["Customer Rating", "Review Length"]
)

print("Response:")
print(result)
print()
print("Is Gemini response (contains specific numbers):", "Zomato" in result and "65" in result)
