from rest_framework import viewsets, permissions
from .models import Usuario, LibroFavorito, PeliculaFavorita
from .serializers import UsuarioSerializer, UsuarioRegistroSerializer, LibroFavoritoSerializer, PeliculaFavoritaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioRegistroSerializer
        return UsuarioSerializer

class LibroFavoritoViewSet(viewsets.ModelViewSet):
    queryset = LibroFavorito.objects.all()
    serializer_class = LibroFavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PeliculaFavoritaViewSet(viewsets.ModelViewSet):
    queryset = PeliculaFavorita.objects.all()
    serializer_class = PeliculaFavoritaSerializer
    permission_classes = [permissions.IsAuthenticated]