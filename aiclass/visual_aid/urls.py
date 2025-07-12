from django.urls import path
from .views import generate_visual

urlpatterns = [
    path('visual/', generate_visual, name='generate_visual'),
]
