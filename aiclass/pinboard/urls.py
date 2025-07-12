from django.urls import path
from . import views

app_name = 'pinboard'

urlpatterns = [
    path('pin/', views.pin_topic_view, name='pin_topic'),
    path('my-pins/', views.my_pins_view, name='my_pins'),
    path('explain/<int:pin_id>/', views.explain_pin, name='explain_pin'),
    path('save-explanation/<int:pin_id>/', views.save_explanation_view, name='save_explanation'),

]
