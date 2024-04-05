from django import forms
from .models import EmotionRecord

class EmotionDetectionForm(forms.ModelForm):
    class Meta:
        model = EmotionRecord
        fields = ['image']

