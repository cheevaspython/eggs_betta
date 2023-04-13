import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from websocket.middleware import JwtAuthMiddlewareStack
from websocket import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
      ),
})
