
from django.contrib import admin
from .models import PinnedTopic

@admin.register(PinnedTopic)
class PinnedTopicAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic_text', 'class_name', 'timestamp', 'selected_tone')
    search_fields = ('topic_text', 'user__username', 'class_name')
