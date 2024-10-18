from django.utils.timezone import now
from Equipos.models import Equipo
from .models import DataSet, SensorStats, FailureLogs
from .serializers import (
    DataSetSerializer,
    SensorStatsSerializer,
    FailureLogsSerializer,
    DumpRequestSerializer,
)
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.filters import SearchFilter, OrderingFilter
from .utils import dump_data
from django_filters import rest_framework as filters


class SensorStatsListCreate(ListCreateAPIView):
    queryset = SensorStats.objects.all()
    serializer_class = SensorStatsSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["equipo"]
    ordering = ["-fecha_registro"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        equipo: Equipo = Equipo.objects.get(id=request.data[0]["equipo"])
        equipo.last_update = now()
        equipo.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FailureLogsViewSet(ModelViewSet):
    queryset = FailureLogs.objects.all()
    serializer_class = FailureLogsSerializer
    http_method_names = ["get", "post", "delete"]


class DumpSensorStatsCsv(CreateAPIView):
    queryset = SensorStats.objects.all()
    serializer_class = DumpRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        modelo = data["modelo"]
        fecha_inicio = data["fecha_inicio"]
        fecha_fin = data["fecha_fin"]
        nombre = data["nombre"]

        # Generar el CSV y guardar en la base de datos
        csv_url = dump_data(modelo, fecha_inicio, fecha_fin, nombre)

        return Response({"csv": csv_url})


class DataSetFilter(filters.FilterSet):
    fecha_registro = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = DataSet
        fields = ["modelo", "fecha_registro"]


class DataSetsListView(ListAPIView):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DataSetFilter
    search_fields = [
        "modelo__nombre",
        "fecha_registro",
        "fecha_inicio",
        "fecha_fin",
    ]
    ordering = ["-fecha_registro"]
    pagination_class = LimitOffsetPagination


class DataSetDestroyView(DestroyAPIView):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
