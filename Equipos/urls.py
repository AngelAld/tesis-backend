from rest_framework.routers import DefaultRouter
from django.urls import path, include
from Equipos.views import (
    EquipoViewSet,
    EquipoListView,
    EquipoDetalleView,
    ModeloViewSet,
)

router = DefaultRouter()
router.register(r"equipos", EquipoViewSet)
router.register(r"modelos", ModeloViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lista/", EquipoListView.as_view(), name="equipos-list"),
    path("detalle/<int:pk>/", EquipoDetalleView.as_view(), name="equipos-detail"),
]
