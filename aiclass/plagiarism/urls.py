from django.urls import path
from . import views

urlpatterns = [
    path('plagiarism/', views.plagiarism_checker, name='plagiarism'),
]
