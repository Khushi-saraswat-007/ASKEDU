from django.db import models
from django.contrib.auth.models import User

class PinnedTopic(models.Model):
    TONE_CHOICES = [
        ('chill', 'Chill'),
        ('strict', 'Strict'),
        ('cartoonie', 'Cartoonie'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_text = models.TextField()
    class_name = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assistant_response = models.TextField(blank=True, null=True)
    selected_tone = models.CharField(max_length=20, choices=TONE_CHOICES, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic_text[:30]}"
