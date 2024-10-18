from .models import Area
from .serializers import AreaSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter


class AreaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["id", "nombre", "ip", "descripcion", "estado"]
    pagination_class = LimitOffsetPagination
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


class AreaDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
