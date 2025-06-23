from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from .forms import PerfilForm  # Agregamos el formulario de perfil
from .models import LibroFavorito, PeliculaFavorita

Usuario = get_user_model()


# Formulario personalizado de registro
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellidos', 'foto_perfil', 'password']


# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            login(request, usuario)
            return redirect('dashboard')
        else:
            print("❌ Errores del formulario:", form.errors)  # Ayuda a depurar
    else:
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})


# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


# Vista protegida (dashboard)
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'core/dashboard.html')


# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Vista de perfil (ver y editar)
@login_required
def perfil_view(request):
    usuario = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('perfil')
    else:
        form = PerfilForm(instance=usuario)
    return render(request, 'core/perfil.html', {
        'form': form,
        'usuario': usuario
    })


# Vista de eliminar cuenta
@login_required
def eliminar_cuenta_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada.")
        return redirect('login')
    return render(request, 'core/confirmar_eliminar.html')


# Vista de búsqueda de libros (simple, por ahora)
@login_required
def buscar_libros_view(request):
    libros = [
        {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez'},
        {'titulo': 'El alquimista', 'autor': 'Paulo Coelho'},
    ]
    return render(request, 'core/buscar_libros.html', {'libros': libros})


# Vista de búsqueda de series (simulada)
@login_required
def buscar_series_view(request):
    series = [
        {'titulo': 'Stranger Things', 'genero': 'Ciencia ficción'},
        {'titulo': 'Breaking Bad', 'genero': 'Drama'},
    ]
    return render(request, 'core/buscar_series.html', {'series': series})


# Vista de favoritos (libros y series)
@login_required
def favoritos_view(request):
    libros_favoritos = LibroFavorito.objects.filter(usuario=request.user)
    peliculas_favoritas = PeliculaFavorita.objects.filter(usuario=request.user)
    return render(request, 'core/favoritos.html', {
        'libros_favoritos': libros_favoritos,
        'peliculas_favoritas': peliculas_favoritas
    })
