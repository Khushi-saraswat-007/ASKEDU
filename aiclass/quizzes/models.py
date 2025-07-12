from django.db import models
from accounts.models import Student

class Quiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    num_questions = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - {self.topic}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    options = models.JSONField()  # options = {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer = models.CharField(max_length=100)
    explanation = models.TextField()
    selected_answer = models.CharField(max_length=100, blank=True, null=True)

    def is_correct(self):
        return self.selected_answer == self.correct_answer


