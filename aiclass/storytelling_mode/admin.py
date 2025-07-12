from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'age', 'created_at')
    search_fields = ('topic', 'user__username', 'content')
    list_filter = ('age', 'created_at')
