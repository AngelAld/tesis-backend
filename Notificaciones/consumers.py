from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notificaciones_{self.user.id}"
            if self.channel_layer is not None:
                await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name") and self.channel_layer is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Aquí puedes manejar datos recibidos si necesitas.
        pass

    async def enviar_notificacion(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "id": event.get("id"),
                    "mensaje": event.get("mensaje", ""),
                    "link": event.get("link"),
                    "timestamp": event.get("timestamp"),
                }
            )
        )
