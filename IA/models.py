from django.db import models
from Equipos.models import Equipo, Modelo

cpu_columns = [
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
]
mem_columns = [
    "cpu_total_load",
    "cpu_core_max_temp",
    "cpu_core_avg_temp",
    "cpu_avg_core_clock",
    "memory_load",
    "memory_available",
    "memory_used",
]
disk_columns = [
    "avg_used_space",
    "avg_read",
    "avg_write",
    "avg_activity",
    "max_used_space",
    "max_read",
    "max_write",
    "max_activity",
]


class ModeloIA(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to="modelos/")
    scaler = models.FileField(upload_to="modelos/", null=True, blank=True)
    modelo_equipo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    variable_objetivo = models.CharField(max_length=100)
    componente = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.modelo_equipo.nombre}"


class Prediccion(models.Model):
    modelo_ia = models.ForeignKey(ModeloIA, on_delete=models.CASCADE)
    modelo_equipo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cpu_total_load = models.FloatField()
    cpu_core_max_load = models.FloatField()
    cpu_core_max_temp = models.FloatField()
    cpu_core_avg_temp = models.FloatField()
    cpu_avg_core_clock = models.FloatField()
    cpu_bus_speed_clock = models.FloatField()
    cpu_package_power = models.FloatField()
    cpu_cores_power = models.FloatField()
    cpu_memory_power = models.FloatField()
    cpu_core_voltage = models.FloatField()
    memory_load = models.FloatField()
    memory_available = models.FloatField()
    memory_used = models.FloatField()
    avg_used_space = models.FloatField()
    avg_read = models.FloatField()
    avg_write = models.FloatField()
    avg_activity = models.FloatField()
    max_used_space = models.FloatField()
    max_read = models.FloatField()
    max_write = models.FloatField()
    max_activity = models.FloatField()
    failure_percentage = models.FloatField()
    is_manual = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.modelo_ia} - {self.fecha_creacion}"
