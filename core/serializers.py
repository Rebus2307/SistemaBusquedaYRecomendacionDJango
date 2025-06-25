from rest_framework import serializers
from core.models import Usuario, LibroFavorito, SerieFavorita

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
        fields = ('id', 'email', 'nombre', 'apellidos', 'fecha_nacimiento', 'foto_perfil')

class LibroFavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibroFavorito
        fields = '__all__'

class SerieFavoritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerieFavorita
        fields = '__all__'