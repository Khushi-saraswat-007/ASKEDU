from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

from .models import EmotionLog

# ✅ Renders the Emotion Tracker page (with optional meeting_id)
@login_required
def emotion_tracker(request, meeting_id=None):
    student_name = request.user.username
    return render(request, 'emotiontracker/emotion_tracker.html', {
        'student_name': student_name,
        'meeting_id': meeting_id
    })

# ✅ Logs attentiveness sent via JavaScript
@csrf_exempt
def process_emotion(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        attentive = data.get('attentive', True)
        meeting_id = data.get('meeting_id')
        student_name = data.get('student_name')
        timestamp = data.get('timestamp')

        try:
            student = User.objects.get(username=student_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=400)

        EmotionLog.objects.create(
            student=student,
            status="Attentive" if attentive else "Not Attentive",
            meeting_id=meeting_id,
            timestamp=timestamp
        )

        return JsonResponse({'message': 'Logged successfully'})