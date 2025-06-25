from rest_framework import viewsets, permissions
from .models import Usuario, LibroFavorito, SerieFavorita
from .serializers import UsuarioSerializer, LibroFavoritoSerializer, SerieFavoritaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class LibroFavoritoViewSet(viewsets.ModelViewSet):
    queryset = LibroFavorito.objects.all()
    serializer_class = LibroFavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

class SerieFavoritaViewSet(viewsets.ModelViewSet):
    queryset = SerieFavorita.objects.all()
    serializer_class = SerieFavoritaSerializer
    permission_classes = [permissions.IsAuthenticated]