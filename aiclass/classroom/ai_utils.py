import google.generativeai as genai
from django.conf import settings

genai.configure(api_key="YOUR_API_KEY")  # <-- ideally use env var

gemini = genai.GenerativeModel("gemini-1.5-flash")


genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_notes_with_gemini(prompt_text):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(f"Give well-organized study notes based on this class: {prompt_text}")
    return response.text

def generate_quiz_with_gemini(prompt_text):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(
        f"Generate 5 MCQs with 4 options (A-D) and correct answer marked separately based on this class: {prompt_text}"
    )
    return response.text

def reexplain_with_gemini(transcript):
    prompt = f"""
You are a helpful teacher assistant. The student didn't understand this lecture:

\"\"\"
{transcript}
\"\"\"

Please re-explain it in **simple language**, **step-by-step**, using clear **headings**, **bullet points**, and **examples** in **Markdown format**.

Start with:
## Re-explained Lecture: [Topic Title or Auto-Detect]

Then break it down clearly.
"""

    response = gemini.generate_content(prompt)
    return response.text
