from django.db import models
from authentication.models import CustomUser

class PeriodicAnalysisConfig(models.Model):
    interval_minutes = models.PositiveIntegerField(default=1)  
    is_analysis_running = models.BooleanField(default=False)

class EmotionRecord(models.Model):
    EMOTION_CHOICES = [
        ('angry', 'Angry'),
        ('disgust', 'Disgust'),
        ('fear', 'Fear'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('surprise', 'Surprise'),
        ('neutral', 'Neutral'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    emotion_level = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    image = models.ImageField(upload_to='emotion_images/', blank=True, null=True)
    video = models.FileField(upload_to='emotion_videos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    config = models.ForeignKey(PeriodicAnalysisConfig, null=True, blank=True, on_delete=models.SET_NULL)

