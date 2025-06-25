from rest_framework.routers import DefaultRouter
from django.urls import path
from . import api_views
from .api_views import UsuarioViewSet, LibroFavoritoViewSet, PeliculaFavoritaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'libros-favoritos', LibroFavoritoViewSet)
router.register(r'peliculas-favoritas', PeliculaFavoritaViewSet)

urlpatterns = router.urls + [
    path('buscar-libros/', api_views.buscar_libros, name='api_buscar_libros'),
    path('buscar-series/', api_views.buscar_series, name='api_buscar_series'),
    path('mis-favoritos/', api_views.mis_favoritos, name='api_mis_favoritos'),
    path('listar-usuarios/', api_views.listar_usuarios, name='api_listar_usuarios'),
]