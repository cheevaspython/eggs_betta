import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# from websocket.middleware import JwtAuthMiddlewareStack
from websocket import routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": (
            URLRouter(
                routing.websocket_urlpatterns
            )
      ),
})
