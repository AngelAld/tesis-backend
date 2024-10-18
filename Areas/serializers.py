from os import read
from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = [
            "id",
            "nombre",
            "ip",
            "descripcion",
            "estado",
        ]
        read_only_fields = ["id", "ip"]
