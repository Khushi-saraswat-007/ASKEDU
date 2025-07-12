from django.urls import path
from . import views

urlpatterns = [
    path('emotion-tracker/', views.emotion_tracker, name='emotion_tracker'),
    path('process_emotion/', views.process_emotion, name='process_emotion'),
    path('feature/emotion-detection/<int:meeting_id>/', views.emotion_tracker, name='student_zoom_with_tracker'),
]
