from operator import eq
from django.utils.timezone import now
from Equipos.models import Equipo
from .models import SensorStats, FailureLogs
from .serializers import SensorStatsSerializer, FailureLogsSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class SensorStatsListCreate(ListCreateAPIView):
    queryset = SensorStats.objects.all()
    serializer_class = SensorStatsSerializer

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
