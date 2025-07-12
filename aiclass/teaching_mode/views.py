
# Create your views here.
import google.generativeai as genai
import markdown
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyC2jQCHiZV4DSq2oYbgWtxYblxOYMFVLoU"))
model = genai.GenerativeModel("gemini-1.5-flash")
@login_required
def index(request):
    return render(request, "teaching_mode/index.html")
@login_required
@csrf_exempt
def evaluate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        topic = data.get("topic", "")
        explanation = data.get("explanation", "")
        standard = data.get("standard", "Grade 8")

        prompt = f"""
You are a supportive tutor helping a Grade {standard} student understand the topic: **{topic}**.

They explained it like this:
"{explanation}"

Give feedback in this format (always use **you** to talk to the student directly):

1. **Positive Feedback:** Start with encouragement. Point out anything the student explained correctly or made a good effort on. Be warm, personal, and direct — use phrases like "You explained...", "I like how you...".

2. **Gaps in Understanding:** Even if their explanation is good, explain what they missed using simple language. Use clear bullets and **bold key terms** to make it easy to learn. Always give at least 2–3 teaching points — don’t skip this section.
        """

        print("Prompt sent to Gemini:", prompt)
        response = model.generate_content(prompt)
        parts = response.text.split("2.")
        positive = markdown.markdown(parts[0].replace("1.", "").strip())
        gaps = markdown.markdown(parts[1]) if len(parts) > 1 else markdown.markdown("No major gaps provided.")

        return JsonResponse({
            "positive": positive,
            "gaps": gaps
        })
    return JsonResponse({"error": "Invalid request"}, status=400)
