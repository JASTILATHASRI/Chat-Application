import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myChat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<int:user_id>/', ChatConsumer.as_asgi()),
        ])
    ),
})