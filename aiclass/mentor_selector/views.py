import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from .models import ChatHistory, ChatSession, Message
from dotenv import load_dotenv
import google.generativeai as genai
from django.contrib.auth.decorators import login_required

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
@login_required
def landing_page(request):
    sessions = ChatSession.objects.prefetch_related('messages').order_by('-created_at')

    # Prepare a list of past sessions with short previews
    session_data = []
    for session in sessions:
        last_msg = session.messages.last()
        preview = last_msg.text[:60] + "..." if last_msg else "(No messages yet)"
        session_data.append({
            'id': session.id,
            'mentor': session.mentor,
            'session_name': session.session_name,
            'created_at': session.created_at,
            'preview': preview
        })

    return render(request, 'mentor_selector/landing.html', {
        'sessions': session_data
    })
@login_required

def chat_view(request, mentor_type):
    if 'session_id' not in request.session:
        session_name = str(uuid.uuid4())[:8]
        chat_session = ChatSession.objects.create(
            mentor=mentor_type,
            session_name=session_name
        )
        request.session['session_id'] = chat_session.id  # ✅ store integer ID

    # ✅ Cast session ID to integer to avoid UUID error
    try:
        session_id = int(request.session['session_id'])
    except (ValueError, TypeError):
        return redirect('new_chat', mentor_type=mentor_type)

    try:
        chat_session = ChatSession.objects.get(id=session_id)
    except ChatSession.DoesNotExist:
        return redirect('new_chat', mentor_type=mentor_type)

    user_question = ""
    response_text = ""

    if request.method == "POST":
        user_question = request.POST.get("user_question")

        style_prompt = {
            "chill": "You're a chill, supportive friend mentor. Use casual, positive, encouraging tone.",
            "strict": "You're a strict professor. Be blunt, serious, and logical.",
            "anime": "You're an anime senpai! Speak anime-style with ✿(◕‿◕) emojis and motivation!"
        }.get(mentor_type, "You're a helpful AI assistant.")

        full_prompt = f"{style_prompt}\nUser asked: {user_question}"

        try:
            chat = model.start_chat()
            response = chat.send_message(full_prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"Error: {str(e)}"

        # Save to new tables
        Message.objects.create(session=chat_session, sender="user", text=user_question)
        Message.objects.create(session=chat_session, sender="mentor", text=response_text)

        # Optional: Also save to legacy ChatHistory model
        ChatHistory.objects.create(
            mentor_type=mentor_type,
            session_id=session_id,
            user_message=user_question,
            ai_response=response_text
        )

    messages = chat_session.messages.order_by('timestamp')

    return render(request, 'mentor_selector/chat.html', {
        'mentor_type': mentor_type,
        'session': chat_session,
        'chat_history': messages,
        'response': response_text,
        'user_question': user_question,
    })

@login_required
def new_chat(request, mentor_type):
    request.session.pop('session_id', None)
    return redirect('chat', mentor_type=mentor_type)
@login_required
def set_session(request, session_id):
    request.session['session_id'] = session_id
    return HttpResponse("Session ID set.")

@login_required
@require_POST
def delete_chat(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    session.delete()
    return redirect('landing')
@login_required
@require_POST
def reset_all_chats(request):
    ChatSession.objects.all().delete()
    return redirect('landing')

@login_required
@require_GET
def clear_session_on_exit(request):
    request.session.pop('session_id', None)
    return redirect('landing')  # Or return HttpResponse("Session cleared")