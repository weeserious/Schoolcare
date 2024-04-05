"""
ASGI config for deepcare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from emotion_detection.routing import application as emotion_detection_application
from emotion_detection.analysis import start_background_task
import threading


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepcare.settings')

# application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            emotion_detection_application,
        )
    ),
})

threading.Thread(target=start_background_task).start()
