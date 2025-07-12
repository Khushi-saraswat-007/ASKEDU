from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('upload/', views.upload_recording, name='upload_recording'),
    path('delete/<int:rec_id>/', views.delete_recording, name='delete_recording'),

    # student
    path('studentrecording/', views.student_dashboard, name='student_dashboard'),
    path('make-notes/<int:rec_id>/', views.generate_notes, name='generate_notes'),
    path('make-quiz/<int:rec_id>/', views.generate_quiz, name='generate_quiz'),
    path('reexplain_recording/<int:rec_id>/', views.reexplain_recording, name='reexplain_recording'),
    path('view-notes/<int:rec_id>/', views.view_notes, name='view_notes'),
    path('view-quiz/<int:rec_id>/', views.view_quiz, name='view_quiz'),
]

