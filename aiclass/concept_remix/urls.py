from django.urls import path
from . import views

urlpatterns = [
    path('concept_remix/', views.index, name='concept_remix_home'),  # Example path
]
