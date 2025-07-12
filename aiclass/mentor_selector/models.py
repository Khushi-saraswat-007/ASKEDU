
from django.db import models
from django.utils import timezone


class ChatHistory(models.Model): 
    mentor_type = models.CharField(max_length=20, default='strict')
    session_id = models.CharField(max_length=100, default='default-session')  # Unique session or chat name

    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mentor_type} - {self.session_id[:6]} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"



class ChatSession(models.Model):
    mentor = models.CharField(max_length=50)
    session_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentor} - {self.session_name}"


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10)  # 'user' or 'mentor'
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} at {self.timestamp}"
