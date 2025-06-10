from rest_framework.routers import DefaultRouter
from .views import (
    ModeloIAViewSet,
    PrediccionManualViewSet,
    PrediccionDashboardViewSet,
    DashboardView,
)
from django.urls import path, include

router = DefaultRouter()

router.register(r"modelos", ModeloIAViewSet)
router.register(r"predicciones", PrediccionManualViewSet)
router.register(
    r"dashboard-predicciones", PrediccionDashboardViewSet, basename="dashboard"
)


urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
