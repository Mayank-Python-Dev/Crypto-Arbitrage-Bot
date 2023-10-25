"""
ASGI config for cryptoArbitrage project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from core.consumers import BotConsumer,AppConsumer,ExchangeConsumer
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoArbitrage.settings")

django_asgi_app = get_asgi_application()

application= ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket':AuthMiddlewareStack(
        URLRouter([
            # path('ws/communicate/<room_code>',CommunicationConsumer.as_asgi()), 
            path("ws/exchangeInfo/<room_code>",AppConsumer.as_asgi()),
            path("ws/getExchangeList/<room_code>",ExchangeConsumer.as_asgi()),
        ]
        )
    ),
})