from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_quizzes = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username
