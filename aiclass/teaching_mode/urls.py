from django.urls import path
from . import views

urlpatterns = [
    path('teaching_mode/', views.index, name='expression_index'),
    path('evaluate/', views.evaluate, name='expression_evaluate'),
]
