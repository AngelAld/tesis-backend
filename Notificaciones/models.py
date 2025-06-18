from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Notificacion(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificaciones"
    )
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)  # <-- Nuevo campo
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
