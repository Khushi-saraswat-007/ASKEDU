from django.shortcuts import render, redirect
from .models import Student, Group, Teacher,  Notification, ChatMessage, StudySession, SessionProgress
import random
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


def home(request):
    return render(request, 'matchmaker/home.html')

def teacher_dashboard(request):
    teacher = Teacher.objects.first()  # or use logic to get the correct one
    return render(request, 'matchmaker/teacher_dashboard.html', {
        'teacher': teacher
    })

def teacher_progress_dashboard(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)

    # Show all sessions for now (ignoring teacher)
    sessions = StudySession.objects.all().order_by('-start_time')

    session_data = []
    for session in sessions:
        progresses = SessionProgress.objects.filter(session=session)
        session_data.append({
            'session': session,
            'group': session.group,
            'progress_list': progresses
        })

    return render(request, 'matchmaker/teacher_progress_dashboard.html', {
        'teacher': teacher,
        'session_data': session_data
    })


def form_groups(request):
    students = list(Student.objects.all())
    random.shuffle(students)

    groups = [students[i:i+4] for i in range(0, len(students), 4)]

    for group_students in groups:
        if len(group_students) >= 2:
            group = Group.objects.create(session_day="Monday")
            group.students.set(group_students)
            group.save()

            # Create a notification for each student in the group
            for student in group_students:
                Notification.objects.create(
                    user=student,
                    message="Your group has been created. Get ready to study on Monday!"
                )

    messages.success(request, "Groups have been formed and students notified!")
    return redirect('teacher_dashboard')


def student_groups(request, student_id):
    student = Student.objects.get(id=student_id)
    groups = student.group_set.all()
    notifications = Notification.objects.filter(user=student).order_by('-id')

    return render(request, 'matchmaker/student_groups.html', {
        'student': student,
        'groups': groups,
        'notifications': notifications
    })

def student_dashboard(request, student_id):
    student = Student.objects.get(id=student_id)
    groups = student.group_set.all()
    notifications = Notification.objects.filter(user=student, is_read=False).order_by('-timestamp')


    return render(request, 'matchmaker/student_dashboard.html', {
        'student': student,
        'groups': groups,
        'notifications': notifications
    })

def group_chat(request, group_id, student_id):
    group = Group.objects.get(id=group_id)
    student = Student.objects.get(id=student_id)

    session, created = StudySession.objects.get_or_create(
        group=group,
        defaults={
            'scheduled_time': timezone.now().time(),
            'start_time': timezone.now(),
            'is_active': True
        }
    )

    # ✅ Important: Get chat messages from this session only
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')

    return render(request, 'matchmaker/group_chat.html', {
        'group': group,
        'student': student,
        'session': session,
        'messages': messages,
        'now': timezone.now()
    })




@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        student_id = request.POST.get('student_id')
        message_text = request.POST.get('message', '')

        image = request.FILES.get('image')
        voice = request.FILES.get('voice')  # ✅ NEW

        try:
            session = StudySession.objects.get(group_id=group_id)
            student = Student.objects.get(id=student_id)

            ChatMessage.objects.create(
                session=session,
                sender=student,
                message_text=message_text,
                image=image,
                voice=voice
            )

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def submit_progress(request, session_id, student_id):
    session = StudySession.objects.get(id=session_id)
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        topics = request.POST.get('topics')
        time_spent = request.POST.get('time_spent_minutes')
        questions = request.POST.get('questions_solved')
        rating = request.POST.get('self_rating')
        notes = request.POST.get('notes')

        SessionProgress.objects.create(
            session=session,
            student=student,
            topics=topics,
            time_spent_minutes=time_spent,
            questions_solved=questions,
            self_rating=rating,
            notes=notes
        )
        return redirect('group_chat', group_id=session.group.id, student_id=student.id)

    return render(request, 'matchmaker/progress_form.html', {
        'session': session,
        'student': student
    })

