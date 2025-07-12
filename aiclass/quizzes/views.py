from django.shortcuts import render, redirect
from django.utils import timezone
from .services.ai import generate_mcq
from .models import Quiz, Question
from accounts.models import Student
import datetime
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.contrib.auth.models import User
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json
@login_required
def home(request):
    return render(request, 'home.html')

generated_quiz = []  # Global temp cache for quiz questions
@login_required
def quiz_start(request):
    subjects = ["Math", "Physics", "Biology", "Chemistry", "Geography"]
    return render(request, 'quizzes/quiz_start.html', {'subjects': subjects})
@login_required
def quiz_view(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        custom_subject = request.POST.get('custom_subject')

        if subject == "Other" and custom_subject:
            subject = custom_subject.strip()

        topic = request.POST['topic']
        num = int(request.POST['num_questions'])

        global generated_quiz

        try:
            generated_quiz = generate_mcq(subject, topic, num)
        except json.JSONDecodeError as e:
            print("❌ JSON decode error in generate_mcq():", e)
            generated_quiz = None
        except Exception as e:
            print("❌ Unexpected error in generate_mcq():", e)
            generated_quiz = None

        if not generated_quiz:
            return render(request, 'quizzes/quiz_start.html', {
                'error': "Could not generate quiz. Try again.",
                'subjects': ["Math", "Physics", "Biology", "Chemistry", "Geography"]
            })

        request.session['start_time'] = str(datetime.datetime.now())
        request.session['subject'] = subject
        request.session['topic'] = topic
        request.session['num'] = num

        return render(request, 'quizzes/quiz.html', {
            'questions': generated_quiz,
            'num': num,
            'time_limit': num * 60
        })

    return redirect('quiz_start')

@login_required
def submit_quiz(request):
    if request.method == 'POST':
        end_time = datetime.datetime.now()
        start_time = datetime.datetime.fromisoformat(request.session['start_time'])

        student, created = Student.objects.get_or_create(user=request.user)

        global generated_quiz
        score = 0
        total = len(generated_quiz)

        for i, q in enumerate(generated_quiz):
            selected = request.POST.get(f'q{i}')
            generated_quiz[i]['selected'] = selected
            if selected == q['answer']:
                score += 1

        accuracy = (score / total) * 100
        time_taken = (end_time - start_time).total_seconds()
        time_factor = 1 - min(time_taken / (total * 60), 1)
        rating = round(((score / total) * 0.5 + (accuracy / 100) * 0.3 + time_factor * 0.2) * 10, 2)

        quiz = Quiz.objects.create(
            student=student,
            subject=request.session['subject'],
            topic=request.session['topic'],
            difficulty='Normal',
            num_questions=total,
            start_time=start_time,
            end_time=end_time,
            score=score,
            rating=rating
        )

        for q in generated_quiz:
            Question.objects.create(
                quiz=quiz,
                question_text=q['question'],
                options=q['options'],
                correct_answer=q['answer'],
                explanation=q['explanation'],
                selected_answer=q.get('selected', '')
            )

        request.session['results'] = {
            'score': score,
            'total': total,
            'accuracy': round(accuracy, 2),
            'time_taken': int(time_taken),
            'rating': rating
        }

        return redirect('quiz_result')

    return redirect('quiz_start')
@login_required
def quiz_result(request):
    result = request.session.get('results', {})
    global generated_quiz
    return render(request, 'quizzes/quiz_result.html', {
        'result': result,
        'questions': generated_quiz
    })

@login_required
def student_dashboard(request):
    student, created = Student.objects.get_or_create(user=request.user)
    quizzes = Quiz.objects.filter(student=student).order_by('-end_time')

    topic_stats = {}
    for quiz in quizzes:
        key = (quiz.subject, quiz.topic)
        if key not in topic_stats:
            topic_stats[key] = {'count': 0, 'total_rating': 0}
        topic_stats[key]['count'] += 1
        topic_stats[key]['total_rating'] += quiz.rating

    topic_analysis = []
    ai_suggestions = []
    for (subject, topic), stats in topic_stats.items():
        avg_rating = round(stats['total_rating'] / stats['count'], 2)
        is_weak = avg_rating < 6.0
        topic_analysis.append({
            'subject': subject,
            'topic': topic,
            'attempts': stats['count'],
            'avg_rating': avg_rating,
            'weak': is_weak
        })
        if is_weak:
            ai_suggestions.append(
                f"📌 You should revisit *{topic}* in *{subject}*. Practice more and revise notes."
            )

    labels = [f"{item['subject']} - {item['topic']}" for item in topic_analysis]
    scores = [item['avg_rating'] * 10 for item in topic_analysis]

    return render(request, 'quizzes/quiz_dashboard.html', {
        'quizzes': quizzes,
        'topic_analysis': topic_analysis,
        'labels': labels,
        'scores': scores,
        'ai_suggestions': ai_suggestions
    })

@login_required
def generate_pdf_result(request):
    result = request.session.get('results', {})
    global generated_quiz

    template = get_template("quizzes/pdf_result_template.html")
    html = template.render({"result": result, "questions": generated_quiz})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="quiz_result.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF")

    return response

@login_required
def quiz_history(request):
    student, created = Student.objects.get_or_create(user=request.user)
    quizzes = Quiz.objects.filter(student=student).order_by('-end_time')

    return render(request, 'quizzes/quiz_history.html', {
        'quizzes': quizzes
    })

@login_required
def leaderboard_view(request):
    subject = request.GET.get('subject')

    if subject:
        leaderboard = (
            Quiz.objects.filter(subject=subject)
            .values('student__user__username')
            .annotate(
                avg_rating=Avg('rating'),
                avg_score=Avg('score'),
                total_quizzes=Count('id')
            )
            .order_by('-avg_rating')[:10]
        )
    else:
        leaderboard = (
            Quiz.objects.all()
            .values('student__user__username')
            .annotate(
                avg_rating=Avg('rating'),
                avg_score=Avg('score'),
                total_quizzes=Count('id')
            )
            .order_by('-avg_rating')[:10]
        )

    subjects = Quiz.objects.values_list('subject', flat=True).distinct()

    return render(request, 'quizzes/leaderboard.html', {
        'leaderboard': leaderboard,
        'subjects': subjects,
        'selected_subject': subject
    })

@login_required
def generate_smart_pdf(request):
    result = request.session.get('results', {})
    global generated_quiz

    score = result.get('score', 0)
    total = result.get('total', 1)
    accuracy = result.get('accuracy', 0)
    time_taken = result.get('time_taken', 0)

    labels = ['Score', 'Accuracy', 'Time Taken (s)']
    values = [score, accuracy, time_taken]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'blue', 'orange'])
    ax.set_ylim(0, max(values) + 10)
    ax.set_title('Quiz Performance Summary')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    chart_url = f"data:image/png;base64,{image_base64}"
    plt.close()

    suggestions = []
    for q in generated_quiz:
        if q.get('selected') != q['answer']:
            suggestions.append(f"❌ *{q['question']}* → Review this concept again. Correct: **{q['answer']}**")

    template = get_template("quizzes/smart_pdf_template.html")
    html = template.render({
        "result": result,
        "questions": generated_quiz,
        "chart_url": chart_url,
        "suggestions": suggestions
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="smart_report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("PDF generation failed")
    return response
