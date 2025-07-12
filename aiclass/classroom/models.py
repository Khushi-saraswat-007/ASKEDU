from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Classroom  # or wherever your Classroom model is

class ClassRecording(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to="recordings/")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # ✅ Add this line


    def _str_(self):
        return self.title

class GeneratedNotes(models.Model):
    recording = models.ForeignKey(ClassRecording, on_delete=models.CASCADE)
    notes = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

class GeneratedQuiz(models.Model):
    recording = models.ForeignKey(ClassRecording, on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    answer = models.CharField(max_length=1)  # A, B, C, D

class ReExplanationRequest(models.Model):
    recording = models.ForeignKey(ClassRecording, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)