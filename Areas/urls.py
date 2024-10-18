from .views import AreaListView, AreaDetailView
from django.urls import path

urlpatterns = [
    path("lista/", AreaListView.as_view(), name="lista de areas"),
    path("<int:pk>/", AreaDetailView.as_view(), name="detalle de area"),
]
