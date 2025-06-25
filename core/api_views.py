from rest_framework import viewsets, permissions
from .models import Usuario, LibroFavorito, PeliculaFavorita
from .serializers import UsuarioSerializer, LibroFavoritoSerializer, PeliculaFavoritaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class LibroFavoritoViewSet(viewsets.ModelViewSet):
    queryset = LibroFavorito.objects.all()
    serializer_class = LibroFavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PeliculaFavoritaViewSet(viewsets.ModelViewSet):
    queryset = PeliculaFavorita.objects.all()
    serializer_class = PeliculaFavoritaSerializer
    permission_classes = [permissions.IsAuthenticated]