from rest_framework.routers import DefaultRouter
from .views import ModeloIAViewSet, PrediccionManualViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r"modelos", ModeloIAViewSet)
router.register(r"predicciones", PrediccionManualViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
