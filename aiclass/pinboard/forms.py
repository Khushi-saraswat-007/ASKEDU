from django import forms
from .models import PinnedTopic

class PinnedTopicForm(forms.ModelForm):
    class Meta:
        model = PinnedTopic
        fields = ['topic_text', 'class_name']
        widgets = {
            'topic_text': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Write the topic or concept you didn’t understand...'
            }),
            'class_name': forms.TextInput(attrs={
                'placeholder': 'Optional: Class name or subject'
            }),
        }
