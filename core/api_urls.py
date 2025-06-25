from rest_framework.routers import DefaultRouter
from .api_views import UsuarioViewSet, LibroFavoritoViewSet, PeliculaFavoritaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'libros-favoritos', LibroFavoritoViewSet)
router.register(r'peliculas-favoritas', PeliculaFavoritaViewSet)

urlpatterns = router.urls