from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # Include your app's URLs at root
    path('', include('multimodal_query.urls')),  # Include multimodal query app URLs
    path('', include('hometracker.urls')),  
    path('', include('visual_aid.urls')),
    path('', include('pinboard.urls')), 
    path('', include('storytelling_mode.urls')),
    path('', include('plagiarism.urls')),
    path('', include('teaching_mode.urls')),
    path('', include('concept_remix.urls')),
    path('', include('mentor_selector.urls')),
    path('', include('classroom.urls')),
    path('', include('quizzes.urls')),
    path('', include('timeline.urls')),
    path('', include('assistant.urls')),
    path('', include('emotiontracker.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
