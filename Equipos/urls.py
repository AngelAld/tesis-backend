from rest_framework.routers import DefaultRouter
from django.urls import path, include
from Equipos.views import EquipoViewSet

router = DefaultRouter()
router.register(r"equipos", EquipoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
