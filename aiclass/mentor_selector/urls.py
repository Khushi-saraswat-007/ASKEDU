from django.urls import path
from . import views

urlpatterns = [
    path('mentor_selector/', views.landing_page, name='landing'),
    path('chat/<str:mentor_type>/', views.chat_view, name='chat'),
    path('new_chat/<str:mentor_type>/', views.new_chat, name='new_chat'),
    path('set_session/<int:session_id>/', views.set_session, name='set_session'),  # ✅ NEW

    path('delete_chat/<int:session_id>/', views.delete_chat, name='delete_chat'),
    path('reset_chats/', views.reset_all_chats, name='reset_all_chats'),
    path('clear_session/', views.clear_session_on_exit, name='clear_session'),


]
