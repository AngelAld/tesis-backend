from rest_framework.viewsets import ModelViewSet
from Equipos.models import Equipo, Modelo
from Equipos.serializers import (
    EquipoSerializer,
    EquipoListSerializer,
    EquipoDetalleSerializer,
    ModeloSerializer,
)
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter


class EquipoViewSet(ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    http_method_names = ["get", "post"]


class EquipoListView(ListAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["area"]
    search_fields = [
        "id",
        "hostname",
        "ip",
        "area__nombre",
        "modelo__nombre",
        "estado",
        "estado_equipo__nombre",
        "estado_alerta__nombre",
    ]


class EquipoDetalleView(RetrieveUpdateAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoDetalleSerializer
    http_method_names = ["get", "put"]


class ModeloViewSet(ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    http_method_names = ["get", "post", "put", "delete"]
