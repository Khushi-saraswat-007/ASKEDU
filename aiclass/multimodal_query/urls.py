from django.urls import path
from . import views

urlpatterns = [
    path('text/', views.text_input_view, name='text_input'),
    path('audio/', views.audio_input_view, name='audio_input'),
    path('record-audio/', views.record_audio_view, name='record_audio'),
    path('pdf/', views.pdf_input_view, name='pdf_input'),
    path('image/', views.image_input_view, name='image_input'),
    path('webcam/', views.webcam_view, name='webcam_input'),
    path('query/', views.query_form, name='query_form'),

]
