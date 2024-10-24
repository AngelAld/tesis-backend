from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
