from django.shortcuts import render
import os
import json
import logging
import uuid
from .gemini_utils import generate_timeline
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

logging.basicConfig(level=logging.DEBUG)

DATA_FILE = os.path.join(settings.BASE_DIR, 'timeline', 'data', 'historical_events.json')

def load_historical_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for event in data.get("events", []):
            event.setdefault("id", str(uuid.uuid4()))
            event.setdefault("avatar", "📍")
            event.setdefault("coordinates", {"lat": 0.0, "lng": 0.0})
            event.setdefault("date", str(event.get("year", "Unknown")))
            event.setdefault("location", "Unknown")
            event.setdefault("significance", "")

        return data

    except FileNotFoundError:
        logging.error("Historical data file not found.")
        return {"events": []}
@login_required
# ✅ Homepage view
def index(request):
    data = load_historical_data()
    featured_timelines = data.get("timelines", [])[:3]

    get_started_steps = [
    {"icon": "search", "label": "Search", "text": "Enter any historical event …"},
    {"icon": "timeline", "label": "Explore", "text": "Browse interactive timelines …"},
    {"icon": "map", "label": "Discover", "text": "View locations on maps …"},
    ]


    # ✅ Instead of doing split in template, do it here
    suggestions = "French Revolution,Space Race,Renaissance,World War".split(",")

    return render(request, "timeline_index.html", {
        "query": None,
        "search_results": None,
        "featured_timelines": featured_timelines,
        "suggestions": suggestions,
        "get_started_steps": get_started_steps  
    })
@login_required
# ✅ Search view
def search(request):
    query = request.GET.get("q", "").strip()
    data = load_historical_data()
    events = data.get("events", [])
    timelines = data.get("timelines", [])

    if not query:
        return render(request, "timeline_index.html", {
            "query": query,
            "search_results": [],
            "error": "Please enter a search term.",
            "featured_timelines": []
        })

    # Search in both timelines and events
    search_results = []

    # Match from timeline titles or descriptions
    for t in timelines:
        if query.lower() in t["title"].lower() or query.lower() in t["description"].lower():
            t["id"] = t.get("id", "unknown")  # Ensure timeline has ID
            search_results.append(t)

    # Also match from events (optional)
    for e in events:
        if query.lower() in e["title"].lower() or query.lower() in e["description"].lower():
            # Attach timeline ID if missing
            e["id"] = e.get("timeline_id", "unknown")
            search_results.append(e)

    return render(request, "timeline_index.html", {
        "query": query,
        "search_results": search_results,
        "featured_timelines": []
    })
@login_required
# ✅ Timeline view (for a selected ID or POST-generated)
@csrf_exempt
def timeline_view(request, timeline_id=None):
    data = load_historical_data()
    events = data.get("events", [])
    
    if timeline_id:
        filtered = [e for e in events if str(e.get("timeline_id", "")) == timeline_id]
        timeline = next((t for t in data.get("timelines", []) if t["id"] == timeline_id), {})
        return render(request, "timeline.html", {
            "timeline": timeline,
            "events": filtered
        })

    # Gemini generation via POST (optional, like "create my own timeline")
    timeline = {}
    generated_events = []
    if request.method == "POST":
        topic = request.POST.get("topic", "")
        if topic:
            try:
                generated_events = generate_timeline(topic)
                timeline = {
                    "id": str(uuid.uuid4()),
                    "title": topic.title(),
                    "period": "Generated",
                    "description": f"A generated timeline for {topic}",
                    "location": "Various",
                    "category": "AI-generated",
                    "avatar": "🧠"
                }
            except Exception as e:
                generated_events = [{"title": "Error", "description": str(e)}]

    return render(request, "timeline.html", {
        "timeline": timeline,
        "events": generated_events
    })
