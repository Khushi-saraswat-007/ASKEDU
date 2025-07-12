from django.urls import path
from . import views

urlpatterns = [
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('form-groups/', views.form_groups, name='form_groups'),
    path('student/<int:student_id>/groups/', views.student_groups, name='student_groups'),
    path('group/<int:group_id>/student/<int:student_id>/chat/', views.group_chat, name='group_chat'),
    path('send-message/', views.send_message, name='send_message'),  # for AJAX
    path('submit-progress/<int:session_id>/<int:student_id>/', views.submit_progress, name='submit_progress'),
    path('teacher-progress/<int:teacher_id>/', views.teacher_progress_dashboard, name='teacher_progress_dashboard'),
    path('student-dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard'),

]

