from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    nombres = CharField(source="first_name")
    apellidos = CharField(source="last_name")

    class Meta:
        model = User
        fields = ["email", "nombres", "apellidos"]
