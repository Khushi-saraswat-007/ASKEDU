import os
import google.generativeai as genai
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Set your Gemini API key
genai.configure(api_key="AIzaSyB3T9SHbvJY_gNp6BoELoYmsGzUOoXZm0U")
model = genai.GenerativeModel("gemini-1.5-flash")
@login_required
def generate_visual(request):
    topic = ""
    visual_type = ""
    output = ""

    if request.method == "POST":
        topic = request.POST.get("topic")
        visual_type = request.POST.get("visual_type")

        if topic and visual_type:
            prompt = f"""Generate a Mermaid.js diagram for the following:
Topic: {topic}
Visual Type: {visual_type}

Please give only valid Mermaid syntax inside triple backticks like ```mermaid ... ``` without any extra explanation."""

            try:
                response = model.generate_content(prompt)
                content = response.text

                # Extract Mermaid code block
                if "```mermaid" in content:
                    output = content.split("```mermaid")[1].split("```")[0].strip()
                else:
                    output = "Unable to generate Mermaid diagram. Please try a different topic."

            except Exception as e:
                output = f"Error: {str(e)}"

    return render(request, "visualaid.html", {
        "topic": topic,
        "visual_type": visual_type,
        "output": output,
    })
