
from django.db import models

from django.db import models

class Chat(models.Model):
    user_prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)  # 👈 Add this

