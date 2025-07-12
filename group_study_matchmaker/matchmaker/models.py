from django.db import models
from django.utils import timezone
from datetime import timedelta


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    strengths = models.JSONField(default=dict)  # e.g., {'Math': 'Strong', 'Physics': 'Weak'}
    weaknesses = models.JSONField(default=dict)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    students = models.ManyToManyField(Student)
    created_at = models.DateTimeField(auto_now_add=True)
    session_day = models.CharField(max_length=20)  # e.g., "Monday"
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name




class StudySession(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    scheduled_time = models.TimeField()
    start_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    @property
    def end_time(self):
        return self.start_time + timedelta(hours=1)



class ChatMessage(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    message_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    voice = models.FileField(upload_to='chat_voices/', blank=True, null=True)  # ✅ NEW
    timestamp = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)


class SessionProgress(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topics = models.TextField()
    time_spent_minutes = models.IntegerField()
    questions_solved = models.IntegerField()
    self_rating = models.IntegerField()  # out of 5
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.session}"


