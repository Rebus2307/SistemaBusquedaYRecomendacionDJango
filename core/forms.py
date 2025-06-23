from django import forms
from .models import Usuario

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'foto_perfil']