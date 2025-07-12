import os
import google.generativeai as genai
import uuid
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Configure Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "PUT-YOUR-API-KEY-HERE"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_timeline(query):
    prompt = f"""
You are a historical expert. Generate a JSON object for the historical event: "{query}".
Return this format:

{{
  "timeline": {{
    "id": "short-id",
    "title": "Event Title",
    "description": "Short description",
    "period": "YYYY–YYYY",
    "image": "https://example.com/image.jpg",
    "category": "war/politics/etc",
    "location": "Location Name",
    "coordinates": {{ "lat": 0.0, "lng": 0.0 }},
    "avatar": "🌍",
    "color": "#17B169"
  }},
  "events": [
    {{
      "timeline_id": "short-id",
      "year": "YYYY",
      "title": "Sub-event Title",
      "description": "Details"
    }}
  ]
}}
Only return valid JSON. No markdown or explanation.
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Log raw Gemini response
        logger.info("Gemini raw response:\n" + raw)

        # Remove markdown wrappers
        if raw.startswith(""):
            raw = raw.split("json")[-1].split("```" )[0].strip()

        data = json.loads(raw)

        # Patch timeline ID
        timeline_id = str(uuid.uuid4())
        data["timeline"]["id"] = timeline_id

        # Default timeline fields
        timeline_defaults = {
            "avatar": "🕰",
            "category": "general",
            "location": "Unknown",
            "coordinates": {"lat": 0.0, "lng": 0.0},
            "period": "Unknown Period",
            "description": "No description provided.",
            "image": "",
            "color": "#666"
        }
        for key, default in timeline_defaults.items():
            data["timeline"].setdefault(key, default)

        # Patch events
        for e in data["events"]:
            e["timeline_id"] = timeline_id
            e.setdefault("title", "Untitled Event")
            e.setdefault("year", "Unknown Year")
            e.setdefault("description", "No description provided.")
            e.setdefault("location", data["timeline"]["location"])
            e.setdefault("significance", "")
            e.setdefault("avatar", data["timeline"]["avatar"])
            e.setdefault("coordinates", data["timeline"]["coordinates"])
            e.setdefault("date", e["year"])

        return data

    except Exception as e:
        logger.error("Error parsing Gemini response: " + str(e))
        return None