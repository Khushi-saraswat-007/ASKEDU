from django.urls import path
from . import views
from .views import generate_smart_pdf

urlpatterns = [
    path('start/', views.quiz_start, name='quiz_start'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('result/', views.quiz_result, name='quiz_result'),
    path('quiz_dashboard/', views.student_dashboard, name='dashboard'),
    path('download_result/', views.generate_pdf_result, name='download_pdf'),
    path('history/', views.quiz_history, name='quiz_history'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('smart_pdf/', generate_smart_pdf, name='generate_smart_pdf'),
]
