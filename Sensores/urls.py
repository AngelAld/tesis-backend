from django.urls import path, include
from .views import SensorStatsListCreate, FailureLogsViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("failure-logs", FailureLogsViewSet, basename="logs")

urlpatterns = [
    path("list/", SensorStatsListCreate.as_view(), name="list"),
    path("", include(router.urls)),
]
