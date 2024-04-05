from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detect-emotion/', detect_emotion, name='detect_emotion'),
    path('start-stop-analysis/', start_stop_analysis, name='start_stop_analysis'),
    path('result/<str:detected_emotion>/', result, name='show_result'),

    # path('start-live-emotion-detection/', start_live_emotion_detection, name='start_live_emotion_detection'),
    # path('stop-live-emotion-detection/<int:emotion_record_id>/', stop_live_emotion_detection, name='stop_live_emotion_detection'),
    # path('live-emotion-feed/', live_emotion_feed, name='live_emotion_feed'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

