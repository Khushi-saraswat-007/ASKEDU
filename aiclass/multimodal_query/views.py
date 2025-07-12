from django.shortcuts import render

# Create your views here.
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import whisper
from django.core.files.storage import default_storage
from PIL import Image
from django.contrib.auth.decorators import login_required

def clean_output(text):
    # Remove asterisks and extra markdown
    return re.sub(r'\*+', '', text).strip()

import base64
from PIL import Image
from io import BytesIO
import tempfile
import subprocess
@login_required
def webcam_view(request):
    result = None
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        audio_data = request.POST.get('audio_data')

        # Decode image
        image_str = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_str)
        image = Image.open(BytesIO(image_bytes))

        # Decode and save audio
        audio_bytes = base64.b64decode(audio_data)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
            audio_file.write(audio_bytes)
            audio_path = audio_file.name

        # Speech-to-text (using whisper)
        try:
            import whisper
            model_whisper = whisper.load_model("base")
            audio_text = model_whisper.transcribe(audio_path)["text"]
        except:
            audio_text = "Speech-to-text failed."

        # Gemini API: image + text
        prompt = f"The user said: '{audio_text}'. Analyze the image and explain accordingly."

        gemini_response = model.generate_content([prompt, image])

        result = {
            "user_voice": audio_text,
            "gemini_output": gemini_response.text.strip()
        }

    return render(request, 'multimodal_query/webcam_input.html', {"result": result})

whisper_model = whisper.load_model("base")
@login_required
def audio_input_view(request):
    result = None
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        file_path = default_storage.save('temp_audio.wav', audio_file)

        # Transcribe using Whisper
        transcription = whisper_model.transcribe(default_storage.path(file_path))
        user_text = transcription['text']

        # Now use Gemini to process this transcribed text
        def gemini_generate(prompt):
            response = model.generate_content(prompt + "\n" + user_text)
            return response.text.strip()
        
        summary = gemini_generate("Summarize the following text:")
        notes = gemini_generate("Convert the following into bullet notes:")
        imp_questions = gemini_generate("Create 10 important questions based on this text:")
        mcqs = gemini_generate("Create 5 multiple-choice questions with 4 options and correct answers:")
        para_qna = gemini_generate("Create 2 paragraph-based questions and answers from this:")
        links = gemini_generate("List 3 websites or sources where a student can learn more about this topic:")

        summary = clean_output(summary)
        notes = clean_output(notes)
        imp_questions = clean_output(imp_questions)
        mcqs = clean_output(mcqs)
        para_qna = clean_output(para_qna)
        links = clean_output(links)

        result = {
            "transcribed_text": user_text,
            "summary": summary,
            "notes": notes,
            "questions": imp_questions.split("\n"),
            "mcqs": mcqs.split("\n"),
            "paragraph_questions": para_qna.split("\n"),
            "links": links.split("\n"),
        }

    return render(request, "multimodal_query/audio_input.html", {"result": result})


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
@login_required
def text_input_view(request):
    result = None
    if request.method == 'POST':
        user_text = request.POST.get("user_text")

        def gemini_generate(prompt):
            response = model.generate_content(prompt + "\n" + user_text)
            return response.text.strip()

        summary = gemini_generate("Summarize the following text:")
        notes = gemini_generate("Convert the following into bullet notes:")
        imp_questions = gemini_generate("Create 10 important questions based on this text:")
        mcqs = gemini_generate("Create 5 multiple-choice questions with 4 options and correct answers:")
        para_qna = gemini_generate("Create 2 paragraph-based questions and answers from this:")
        links = gemini_generate("List 3 websites or sources where a student can learn more about this topic:")

        summary = clean_output(summary)
        notes = clean_output(notes)
        imp_questions = clean_output(imp_questions)
        mcqs = clean_output(mcqs)
        para_qna = clean_output(para_qna)
        links = clean_output(links)

        result = {
            "summary": summary,
            "notes": notes,
            "questions": imp_questions.split("\n"),
            "mcqs": mcqs.split("\n"),
            "paragraph_questions": para_qna.split("\n"),
            "links": links.split("\n"),
        }

    return render(request, "multimodal_query/text_input.html", {"result": result})

@login_required
def record_audio_view(request):
    result = None
    if request.method == 'POST' and request.FILES.get('recorded_audio'):
        audio_file = request.FILES['recorded_audio']
        file_path = default_storage.save('recorded_audio.webm', audio_file)

        # Transcribe
        transcription = whisper_model.transcribe(default_storage.path(file_path))
        user_text = transcription['text']

        # Use Gemini
        def gemini_generate(prompt):
            response = model.generate_content(prompt + "\n" + user_text)
            return response.text.strip()

        result = {
            "transcribed_text": user_text,
            "summary": gemini_generate("Summarize the following:"),
            "notes": gemini_generate("Convert the following into bullet point notes:"),
            "questions": gemini_generate("Generate 10 important questions based on this:").split("\n"),
            "mcqs": gemini_generate("Generate 5 multiple choice questions with 4 options and correct answers:").split("\n"),
            "paragraph_questions": gemini_generate("Create 2 paragraph-based questions and answers:").split("\n"),
            "links": gemini_generate("List 3 websites to learn more about this topic:").split("\n"),
        }

    return render(request, "multimodal_query/record_audio.html", {"result": result})

import fitz  # PyMuPDF
from django.core.files.storage import default_storage
@login_required
def pdf_input_view(request):
    result = None
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        file_path = default_storage.save('uploaded_pdf.pdf', pdf_file)
        full_path = default_storage.path(file_path)

        # Extract text using PyMuPDF
        text = ""
        with fitz.open(full_path) as doc:
            for page in doc:
                text += page.get_text()

        # Gemini prompts
        def gemini_generate(prompt):
            response = model.generate_content(prompt + "\n" + text)
            return response.text.strip()
        
        summary = gemini_generate("Summarize the following text:")
        imp_questions = gemini_generate("Create 10 important questions based on this text:")
        mcqs = gemini_generate("Create 5 multiple-choice questions with 4 options and correct answers:")
        para_qna = gemini_generate("Create 2 paragraph-based questions and answers from this:")
        links = gemini_generate("List 3 websites or sources where a student can learn more about this topic:")

        summary = clean_output(summary)
        imp_questions = clean_output(imp_questions)
        mcqs = clean_output(mcqs)
        para_qna = clean_output(para_qna)
        links = clean_output(links)

        result = {
            "extracted_text": text[:1500] + "...",  # only previewing part of text
            "summary": summary,
            "questions": imp_questions.split("\n"),
            "mcqs": mcqs.split("\n"),
            "paragraph_questions": para_qna.split("\n"),
            "links": links.split("\n"),
        }

    return render(request, "multimodal_query/pdf_input.html", {"result": result})
@login_required
def image_input_view(request):
    result = None
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        file_path = default_storage.save('uploaded_image.png', image_file)
        full_path = default_storage.path(file_path)

        # Open the image with PIL
        image = Image.open(full_path)

        # Use Gemini to describe/explain it
        response = model.generate_content(
            [
                "Explain this image in detail like you would to a student studying the topic.",
                image
            ]
        )

        result = response.text.strip()

    return render(request, 'multimodal_query/image_input.html', {'result': result})
@login_required
def query_form(request):
    return render(request, 'multimodal_query/query_form.html')