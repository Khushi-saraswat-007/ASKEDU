from django.contrib import admin
from .models import ClassRecording, GeneratedNotes, GeneratedQuiz, ReExplanationRequest

admin.site.register(ClassRecording)
admin.site.register(GeneratedNotes)
admin.site.register(GeneratedQuiz)
admin.site.register(ReExplanationRequest)
