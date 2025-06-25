from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # Redirección automática
    path('', include('core.urls')),
    path('api/', include('core.api_urls')),  # Asegúrate de tener este include para tus rutas de API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Ruta para obtener el token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # Ruta para refrescar el token
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)