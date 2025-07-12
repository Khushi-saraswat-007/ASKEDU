from django.urls import path
from . import views

urlpatterns = [
path('storytelling_mode/', views.storytelling_home, name='storytelling_home'),
path('storytelling_mode/generate-story-with-audio/', views.generate_story_with_audio, name='generate_story_with_audio'),

    path('storytelling_mode/my-stories/', views.my_stories_view, name='my_stories'),
    path('storytelling_mode/delete/<int:story_id>/', views.delete_story, name='delete_story'),

]
