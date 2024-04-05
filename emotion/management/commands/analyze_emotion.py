from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from .emotion_model import EmotionModel  
from emotion.models import EmotionRecord

class Command(BaseCommand):
    help = 'Periodically analyzes emotion and saves results to the database.'

    def handle(self, *args, **options):
        model = EmotionModel()
        
        image = capture_image()  

        with transaction.atomic():
            emotion_result = model.predict_emotion_from_image(image)

            depression_level = scale_depression(emotion_result)

            EmotionRecord.objects.create(
                timestamp=timezone.now(),
                emotion_result=emotion_result,
                depression_level=depression_level
            )
