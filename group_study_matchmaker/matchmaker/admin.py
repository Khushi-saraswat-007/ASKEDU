from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(StudySession)
admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(SessionProgress)
