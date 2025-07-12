import re
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("API key not found. Check .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_mcq(subject, topic, num_questions=5):
    prompt = f"""
    Generate {num_questions} MCQs on the topic "{topic}" under the subject "{subject}".

    Each question should have:
    - 4 options (A to D)
    - clearly correct answer
    - explanation

    Return ONLY valid JSON inside triple backticks like this:

    ```json
    [
      {{
        "question": "...",
        "options": {{
          "A": "...",
          "B": "...",
          "C": "...",
          "D": "..."
        }},
        "answer": "A",
        "explanation": "..."
      }},
      ...
    ]
    ```
    """

    response = model.generate_content(prompt)

    # print("\n🔍 RAW GEMINI OUTPUT:\n", response.text)

    # ✅ Extract JSON block from backticks
    try:
        # Remove Markdown ```json ... ```
        json_block = re.search(r"```json\s*(.*?)```", response.text, re.DOTALL).group(1)
        json_data = json.loads(json_block)
        return json_data
    except Exception as e:
        print("❌ Error parsing Gemini JSON:", e)
        return None
