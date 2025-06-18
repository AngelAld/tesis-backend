from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notificacion
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Notificacion)
def notificacion_creada(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            group_name = f"notificaciones_{instance.usuario.id}"
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "enviar_notificacion",
                    "id": instance.id,  # Agrega el id
                    "mensaje": instance.mensaje,
                    "link": instance.link,  # Si tienes este campo
                    "timestamp": (
                        instance.timestamp.isoformat()
                        if hasattr(instance, "timestamp")
                        else None
                    ),
                },
            )
