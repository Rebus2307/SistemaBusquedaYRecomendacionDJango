from rest_framework import serializers
from core.models import Usuario, LibroFavorito, PeliculaFavorita

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'apellidos', 'fecha_nacimiento', 'foto_perfil', 'password')

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

class LibroFavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibroFavorito
        fields = '__all__'

class PeliculaFavoritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeliculaFavorita
        fields = '__all__'