from rest_framework import serializers
from core.models import (
    Usuario, Libro, Serie, LibroFavorito, PeliculaFavorita
)

# --- Usuario ---

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = (
            'email', 'nombre', 'apellidos', 'fecha_nacimiento',
            'foto_perfil', 'password'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellidos', 'fecha_nacimiento',
            'foto_perfil', 'is_staff', 'is_superuser'
        )

class UsuarioEditarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'nombre', 'apellidos', 'fecha_nacimiento', 'foto_perfil'
        )

# --- Libros y Series (Películas) ---

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'

# --- Favoritos ---

class LibroFavoritoSerializer(serializers.ModelSerializer):
    libro = LibroSerializer(read_only=True)
    class Meta:
        model = LibroFavorito
        fields = '__all__'

class PeliculaFavoritaSerializer(serializers.ModelSerializer):
    serie = SerieSerializer(read_only=True)
    class Meta:
        model = PeliculaFavorita
        fields = '__all__'

# --- Listado de usuarios para admin ---

class UsuarioAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id', 'email', 'nombre', 'apellidos', 'is_staff', 'is_superuser'
        )