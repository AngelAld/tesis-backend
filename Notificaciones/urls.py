from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/notificaciones/", views.listar_notificaciones, name="listar_notificaciones"
    ),
    path(
        "api/notificaciones/<int:pk>/leida/",
        views.marcar_como_leida,
        name="marcar_como_leida",
    ),
]
