from rest_framework.serializers import ModelSerializer
from Equipos.models import Equipo
from Sensores.models import SensorStats, FailureLogs
from django.db.transaction import atomic


class SensorStatsSerializer(ModelSerializer):
    class Meta:
        model = SensorStats
        fields = "__all__"


class FailureLogsSerializer(ModelSerializer):
    class Meta:
        model = FailureLogs
        fields = "__all__"
