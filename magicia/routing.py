from channels.routing import ProtocolTypeRouter, URLRouter
from magicia.consumers import PracticeConsumer
from channels.auth import AuthMiddlewareStack
from django.urls import path

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('test/',PracticeConsumer(),name='test')
        ])
    )
})
