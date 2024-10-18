tengo estos modelos de django:

````python
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
```

quiero un serializer de django rest framework que me dé los siguientes datos:

 ```json
{
    "id": 1,
    "hostname": "hostname",
    "ip": "192.168.1.20",
    "last_update": "2021-08-01 12:00:00",
    "estado_equipo": "bueno",
    "estado_alerta": "sin alertas",
    "sensores":{
        "cpu": {
            "temperatura": 80,
            "subiendo": "true"
        },
        "memoria": {
            "usada": 80,
            "subiendo": "true"
        },
        "disco": {
            "usado": 70,
            "subiendo": "false"
        }
    }
}
```