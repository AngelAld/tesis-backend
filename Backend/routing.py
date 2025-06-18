# tu_proyecto/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from .jwt_auth_middleware import JWTAuthMiddleware
import Notificaciones.routing
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(
            URLRouter(Notificaciones.routing.websocket_urlpatterns)
        ),
    }
)
