from django.shortcuts import render, redirect, get_object_or_404
from .models import ClassRecording
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from .models import ClassRecording, GeneratedNotes, GeneratedQuiz, ReExplanationRequest
from django.utils import timezone
import markdown
import re
from .utils.audio_transcriber import extract_transcript_from_video
from .utils.audio_transcriber import extract_transcript_from_video
from .ai_utils import reexplain_with_gemini
from dashboard.models import Classroom , StudentClassroom

@login_required
def reexplain_recording(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)
    transcript = extract_transcript_from_video(recording.video.path)
    if not transcript:
        return HttpResponse("Transcript failed")

    explanation_md = reexplain_with_gemini(transcript)
    explanation_html = markdown.markdown(explanation_md)

    return render(request, 'classroom/reexplanation.html', {
        'recording': recording,
        'explanation': explanation_html,
    })

@login_required
def generate_notes(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)
    transcript = extract_transcript_from_video(recording.video.path)

    if transcript:
        ai_notes = generate_notes_with_gemini(transcript)
        GeneratedNotes.objects.create(recording=recording, notes=ai_notes)

    return redirect('student_dashboard')

@login_required
def teacher_dashboard(request):
    recordings = ClassRecording.objects.filter(uploaded_by=request.user)
    return render(request, 'classroom/teacher_dashboard.html', {'recordings': recordings})

@login_required
def upload_recording(request):
    classrooms = Classroom.objects.filter(teacher=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        video = request.FILES['video']
        classroom_id = request.POST.get('classroom')
        classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)

        ClassRecording.objects.create(
            title=title,
            video=video,
            uploaded_by=request.user,
            classroom=classroom
        )

        return redirect('teacher_dashboard')

    return render(request, 'classroom/upload.html', {
        'classrooms': classrooms
    })

@login_required
def delete_recording(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)
    if request.user != recording.uploaded_by:
        return HttpResponseForbidden("You're not allowed to delete this.")
    recording.delete()
    return redirect('teacher_dashboard')

@login_required
def student_dashboard(request):
    # ✅ Get classroom IDs the student has joined
    student_classrooms = StudentClassroom.objects.filter(student=request.user)
    classroom_ids = student_classrooms.values_list('classroom_id', flat=True)

    # ✅ Get only recordings from those classrooms
    recordings = ClassRecording.objects.filter(classroom_id__in=classroom_ids)

    return render(request, 'classroom/student_dashboard.html', {
        'recordings': recordings
    })

from .ai_utils import generate_notes_with_gemini, generate_quiz_with_gemini
import re

@login_required
def generate_quiz(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)

    transcript = extract_transcript_from_video(recording.video.path)
    if not transcript:
        print("❌ Transcription failed.")
        return redirect('student_dashboard')

    # Call Gemini
    ai_quiz_text = generate_quiz_with_gemini(transcript)

    cleaned_text = ai_quiz_text.replace("", "").strip()
    question_blocks = re.split(r'\n?\d+\.\s+', cleaned_text)[1:]

    saved_count = 0

    for block in question_blocks[:5]:  # Max 5 questions
        lines = block.strip().split("\n")

        if len(lines) < 2:
            print("⚠ Skipping block due to insufficient lines:", block)
            continue

        question = lines[0].strip()

        # Extract options
        option_lines = lines[1:5]
        options = []
        for line in option_lines:
            clean_option = re.sub(r'^[A-D][).]?\s*', '', line).strip()
            options.append(clean_option)

        # Fallback to ensure we have 4 options
        while len(options) < 4:
            options.append("N/A")

        # Extract answer
        answer_match = re.search(r'Answer:\s*([A-D])', block, re.IGNORECASE)
        answer = answer_match.group(1).upper() if answer_match else "A"

        # Save the question
        GeneratedQuiz.objects.create(
            recording=recording,
            question=question,
            option_a=options[0],
            option_b=options[1],
            option_c=options[2],
            option_d=options[3],
            answer=answer
        )
        saved_count += 1

    if saved_count == 0:
        print("❌ No quiz questions saved. Check Gemini output formatting.")

    return redirect('student_dashboard')

@login_required
def view_notes(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)
    notes_obj = GeneratedNotes.objects.filter(recording=recording).last()
    
    formatted_notes = markdown.markdown(notes_obj.notes) if notes_obj else None

    return render(request, 'classroom/view_notes.html', {
        'recording': recording,
        'notes': formatted_notes
    })

@login_required
def view_quiz(request, rec_id):
    recording = get_object_or_404(ClassRecording, id=rec_id)
    quiz_questions = GeneratedQuiz.objects.filter(recording=recording)
    return render(request, 'classroom/view_quiz.html', {
        'recording': recording,
        'questions': quiz_questions
    })