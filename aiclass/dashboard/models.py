from django.db import models
from django.contrib.auth.models import User

# ------------------ CLASSROOM MODEL ------------------

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return f"{self.name} ({self.code})"

# ------------------ STUDENT PROFILE ------------------

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

# ------------------ TEACHER PROFILE ------------------

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Teacher Profile"

# ------------------ MANUAL STUDENT ------------------

class ManualStudent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    classroom_name = models.CharField(max_length=255)  # ✅ extra string field

# ------------------ ATTENDANCE ------------------

class Attendance(models.Model):
    student = models.ForeignKey(ManualStudent, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # ✅ Add this line
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.classroom.name} - {self.date} - {self.status}"

# ------------------ BEHAVIOR NOTE ------------------

class BehaviorNote(models.Model):
    student = models.ForeignKey(ManualStudent, on_delete=models.CASCADE, related_name='behavior_notes')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True)  # ✅ newly added
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.student.name} in {self.classroom.name} by {self.teacher.username}"

# ------------------ SCHEDULED MEETING ------------------

# models.py
class ScheduledMeeting(models.Model):
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    join_url = models.URLField()  # ✅ Zoom link field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

# ------------------ ANNOUNCEMENT ------------------

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
class StudentClassroom(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'classroom')  # prevents duplicates

    def __str__(self):
        return f"{self.student.username} in {self.classroom.name}"
