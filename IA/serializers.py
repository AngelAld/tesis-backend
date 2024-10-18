from pyexpat import model
from rest_framework import serializers
from .models import ModeloIA, Prediccion
import tensorflow as tf
import numpy as np


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
        modelo_equipo = validated_data.pop("modelo_equipo")
        equipo = validated_data.pop("equipo")
        try:
            tf_model = tf.keras.models.load_model(modelIA.archivo.path)  # type: ignore
            variable_objetivo = modelIA.variable_objetivo
            expected_value = validated_data.pop(variable_objetivo)

            variables_entrada = [
                validated_data.get(field) for field in validated_data.keys()
            ]

            input_values = np.array(variables_entrada, dtype=float).reshape(1, -1)

            predicted_value = tf_model.predict([input_values])[0][0]

            failure_percentage = abs(expected_value - predicted_value) / expected_value

            validated_data["failure_percentage"] = failure_percentage

            validated_data["modelo_equipo"] = modelo_equipo

            validated_data["is_manual"] = True

            validated_data[variable_objetivo] = expected_value

            validated_data["modelo_ia"] = modelIA

            validated_data["equipo"] = equipo

            instance = Prediccion.objects.create(**validated_data)

            print("## PREDICTION ##")
            print(f"Expected Value: {expected_value}")
            print(f"Predicted Value: {predicted_value}")
            print(f"Failure Percentage: {failure_percentage}")

            return instance
        except Exception as e:
            print("## ERROR ## ")
            print(e)
            raise serializers.ValidationError("Error al realizar la predicción")

        # predict the failure percentage
