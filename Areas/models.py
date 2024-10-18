from django.db import models


# Create your models here.
class Area(models.Model):
    nombre = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
