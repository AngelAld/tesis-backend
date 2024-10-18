import csv
import os
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings

from Sensores.models import DataSet, SensorStats


def dump_data(modelo, fecha_inicio, fecha_fin, nombre):
    # Filtrar los datos
    data = SensorStats.objects.filter(
        equipo__modelo=modelo,
        fecha_registro__gte=fecha_inicio,
        fecha_registro__lte=fecha_fin,
    )

    # Crear un nombre de archivo único
    filename = f"{nombre}_{timezone.now().date()}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Generar el CSV y guardarlo en un archivo
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "fecha_registro",
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
            ]
        )  # Escribir encabezados

        # Escribir filas en el CSV
        for (
            row
        ) in data.iterator():  # Usar iterator() para manejar grandes conjuntos de datos
            writer.writerow(
                [
                    row.fecha_registro,
                    row.cpu_total_load,
                    row.cpu_core_max_load,
                    row.cpu_core_max_temp,
                    row.cpu_core_avg_temp,
                    row.cpu_avg_core_clock,
                    row.cpu_bus_speed_clock,
                    row.cpu_package_power,
                    row.cpu_cores_power,
                    row.cpu_memory_power,
                    row.cpu_core_voltage,
                    row.memory_load,
                    row.memory_available,
                    row.memory_used,
                    row.avg_used_space,
                    row.avg_read,
                    row.avg_write,
                    row.avg_activity,
                    row.max_used_space,
                    row.max_read,
                    row.max_write,
                    row.max_activity,
                ]
            )  # Escribir cada fila

    # Guardar la instancia del modelo DumpModel
    dump_instance = DataSet(
        modelo=modelo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )
    dump_instance.csv.save(
        filename, ContentFile(open(file_path, "rb").read())
    )  # Guardar el archivo en el modelo
    dump_instance.save()

    # Eliminar el archivo CSV
    os.remove(file_path)

    # Retornar la URL del archivo CSV
    return dump_instance.csv.url  # O usa dump_instance.csv.name si prefieres
