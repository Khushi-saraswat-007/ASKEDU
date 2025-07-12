from django.db import models
from django.contrib.auth.models import User

class EmotionLog(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # Attentive or Not Attentive
    meeting_id = models.IntegerField(null=True, blank=True)  # Add this line
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.status} at {self.timestamp}"
