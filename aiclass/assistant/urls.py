from django.urls import path
from . import views

urlpatterns = [
    path('assistant/', views.chat_view, name='chat'),
]
