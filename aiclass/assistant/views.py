import os
import re
from dotenv import load_dotenv
from django.shortcuts import render
import google.generativeai as genai
from django.shortcuts import redirect, get_object_or_404

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def format_response(text):
    # Multiline Code Blocks: ```lang\ncode\n```
    text = re.sub(
        r"```(\w+)?\n(.*?)```",
        lambda m: f"<pre><code class='language-{m.group(1)}'>{m.group(2)}</code></pre>" if m.group(1) else f"<pre><code>{m.group(2)}</code></pre>",
        text,
        flags=re.DOTALL
    )

    # Bold: **bold**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Inline Italic: `text`
    text = re.sub(r"`([^`]+)`", r"<i>\1</i>", text)

    # Bullet points: - item → <ul><li>item</li></ul>
    lines = text.split('\n')
    bullet_lines = []
    in_list = False

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                bullet_lines.append('<ul>')
                in_list = True
            bullet_lines.append(f"<li>{line.strip()[2:]}</li>")
        else:
            if in_list:
                bullet_lines.append('</ul>')
                in_list = False
            bullet_lines.append(line)

    if in_list:
        bullet_lines.append('</ul>')

    return '\n'.join(bullet_lines)

from .models import Chat  # Import Chat model
def chat_view(request):

    formatted_response = None

    if request.method == "POST":
        task = request.POST.get("prompt")
        code = request.POST.get("code") or ""
        full_prompt = f"{task}:\n\n{code}"

        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
            result = model.generate_content(full_prompt)
            raw_response = result.text
            formatted_response = format_response(raw_response)
            # existing processing...
            Chat.objects.create(
                user_prompt=full_prompt,
                response=formatted_response,
        )
        except Exception as e:
            formatted_response = f"<span style='color:red;'>Error: {str(e)}</span>"

    return render(request, "assistant/chat.html", {
        "response": formatted_response,
    })
