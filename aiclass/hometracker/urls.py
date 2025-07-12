from django.urls import path
from . import views

urlpatterns = [
    path('homework/', views.react_home, name='react-home'),
]
