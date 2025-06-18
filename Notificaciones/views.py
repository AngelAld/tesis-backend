from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notificacion
from .serializers import NotificacionSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    no_leidas = notificaciones.filter(leido=False)
    leidas = notificaciones.filter(leido=True)
    return Response(
        {
            "no_leidas": NotificacionSerializer(no_leidas, many=True).data,
            "leidas": NotificacionSerializer(leidas, many=True).data,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def marcar_como_leida(request, pk):
    try:
        notificacion = Notificacion.objects.get(pk=pk, usuario=request.user)
        notificacion.leido = True
        notificacion.save()
        return Response({"success": True})
    except Notificacion.DoesNotExist:
        return Response(
            {"error": "Notificación no encontrada"}, status=status.HTTP_404_NOT_FOUND
        )
