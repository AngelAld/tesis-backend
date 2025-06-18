from django.core.management.base import BaseCommand
from ...models import Notificacion
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Envía una notificación"

    def handle(self, *args, **options):
        # Obtén todos los usuarios
        usuarios = User.objects.all()
        for usuario in usuarios:
            # Crea una notificación para cada usuario
            notificacion = Notificacion(
                usuario=usuario,
                mensaje="Esta es una notificación de prueba",
                leido=False,
                timestamp=timezone.now(),
            )
            notificacion.save()
            self.stdout.write(
                self.style.SUCCESS(f"Notificación enviada a {usuario.username}")
            )
