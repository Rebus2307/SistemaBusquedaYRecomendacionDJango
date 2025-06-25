from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings

# Usuario Manager
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, password, **extra_fields)

# Usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permite acceso al admin
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

# Modelo general de Libro
class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    portada_url = models.URLField(blank=True)

    def __str__(self):
        return self.titulo

# Modelo general de Serie
class Serie(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    show_id = models.IntegerField(null=True, blank=True)  # ID externo si lo usas
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        return self.titulo

# Modelo de libros favoritos
class LibroFavorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='libros_favoritos')
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    portada_url = models.URLField(blank=True)
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.usuario.email})"

# Modelo de películas favoritas
class PeliculaFavorita(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='peliculas_favoritas')
    titulo = models.CharField(max_length=255)
    show_id = models.IntegerField()  # ID del show en TVMaze
    imagen_url = models.URLField(blank=True)
    resumen = models.TextField(blank=True)
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.usuario.email})"