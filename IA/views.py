from .serializers import ModeloIASerializer, PrediccionManualSerializer
from .models import ModeloIA, Prediccion
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class ModeloIAViewSet(ModelViewSet):
    queryset = ModeloIA.objects.all()
    serializer_class = ModeloIASerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "post", "delete"]


class PrediccionManualViewSet(ModelViewSet):
    queryset = Prediccion.objects.all()
    serializer_class = PrediccionManualSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["modelo_ia", "modelo_equipo", "equipo"]
    search_fields = [
        "cpu_total_load",
        "cpu_core_max_load",
        "cpu_core_max_temp",
        "cpu_core_avg_temp",
        "cpu_avg_core_clock",
        "cpu_bus_speed_clock",
        "cpu_package_power",
        "cpu_cores_power",
        "cpu_memory_power",
        "cpu_core_voltage",
        "memory_load",
        "memory_available",
        "memory_used",
        "avg_used_space",
        "avg_read",
        "avg_write",
        "avg_activity",
        "max_used_space",
        "max_read",
        "max_write",
        "max_activity",
        "failure_percentage",
    ]
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "post", "delete"]
