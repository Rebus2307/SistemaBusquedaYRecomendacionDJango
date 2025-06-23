from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, LibroFavorito, PeliculaFavorita

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'nombre', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'nombre')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellidos', 'fecha_nacimiento', 'foto_perfil')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(LibroFavorito)
admin.site.register(PeliculaFavorita)
