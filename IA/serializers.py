from pyexpat import model
from rest_framework import serializers

from IA.util import predecir
from .models import ModeloIA, Prediccion, cpu_columns, disk_columns, mem_columns
import tensorflow as tf
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler


class ModeloIASerializer(serializers.ModelSerializer):
    # modelo_equipo = serializers.CharField(source="modelo_equipo")

    class Meta:
        model = ModeloIA
        fields = "__all__"


class PrediccionManualSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediccion
        fields = [
            "id",
            "modelo_ia",
            "modelo_equipo",
            "equipo",
            "fecha_creacion",
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
            "is_manual",
        ]
        read_only_fields = [
            "is_manual",
            "failure_percentage",
            "id",
            "fecha_creacion",
        ]

    def create(self, validated_data):
        modelIA: ModeloIA = validated_data.pop("modelo_ia")
        print(modelIA)
        modelo_equipo = validated_data.pop("modelo_equipo")
        equipo = validated_data.pop("equipo")
        try:
            variable_objetivo = modelIA.variable_objetivo

            componente = modelIA.componente
            columns = []
            if componente == "cpu":
                columns = cpu_columns
            elif componente == "ram":
                columns = mem_columns
            elif componente == "disk":
                columns = disk_columns

            variables = [
                validated_data.get(column)
                for column in columns
                if column != variable_objetivo
            ]

            expected_value = validated_data.get(variable_objetivo)

            predicted_value = predecir(modelIA, variables)

            failure_percentage = abs(expected_value - predicted_value) / expected_value

            validated_data["failure_percentage"] = failure_percentage

            validated_data["modelo_equipo"] = modelo_equipo

            validated_data["is_manual"] = True

            validated_data[variable_objetivo] = expected_value

            validated_data["modelo_ia"] = modelIA

            validated_data["equipo"] = equipo

            instance = Prediccion.objects.create(**validated_data)

            return instance
        except Exception as e:
            print("## ERROR ## ")
            print(e)
            raise serializers.ValidationError("Error al realizar la predicción")

        # predict the failure percentage
