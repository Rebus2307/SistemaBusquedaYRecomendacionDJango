from rest_framework import viewsets, permissions
from .models import Usuario, LibroFavorito, PeliculaFavorita
from .serializers import UsuarioSerializer, UsuarioRegistroSerializer, LibroFavoritoSerializer, PeliculaFavoritaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class LibroFavoritoViewSet(viewsets.ModelViewSet):
    queryset = LibroFavorito.objects.all()
    serializer_class = LibroFavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PeliculaFavoritaViewSet(viewsets.ModelViewSet):
    queryset = PeliculaFavorita.objects.all()
    serializer_class = PeliculaFavoritaSerializer
    permission_classes = [permissions.IsAuthenticated]