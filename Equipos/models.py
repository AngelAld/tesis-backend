from django.db import models
from django.utils.timezone import now


class EstadoEquipo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class EstadoAlerta(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class EstadoHardware(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Area(models.Model):
    nombre = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    hostname = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(default=now)
    last_update = models.DateTimeField(default=now)
    estado_equipo = models.ForeignKey(EstadoEquipo, on_delete=models.PROTECT)
    estado_alerta = models.ForeignKey(EstadoAlerta, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.hostname} - {self.ip} - {self.area.nombre}"


class Cpu(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="cpu_set")
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(EstadoHardware, on_delete=models.PROTECT)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.equipo.hostname} - {self.nombre}"


class Memory(models.Model):
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name="memory_set"
    )
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(EstadoHardware, on_delete=models.PROTECT)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.equipo.hostname} - {self.nombre}"


class Disk(models.Model):
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name="disk_set"
    )
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(EstadoHardware, on_delete=models.PROTECT)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.equipo.hostname} - {self.nombre}"
