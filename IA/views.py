from IA.serializers import (
    ModeloIASerializer,
    PrediccionManualSerializer,
    PrediccionDashboardSerializer,
    DashboardSerializer,
)
from IA.models import ModeloIA, Prediccion
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from Equipos.models import Equipo, Area


class ModeloIAViewSet(ModelViewSet):
    queryset = ModeloIA.objects.all()
    serializer_class = ModeloIASerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "post", "delete"]


class PrediccionManualViewSet(ModelViewSet):
    queryset = Prediccion.objects.all()
    serializer_class = PrediccionManualSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["modelo_ia", "modelo_equipo", "equipo"]
    ordering = ["-fecha_creacion"]
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


class PrediccionDashboardFilter(filters.FilterSet):
    fecha_creacion = filters.DateFromToRangeFilter()

    class Meta:
        model = Prediccion
        fields = ["modelo_ia", "modelo_equipo", "equipo", "fecha_creacion"]


class PrediccionDashboardViewSet(ModelViewSet):
    queryset = Prediccion.objects.all()
    serializer_class = PrediccionDashboardSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PrediccionDashboardFilter
    filterset_fields = [
        "modelo_ia",
        "modelo_equipo",
        "equipo",
        "fecha_creacion",
    ]
    ordering = ["-fecha_creacion"]
    pagination_class = LimitOffsetPagination
    http_method_names = ["get"]


class DashboardView(GenericAPIView):
    serializer_class = DashboardSerializer

    def get(self, request):

        data = {
            "num_modelos": ModeloIA.objects.count(),
            "num_predicciones": Prediccion.objects.count(),
            "num_equipos": Equipo.objects.count(),
            "num_areas": Area.objects.count(),
        }

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
