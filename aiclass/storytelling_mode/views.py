import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import google.generativeai as genai
from .models import Story
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# ✅ Gemini API setup
genai.configure(api_key="AIzaSyCBTCRq185mrf4e6yZKktBoLKL-JG042dc")
@login_required
def storytelling_home(request):
    return render(request, 'storytelling.html')
@login_required
@csrf_exempt
def generate_story_with_audio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic')
            age = data.get('age')
            tone = data.get('tone', 'neutral')

            print("Incoming:", topic, age, tone)

            tone_text = f" Make the story {tone.lower()} in tone." if tone and tone.lower() != "random" else ""
            prompt = f"Write a short story for a {age}-year-old about '{topic}'.{tone_text}"

            # ✅ Generate story
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(prompt)
            story = response.text.strip()
            print("Generated Story:", story)

            # ✅ Save to DB (assign a user — replace with real login system later)
            user = request.user if request.user.is_authenticated else User.objects.first()  # fallback for testing
            Story.objects.create(user=user, topic=topic, age=age, content=story)
            print("✅ Story saved to DB")

            # ✅ Convert to audio
            tts = gTTS(text=story, lang='en')
            audio_filename = f"audio_{topic.replace(' ', '_')}.mp3"
            audio_path = os.path.join("media", audio_filename)
            tts.save(audio_path)

            return JsonResponse({
                'story': story,
                'audio_url': f"/media/{audio_filename}"
            })

        except Exception as e:
            print("❌ Error occurred:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
@login_required
def my_stories_view(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'mystories.html', {'stories': stories})
@login_required
@csrf_exempt
def delete_story(request, story_id):
    if request.method == 'POST':
        Story.objects.filter(id=story_id).delete()
        return redirect('my_stories')
