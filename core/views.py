import requests  # Asegúrate de importar el módulo requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from .forms import PerfilForm  # Asegúrate de que este formulario esté definido
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


# Vista de búsqueda de libros (por título o autor)
@login_required
def buscar_libros_view(request):
    query = request.GET.get('q', '')
    libros = []

    if query:
        # Busca por título
        response = requests.get(f'https://openlibrary.org/search.json?q={query}')
        if response.status_code == 200:
            libros = response.json().get('docs', [])
        
        # O busca por autor
        response_author = requests.get(f'https://openlibrary.org/search.json?author={query}')
        if response_author.status_code == 200:
            libros += response_author.json().get('docs', [])

    return render(request, 'core/buscar_libros.html', {'libros': libros, 'query': query})


# Vista de búsqueda de series
@login_required
def buscar_series_view(request):
    query = request.GET.get('q', '')
    series = []

    if query:
        response = requests.get(f'https://api.tvmaze.com/search/shows?q={query}')
        if response.status_code == 200:
            series = response.json()

    return render(request, 'core/buscar_series.html', {'series': series, 'query': query})


# Vista de agregar libro a favoritos
@login_required
def agregar_favorito_libro(request, libro_id):
    if request.method == 'POST':
        response = requests.get(f'https://openlibrary.org/works/{libro_id}.json')
        if response.status_code == 200:
            data = response.json()
            titulo = data.get('title')
            autor = ', '.join([author['name'] for author in data.get('authors', [])])
            isbn = data.get('isbn', [''])[0]
            portada_url = f"http://covers.openlibrary.org/b/id/{data.get('covers', [None])[0]}-L.jpg" if data.get('covers') else None
            LibroFavorito.objects.create(usuario=request.user, titulo=titulo, autor=autor, isbn=isbn, portada_url=portada_url)
            messages.success(request, f"El libro {titulo} ha sido agregado a tus favoritos.")
    return redirect('buscar_libros')


# Vista de agregar película a favoritos
@login_required
def agregar_favorito_pelicula(request, serie_id):
    if request.method == 'POST':
        response = requests.get(f'https://api.tvmaze.com/shows/{serie_id}')
        if response.status_code == 200:
            data = response.json()
            titulo = data.get('name')
            imagen_url = data.get('image', {}).get('original', None)
            resumen = data.get('summary', '')
            PeliculaFavorita.objects.create(usuario=request.user, titulo=titulo, show_id=serie_id, imagen_url=imagen_url, resumen=resumen)
            messages.success(request, f"La serie {titulo} ha sido agregada a tus favoritos.")
    return redirect('buscar_series')


# Vista de favoritos (libros y series)
@login_required
def favoritos_view(request):
    libros_favoritos = LibroFavorito.objects.filter(usuario=request.user)
    peliculas_favoritas = PeliculaFavorita.objects.filter(usuario=request.user)
    return render(request, 'core/favoritos.html', {
        'libros_favoritos': libros_favoritos,
        'peliculas_favoritas': peliculas_favoritas
    })
