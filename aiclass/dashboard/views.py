import base64
import csv
import requests
from datetime import datetime, date
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from .models import Classroom, StudentClassroom
from django.contrib import messages

import json
import random, string
from django.shortcuts import render
from .models import StudentProfile, Classroom, ScheduledMeeting, Announcement

from .models import (
    ManualStudent,
    StudentProfile,
    BehaviorNote,
    Attendance,
    ScheduledMeeting,
    Announcement,
    TeacherProfile,
    Classroom
)
from django.contrib.auth.models import User
from django.urls import reverse

@login_required
def edit_manual_student(request, student_id):
    student = get_object_or_404(ManualStudent, id=student_id, added_by=request.user)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.roll_number = request.POST.get('roll_number')
        student.course = request.POST.get('course')
        student.save()
        return redirect(f"{reverse('manual_student_list')}?classroom={student.classroom.id}")

    return render(request, 'edit_manual_student.html', {'student': student})


@login_required
def delete_manual_student(request, student_id):
    student = get_object_or_404(ManualStudent, id=student_id, added_by=request.user)
    classroom_id = student.classroom.id
    student.delete()
    return redirect(f"{reverse('manual_student_list')}?classroom={classroom_id}")

# -- Classroom Join/Create --

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_classroom(request):
    if request.method == "POST":
        name = request.POST['name']
        code = generate_code()
        teacher = request.user
        Classroom.objects.create(name=name, code=code, teacher=teacher)
        return redirect('teachersdashboard')
    return render(request, 'create_classroom.html')

@login_required
def join_classroom(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            classroom = Classroom.objects.get(code=code)
            StudentClassroom.objects.get_or_create(student=request.user, classroom=classroom)
            return redirect('studentdashboard')
        except Classroom.DoesNotExist:
            messages.error(request, 'Invalid classroom code.')

    return render(request, 'join_classroom.html')

# -- Gemini Chatbot --
genai.configure(api_key="YOUR_API_KEY")


@csrf_exempt
@login_required
def update_user_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')

        user = request.user
        if name:
            user.username = name
            user.first_name = name
        if email:
            user.email = email
        user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


@login_required
def start_live_class(request):
    access_token = request.session.get('zoom_access_token')
    if not access_token:
        return redirect('zoom_login')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        headers=headers,
        json={"topic": "Live Class", "type": 1}
    )
    data = response.json()
    if 'join_url' in data:
        return redirect(data['join_url'])
    return render(request, 'error.html', {'message': 'Failed to create Zoom meeting.'})
@login_required
def delete_meeting(request, meeting_id):
    meeting = get_object_or_404(ScheduledMeeting, id=meeting_id, created_by=request.user)
    if request.method == 'POST':
        meeting.delete()
        return redirect('teachersdashboard')
    return redirect('teachersdashboard')

@login_required
def schedule_meeting(request):
    classrooms = Classroom.objects.filter(teacher=request.user)

    if request.method == 'POST':
        topic = request.POST.get('topic')
        start_time = request.POST.get('start_time')
        join_url = request.POST.get('join_url')
        classroom_id = request.POST.get('classroom_id')

        if not (topic and start_time and join_url and classroom_id):
            return render(request, 'schedule_meeting.html', {'error': 'All fields required.', 'classrooms': classrooms})

        classroom = Classroom.objects.get(id=classroom_id)

        ScheduledMeeting.objects.create(
            topic=topic,
            start_time=start_time,
            join_url=join_url,
            created_by=request.user,
            classroom=classroom
        )
        return redirect('teachersdashboard')

    return render(request, 'schedule_meeting.html', {'classrooms': classrooms})

# -- Dashboards --
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import ScheduledMeeting, Announcement, Classroom



@login_required
def dashboard(request):
    classrooms = Classroom.objects.filter(teacher=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        classroom_id = request.POST.get('classroom_id')

        if title and message and classroom_id:
            classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
            Announcement.objects.create(
                title=title,
                message=message,
                created_by=request.user,
                classroom=classroom
            )
            return redirect('teachersdashboard')

    # ✅ Only fetch meetings whose start time is in the future
    now = timezone.now()
    upcoming_meetings = ScheduledMeeting.objects.filter(
        created_by=request.user,
        start_time__gte=now
    ).order_by('start_time')

    # ✅ This will ensure no past meetings are shown on the green button
    next_meeting = upcoming_meetings.first() if upcoming_meetings.exists() else None

    announcements = Announcement.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'meetings': upcoming_meetings,     # shown in "Upcoming" box
        'next_meeting': next_meeting,      # shown in the green button
        'announcements': announcements,
        'classrooms': classrooms
    })





@login_required
def teacher_profile_view(request):
    profile, created = TeacherProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.emergency_contact_name = request.POST.get('emergency_contact_name')
        profile.emergency_contact_number = request.POST.get('emergency_contact_number')
        profile.emergency_contact_relation = request.POST.get('emergency_contact_relation')
        profile.bio = request.POST.get('bio')
        profile.save()
        return redirect('teacher_profile')

    return render(request, 'teacher_profile.html', {'profile': profile, 'user': request.user})

@login_required
def profile_view(request):
    firebase_email = request.POST.get('firebase_email') if request.method == 'POST' else request.user.email

    user = get_object_or_404(User, email=firebase_email)
    profile, created = StudentProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.emergency_contact_name = request.POST.get('emergency_contact_name')
        profile.emergency_contact_number = request.POST.get('emergency_contact_number')
        profile.emergency_contact_relation = request.POST.get('emergency_contact_relation')
        profile.bio = request.POST.get('bio')
        profile.interests = request.POST.get('interests')
        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile, 'user': user})
@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.message = request.POST.get('message')
        announcement.save()
        return redirect('teachersdashboard')
    return render(request, 'edit_announcement.html', {'announcement': announcement})

@login_required
def behavior_notes_view(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    selected_classroom_id = request.GET.get('classroom')
    notes = []
    students = []

    if selected_classroom_id:
        students = ManualStudent.objects.filter(classroom_id=selected_classroom_id, added_by=request.user)
        notes = BehaviorNote.objects.filter(classroom_id=selected_classroom_id, teacher=request.user).order_by('-created_at')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        note_text = request.POST.get('note')
        classroom_id = request.POST.get('classroom_id')

        if student_id and note_text and classroom_id:
            student = get_object_or_404(ManualStudent, id=student_id, classroom_id=classroom_id)
            BehaviorNote.objects.create(
                student=student,
                teacher=request.user,
                note=note_text,
                classroom=student.classroom  # ✅ store classroom too
            )
            return redirect(f"{reverse('behavior_notes')}?classroom={classroom_id}")

    return render(request, 'behavior_notes.html', {
        'notes': notes,
        'students': students,
        'classrooms': classrooms,
        'selected_classroom_id': selected_classroom_id
    })


@login_required
def edit_behavior_note(request, note_id):
    note = get_object_or_404(BehaviorNote, id=note_id)
    if request.method == 'POST':
        note.note = request.POST.get('note')
        note.save()
        return redirect('behavior_notes')
    return render(request, 'edit_behavior_note.html', {'note': note})
@login_required
def delete_behavior_note(request, note_id):
    note = get_object_or_404(BehaviorNote, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('behavior_notes')
    return render(request, 'delete_behavior_note.html', {'note': note})
from django.shortcuts import render, redirect
from .models import ManualStudent, Classroom
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import ManualStudent, Classroom
from django.contrib.auth.decorators import login_required

@login_required
def manual_student_list(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    selected_classroom_id = request.GET.get('classroom')
    students = []

    if selected_classroom_id:
        students = ManualStudent.objects.filter(classroom_id=selected_classroom_id, added_by=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        roll_number = request.POST.get('roll_number')
        course = request.POST.get('course')
        classroom_id = request.POST.get('classroom')

        if name and classroom_id:
            classroom = get_object_or_404(Classroom, id=classroom_id)
            ManualStudent.objects.create(
                name=name,
                email=email,
                roll_number=roll_number,
                course=course,
                added_by=request.user,
                classroom=classroom,              # ✅ saves classroom FK
                classroom_name=classroom.name     # ✅ saves classroom name string
            )
            return redirect(f'/manual-students/?classroom={classroom_id}')

    return render(request, 'manual_student_list.html', {
        'classrooms': classrooms,
        'students': students,
        'selected_classroom_id': selected_classroom_id
    })


@login_required
def attendance_view(request):
    # Get classrooms for logged-in teacher
    classrooms = Classroom.objects.filter(teacher=request.user)
    selected_classroom_id = request.GET.get('classroom')
    students = []

    if selected_classroom_id:
        # Get students for selected classroom added by the teacher
        students = ManualStudent.objects.filter(
            classroom_id=selected_classroom_id,
            added_by=request.user
        ).order_by('name')

    if request.method == 'POST':
        # Get date and classroom_id from hidden inputs
        date_str = request.POST.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        classroom_id = request.POST.get('classroom_id')

        if classroom_id:
            classroom = get_object_or_404(Classroom, id=classroom_id)
            for student in students:
                status = request.POST.get(f'status_{student.id}')
                if status:  # Only save if status is selected
                    Attendance.objects.update_or_create(
                        student=student,
                        date=date_obj,
                        classroom=classroom,  # Important: include classroom here
                        defaults={
                            'status': status,
                            'marked_by': request.user,
                        }
                    )
            # Redirect back to attendance page for selected classroom
            return redirect(f"{reverse('attendance')}?classroom={classroom_id}")

    return render(request, 'attendance.html', {
        'classrooms': classrooms,
        'students': students,
        'selected_classroom_id': selected_classroom_id,
        'today_date': date.today().strftime('%Y-%m-%d'),  # Pass today’s date to template
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ManualStudent, Attendance

@login_required
def attendance_history(request):
    classrooms = Classroom.objects.filter(teacher=request.user)
    selected_classroom_id = request.GET.get('classroom')
    selected_student_id = request.GET.get('student_id')
    students = []
    attendance_records = []

    if selected_classroom_id:
        students = ManualStudent.objects.filter(
            classroom_id=selected_classroom_id,
            added_by=request.user
        ).order_by('name')

    if selected_student_id:
        selected_student = get_object_or_404(ManualStudent, id=selected_student_id)
        attendance_records = Attendance.objects.filter(student=selected_student).order_by('-date')

    return render(request, 'attendance_history.html', {
        'classrooms': classrooms,
        'students': students,
        'selected_classroom_id': selected_classroom_id,
        'selected_student_id': selected_student_id,
        'attendance_records': attendance_records,
    })

@login_required
def attendance_csv_export(request):
    student_id = request.GET.get('student_id')
    if student_id:
        student = get_object_or_404(ManualStudent, id=student_id)
        attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    else:
        attendance_records = Attendance.objects.all().order_by('-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Status', 'Marked By'])
    for record in attendance_records:
        writer.writerow([record.date, record.status, record.marked_by.username])

    return response


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StudentProfile, StudentClassroom, ScheduledMeeting, Announcement

@login_required
def studentdashboard(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)

        classroom_links = StudentClassroom.objects.filter(student=request.user).select_related('classroom')
        classrooms = [entry.classroom for entry in classroom_links]

        meetings = ScheduledMeeting.objects.filter(classroom__in=classrooms).order_by('start_time') if classrooms else []
        announcements = Announcement.objects.filter(classroom__in=classrooms).order_by('-created_at') if classrooms else []

        return render(request, 'testdashboard.html', {
            'classrooms': classrooms,
            'meetings': meetings,
            'announcements': announcements
        })

    except StudentProfile.DoesNotExist:
        # If no profile exists, show dashboard with no data
        return render(request, 'testdashboard.html', {
            'classrooms': [],
            'meetings': [],
            'announcements': []
        })

# File: aiclass/dashboard/views.py
def index(request):
    return render(request, 'animation.html')
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

def loginpage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') or reverse('dashboard'))
        else:
            return render(request, "login1.html", {"error": "Invalid credentials"})

    return render(request, "login1.html")

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def firebase_login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name', 'User')  # optional name

        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)

        # Get or create the user
        user, created = User.objects.get_or_create(username=email, defaults={
            'email': email,
            'first_name': name
        })

        # Log the user in (no password needed for Firebase)
        login(request, user)
        return JsonResponse({'status': 'logged_in'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, created_by=request.user)
    if request.method == 'POST':
        announcement.delete()
        return redirect('teachersdashboard') 
    return redirect('teachersdashboard')
