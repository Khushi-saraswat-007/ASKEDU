from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from matchmaker import views as matchmaker_views

urlpatterns = [
    path('', matchmaker_views.home, name='home'),  # Default homepage
    path('admin/', admin.site.urls),
    path('matchmaker/', include('matchmaker.urls')),

]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

