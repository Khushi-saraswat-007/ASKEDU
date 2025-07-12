from django.urls import path
from . import views
from .views import teacher_profile_view
from .views import update_user_info
from .views import firebase_login_view

urlpatterns = [
    path('firebase-login/', firebase_login_view, name='firebase_login'),
    path('start-live-class/', views.start_live_class, name='start_live_class'),
    path('schedule-meeting/', views.schedule_meeting, name='schedule_meeting'),
    path('update-user-info/', update_user_info, name='update_user_info'),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='teachersdashboard'),
    path('studentdashboard/', views.studentdashboard, name='studentdashboard'),
    path('login/', views.loginpage, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('announcement/edit/<int:pk>/', views.edit_announcement, name='edit_announcement'),
    path('behavior-notes/', views.behavior_notes_view, name='behavior_notes'),
    path('behavior-notes/edit/<int:note_id>/', views.edit_behavior_note, name='edit_behavior_note'),
    path('behavior-notes/delete/<int:note_id>/', views.delete_behavior_note, name='delete_behavior_note'),
    path('manual-students/', views.manual_student_list, name='manual_student_list'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),
    path('attendance/export/', views.attendance_csv_export, name='attendance_csv_export'),
    path('teacher/profile/', teacher_profile_view, name='teacher_profile'),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    path('join_classroom/', views.join_classroom, name='join_classroom'),
    path('meeting/delete/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
    path('manual-students/edit/<int:student_id>/', views.edit_manual_student, name='edit_manual_student'),
    path('manual-students/delete/<int:student_id>/', views.delete_manual_student, name='delete_manual_student'),
    path('delete-announcement/<int:pk>/', views.delete_announcement, name='delete_announcement'),

]

