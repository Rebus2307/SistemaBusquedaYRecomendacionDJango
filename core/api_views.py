import requests
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Libro, Serie, Usuario, LibroFavorito, PeliculaFavorita
from .serializers import (
    LibroSerializer,
    SerieSerializer,
    UsuarioAdminListSerializer,
    UsuarioSerializer,
    UsuarioRegistroSerializer,
    LibroFavoritoSerializer,
    PeliculaFavoritaSerializer,
)

# Buscar libros en OpenLibrary
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_libros(request):
    q = request.GET.get('q', '')
    if not q:
        return Response([])
    url = f'https://openlibrary.org/search.json?q={q}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response([])
    data = r.json()
    resultados = []
    for doc in data.get('docs', []):
        resultados.append({
            'titulo': doc.get('title', ''),
            'autor': ', '.join(doc.get('author_name', [])) if doc.get('author_name') else '',
            'isbn': doc.get('isbn', [''])[0] if doc.get('isbn') else '',
            'portada_url': f"https://covers.openlibrary.org/b/isbn/{doc.get('isbn', [''])[0]}-M.jpg" if doc.get('isbn') else '',
        })
    return Response(resultados)

# Buscar series en TVMaze
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_series(request):
    q = request.GET.get('q', '')
    if not q:
        return Response([])
    url = f'https://api.tvmaze.com/search/shows?q={q}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response([])
    data = r.json()
    resultados = []
    for item in data:
        show = item.get('show', {})
        resultados.append({
            'titulo': show.get('name', ''),
            'descripcion': show.get('summary', ''),
            'show_id': show.get('id', ''),
            'imagen_url': show.get('image', {}).get('medium', '') if show.get('image') else '',
        })
    return Response(resultados)

# Mostrar favoritos del usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_favoritos(request):
    libros = request.user.librofavorito_set.all()
    series = request.user.peliculafavorita_set.all()
    return Response({
        "libros": LibroFavoritoSerializer(libros, many=True).data,
        "series": PeliculaFavoritaSerializer(series, many=True).data,
    })

# Listar usuarios (solo admin)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuarios(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return Response({'detail': 'No autorizado'}, status=403)
    usuarios = Usuario.objects.all()
    serializer = UsuarioAdminListSerializer(usuarios, many=True)
    return Response(serializer.data)

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