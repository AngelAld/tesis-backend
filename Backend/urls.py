"""
URL configuration for Backend project.

"""

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from Areas import urls as AreasUrls
from Equipos import urls as EquiposUrls
from Sensores import urls as SensoresUrls
from Usuarios import urls as UsuariosUrls
from IA import urls as IAUrls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="docs "),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("admin/", admin.site.urls),
    path("areas/", include(AreasUrls)),
    path("equipos/", include(EquiposUrls)),
    path("sensores/", include(SensoresUrls)),
    path("auth/", include(UsuariosUrls)),
    path("ai/", include(IAUrls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
