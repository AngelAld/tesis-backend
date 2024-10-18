from django.urls import path, include
from .views import (
    SensorStatsListCreate,
    FailureLogsViewSet,
    DumpSensorStatsCsv,
    DataSetsListView,
    DataSetDestroyView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("failure-logs", FailureLogsViewSet, basename="logs")

urlpatterns = [
    path("list/", SensorStatsListCreate.as_view(), name="list"),
    path("", include(router.urls)),
    path("dump/", DumpSensorStatsCsv.as_view(), name="dump"),
    path("datasets/", DataSetsListView.as_view(), name="datasets"),
    path("datasets/<int:pk>/", DataSetDestroyView.as_view(), name="delete"),
]
