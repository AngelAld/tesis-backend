from django.contrib import admin
from .models import (
    Equipo,
    EstadoAlerta,
    EstadoEquipo,
    EstadoHardware,
    Area,
    Cpu,
    Memory,
    Disk,
    Modelo,
)

admin.site.register(Equipo)
admin.site.register(EstadoAlerta)
admin.site.register(EstadoEquipo)
admin.site.register(EstadoHardware)
admin.site.register(Area)
admin.site.register(Cpu)
admin.site.register(Memory)
admin.site.register(Disk)
admin.site.register(Modelo)
