from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('timeline_home/', views.index, name='timeline_home'),  # Home Page
    path('search/', views.search, name='search'),  # Search results
    path('timeline/<str:timeline_id>/', views.timeline_view, name='timeline_detail'),  # Timeline detail
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
