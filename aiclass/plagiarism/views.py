from django.shortcuts import render
from django.contrib import messages
from .gemini_service import analyze_plagiarism
from django.contrib.auth.decorators import login_required
@login_required
def plagiarism_checker(request):
    if request.method == "POST":
        content = ""
        content_type = request.POST.get("content_type", "text")

        # 🔍 Check if file is uploaded
        uploaded_file = request.FILES.get("file")
        if uploaded_file:
            try:
                file_data = uploaded_file.read()
                content = file_data.decode("utf-8", errors="ignore")  # decode safely
            except Exception as e:
                messages.error(request, f"File read error: {e}")
                return render(request, "plagiarism/plagiarism_index.html")
        else:
            # If no file, get content from textarea
            content = request.POST.get("content", "")

        if len(content.strip()) < 50:
            messages.error(request, "Content must be at least 50 characters for analysis.")
            return render(request, "plagiarism/plagiarism_index.html")

        # ✅ Run Gemini analysis
        result = analyze_plagiarism(content, content_type)

        # ✅ Flash message
        messages.success(request, "Analysis completed!")
        return render(request, "plagiarism/result.html", {
            "analysis": result,
            "content": content,
            "content_type": content_type
        })

    return render(request, "plagiarism/plagiarism_index.html")
