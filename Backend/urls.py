"""
URL configuration for Backend project.

"""

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from Equipos import urls as EquiposUrls
from Sensores import urls as SensoresUrls

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="docs "),
    path("admin/", admin.site.urls),
    path("equipos/", include(EquiposUrls)),
    path("sensores/", include(SensoresUrls)),
]
