# notificaciones/routing.py

from django.urls import path

from Notificaciones.consumers import NotificacionConsumer


websocket_urlpatterns = [
    path("ws/notificaciones/", NotificacionConsumer.as_asgi()),
]
