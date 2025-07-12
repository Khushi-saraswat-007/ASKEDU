from django.contrib import admin
from .models import Chat
# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_prompt', 'created_at', 'session_key')

admin.site.register(Chat, ChatAdmin)