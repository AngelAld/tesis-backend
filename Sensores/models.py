from django.db import models
from Equipos.models import Equipo
from django.utils.timezone import now


class SensorStats(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(default=now)
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

    def __str__(self):
        return f"{self.equipo} - {self.fecha_registro}"


class FailureLogs(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(default=now)
    error = models.TextField()

    def __str__(self):
        return f"{self.equipo} - {self.fecha_registro}"
