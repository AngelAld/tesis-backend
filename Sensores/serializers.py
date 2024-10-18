from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    PrimaryKeyRelatedField,
    DateTimeField,
    StringRelatedField,
    CharField,
)
from Equipos.models import Equipo, Modelo
from Sensores.models import DataSet, SensorStats, FailureLogs
from django.db.transaction import atomic


class SensorStatsSerializer(ModelSerializer):
    class Meta:
        model = SensorStats
        fields = "__all__"


class FailureLogsSerializer(ModelSerializer):
    class Meta:
        model = FailureLogs
        fields = "__all__"


class DumpRequestSerializer(Serializer):
    modelo = PrimaryKeyRelatedField(queryset=Modelo.objects.all())
    fecha_inicio = DateTimeField()
    fecha_fin = DateTimeField()
    nombre = CharField()

    def validate(self, attrs):
        if attrs["fecha_inicio"] > attrs["fecha_fin"]:
            raise ValueError("Fecha de inicio no puede ser mayor a la fecha de fin")
        return attrs

    class Meta:
        fields = ["modelo", "fecha_inicio", "fecha_fin", "nombre"]


class DataSetSerializer(ModelSerializer):
    modelo = StringRelatedField(source="modelo.nombre")
    nombre = StringRelatedField(source="csv.name")

    class Meta:
        model = DataSet
        fields = "__all__"
