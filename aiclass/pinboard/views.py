from django.shortcuts import render, redirect
from .forms import PinnedTopicForm
from .models import PinnedTopic
from django.contrib.auth.decorators import login_required
import os
import google.generativeai as genai
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import PinnedTopic as Pin

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
import re
@login_required
def remove_markdown(text):
    # Removes **bold**, *italic*, `code`, and ## headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Inline code
    text = re.sub(r'#+\s*(.*?)\n', r'\1\n', text) # Headers
    return text

@login_required
def pin_topic_view(request):
    if request.method == 'POST':
        form = PinnedTopicForm(request.POST)
        if form.is_valid():
            pinned_topic = form.save(commit=False)
            pinned_topic.user = request.user
            pinned_topic.save()
            return redirect('pinboard:my_pins')  # or your preferred view name
    else:
        form = PinnedTopicForm()

    return render(request, 'pinboard/pin_form_card.html', {'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def my_pins_view(request):
    pins = Pin.objects.filter(user=request.user)
    explained_pin_id = request.session.get('explained_pin_id')
    temp_response = request.session.get('temp_response')
    tone = request.session.get('selected_tone')
    return render(request, 'pinboard/pin_list_card.html', {
        'pins': pins,
        'explained_pin_id': explained_pin_id,
        'temp_response': temp_response,
        'selected_tone': tone,
    })


@login_required
def explain_pin(request, pin_id):
    pin = get_object_or_404(PinnedTopic, id=pin_id, user=request.user)

    if request.method == 'POST':
        tone = request.POST.get('tone')

        # Construct prompt
        prompt = f"Explain the following topic in a {tone} tone: {pin.topic_text}"

        # Use Gemini
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        clean_text = remove_markdown(raw_text)

        # Save response
        pin.assistant_response = clean_text
        pin.selected_tone = tone
        pin.save()


    return redirect('pinboard:my_pins')

@login_required

def save_explanation_view(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)
    pin.assistant_response = request.session.get('temp_response')
    pin.selected_tone = request.session.get('selected_tone')
    pin.save()

    request.session['explained_pin_id'] = None
    request.session['temp_response'] = None
    request.session['selected_tone'] = None

    return redirect('my_pins')