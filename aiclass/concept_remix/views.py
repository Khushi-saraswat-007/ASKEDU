
# Create your views here.
import os
import re
from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("AIzaSyCVZ9oXr-m70AZ7LO_1D1EMNiLsfBYlDOg")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def clean_output(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # remove bold markdown
    text = re.sub(r'\* (Image:|image:)\*', '', text, flags=re.IGNORECASE)
    return text.strip()

def index(request):
    remix = None
    concept = ""
    format_type = ""

    if request.method == "POST":
        concept = request.POST.get("concept", "").strip()
        format_type = request.POST.get("format", "").strip()

        if concept and format_type:
            prompt_map = {
                "poem": f"Write a short educational poem about {concept} in a fun and engaging way.",
                "song": f"Turn the concept of {concept} into a short, catchy educational rap or song lyrics.",
                "meme": f"Create a humorous meme-style caption or joke about {concept}.",
                "comic": f"Describe a short comic strip idea (in 3 panels) that explains {concept} in a fun way."
            }
            prompt = prompt_map.get(format_type, f"Explain the concept of {concept} in an engaging way.")
            try:
                response = model.generate_content(prompt)
                remix = clean_output(response.text)
            except Exception as e:
                remix = f"❌ Error: {e}"

    return render(request, "concept_remix/indexx.html", {
        "remix": remix,
        "concept": concept,
        "format_type": format_type,
    })
