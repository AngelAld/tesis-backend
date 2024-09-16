from rest_framework.viewsets import ModelViewSet
from Equipos.models import Equipo
from Equipos.serializers import EquipoSerializer


class EquipoViewSet(ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    http_method_names = ["get", "post", "delete"]
