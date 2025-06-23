import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import logging
from .forms import PerfilForm
from .models import LibroFavorito, PeliculaFavorita

# Configurar logging
logger = logging.getLogger(__name__)

Usuario = get_user_model()

# Formulario personalizado de registro
class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellidos', 'foto_perfil', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                usuario.set_password(form.cleaned_data['password'])
                usuario.save()
                login(request, usuario)
                messages.success(request, f'¡Bienvenido {usuario.nombre}! Tu cuenta ha sido creada exitosamente.')
                return redirect('dashboard')
            except Exception as e:
                logger.error(f"Error al crear usuario: {e}")
                messages.error(request, 'Ocurrió un error al crear tu cuenta. Inténtalo de nuevo.')
        else:
            logger.warning(f"Errores en el formulario de registro: {form.errors}")
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
            messages.success(request, f'¡Bienvenido de nuevo, {usuario.nombre}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas. Verifica tu email y contraseña.')
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
    messages.info(request, 'Has cerrado sesión exitosamente.')
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
            messages.error(request, "Por favor corrige los errores en el formulario.")
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
        usuario_nombre = request.user.nombre
        request.user.delete()
        messages.success(request, f"La cuenta de {usuario_nombre} ha sido eliminada exitosamente.")
        return redirect('login')
    return render(request, 'core/confirmar_eliminar.html')

# Vista de búsqueda de libros (versión mejorada en core/views.py)
@login_required
def buscar_libros_view(request):
    query = request.GET.get('q', '').strip()
    libros = []
    
    if query:
        try:
            # Buscar en Open Library API
            url = f'https://openlibrary.org/search.json'
            params = {
                'q': query,
                'limit': 20,
                'fields': 'key,title,author_name,first_publish_year,isbn,cover_i,subject'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            docs = data.get('docs', [])
            
            # Procesar los resultados
            for doc in docs:
                # Construir URL de la portada
                cover_url = None
                if doc.get('cover_i'):
                    cover_url = f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg"
                
                libro = {
                    'key': doc.get('key', '').replace('/works/', ''),
                    'title': doc.get('title', 'Título no disponible'),
                    'author': ', '.join(doc.get('author_name', [])) or 'Autor desconocido',
                    'first_publish_year': doc.get('first_publish_year', ''),
                    'isbn': doc.get('isbn', [''])[0] if doc.get('isbn') else '',
                    'cover_url': cover_url,  # Esta es la clave importante
                    'subjects': ', '.join(doc.get('subject', [])[:3]) if doc.get('subject') else ''
                }
                libros.append(libro)
                
        except requests.RequestException as e:
            logger.error(f"Error al buscar libros: {e}")
            messages.error(request, 'Error al conectar con el servicio de búsqueda de libros.')
        except Exception as e:
            logger.error(f"Error inesperado en búsqueda de libros: {e}")
            messages.error(request, 'Ocurrió un error inesperado en la búsqueda.')

    return render(request, 'core/buscar_libros.html', {
        'libros': libros, 
        'query': query
    })

# Vista de búsqueda de series
@login_required
def buscar_series_view(request):
    query = request.GET.get('q', '').strip()
    series = []
    
    if query:
        try:
            # Buscar en TVMaze API
            url = f'https://api.tvmaze.com/search/shows'
            params = {'q': query}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Procesar los resultados
            for item in data:
                show = item.get('show', {})
                serie = {
                    'id': show.get('id'),
                    'name': show.get('name', 'Nombre no disponible'),
                    'genres': show.get('genres', []),
                    'premiered': show.get('premiered', ''),
                    'rating': show.get('rating', {}).get('average', 'N/A'),
                    'summary': show.get('summary', ''),
                    'image': show.get('image', {}).get('medium') if show.get('image') else None,
                    'network': show.get('network', {}).get('name', '') if show.get('network') else '',
                    'status': show.get('status', '')
                }
                series.append(serie)
                
        except requests.RequestException as e:
            logger.error(f"Error al buscar series: {e}")
            messages.error(request, 'Error al conectar con el servicio de búsqueda de series.')
        except Exception as e:
            logger.error(f"Error inesperado en búsqueda de series: {e}")
            messages.error(request, 'Ocurrió un error inesperado en la búsqueda.')

    return render(request, 'core/buscar_series.html', {
        'series': series, 
        'query': query
    })


# Vista de agregar libro a favoritos
@login_required
def agregar_favorito_libro(request, libro_id):
    if request.method == 'POST':
        try:
            # Verificar si ya existe en favoritos
            if LibroFavorito.objects.filter(usuario=request.user, isbn=libro_id).exists():
                messages.warning(request, 'Este libro ya está en tus favoritos.')
                return redirect('buscar_libros')
            
            # Obtener información del libro desde la API
            url = f'https://openlibrary.org/works/{libro_id}.json'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer información del libro
                titulo = data.get('title', 'Título no disponible')
                
                # Obtener información de autores
                autor = 'Autor desconocido'
                if 'authors' in data:
                    try:
                        authors_info = []
                        for author_ref in data['authors']:
                            if 'author' in author_ref:
                                author_key = author_ref['author']['key']
                                author_response = requests.get(f'https://openlibrary.org{author_key}.json', timeout=5)
                                if author_response.status_code == 200:
                                    author_data = author_response.json()
                                    authors_info.append(author_data.get('name', 'Autor desconocido'))
                        if authors_info:
                            autor = ', '.join(authors_info)
                    except Exception as e:
                        logger.warning(f"Error al obtener información de autores: {e}")
                
                # Obtener portada
                portada_url = None
                if 'covers' in data and data['covers']:
                    cover_id = data['covers'][0]
                    portada_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                
                # Crear el favorito
                LibroFavorito.objects.create(
                    usuario=request.user,
                    titulo=titulo,
                    autor=autor,
                    isbn=libro_id,  # Usar el libro_id como ISBN
                    portada_url=portada_url
                )
                
                messages.success(request, f'"{titulo}" ha sido agregado a tus favoritos.')
            else:
                messages.error(request, 'No se pudo obtener la información del libro.')
                
        except requests.RequestException as e:
            logger.error(f"Error al agregar libro a favoritos: {e}")
            messages.error(request, 'Error al conectar con el servicio de libros.')
        except Exception as e:
            logger.error(f"Error inesperado al agregar libro: {e}")
            messages.error(request, 'Ocurrió un error al agregar el libro a favoritos.')
    
    return redirect('buscar_libros')


# Vista de agregar serie a favoritos
@login_required
def agregar_favorito_pelicula(request, serie_id):
    if request.method == 'POST':
        try:
            # Verificar si ya existe en favoritos
            if PeliculaFavorita.objects.filter(usuario=request.user, show_id=serie_id).exists():
                messages.warning(request, 'Esta serie ya está en tus favoritos.')
                return redirect('buscar_series')
            
            # Obtener información de la serie desde la API
            url = f'https://api.tvmaze.com/shows/{serie_id}'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                titulo = data.get('name', 'Título no disponible')
                imagen_url = data.get('image', {}).get('original') if data.get('image') else None
                resumen = data.get('summary', '')
                
                # Crear el favorito
                PeliculaFavorita.objects.create(
                    usuario=request.user,
                    titulo=titulo,
                    show_id=serie_id,
                    imagen_url=imagen_url,
                    resumen=resumen
                )
                
                messages.success(request, f'"{titulo}" ha sido agregada a tus favoritos.')
            else:
                messages.error(request, 'No se pudo obtener la información de la serie.')
                
        except requests.RequestException as e:
            logger.error(f"Error al agregar serie a favoritos: {e}")
            messages.error(request, 'Error al conectar con el servicio de series.')
        except Exception as e:
            logger.error(f"Error inesperado al agregar serie: {e}")
            messages.error(request, 'Ocurrió un error al agregar la serie a favoritos.')
    
    return redirect('buscar_series')


# Vista de favoritos (libros y series)
@login_required
def favoritos_view(request):
    usuario = request.user
    libros_favoritos = LibroFavorito.objects.filter(usuario=usuario)
    series_favoritas = PeliculaFavorita.objects.filter(usuario=usuario)

    # Recomendaciones de libros (por autor del primer favorito)
    recomendaciones_libros = []
    if libros_favoritos.exists():
        autor = libros_favoritos.first().autor
        url = f"https://openlibrary.org/search.json?author={autor}"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            for doc in data.get("docs", [])[:5]:
                recomendaciones_libros.append({
                    "titulo": doc.get("title"),
                    "autor": ", ".join(doc.get("author_name", [])),
                    "portada": f"https://covers.openlibrary.org/b/olid/{doc.get('cover_edition_key', '')}-M.jpg" if doc.get("cover_edition_key") else "",
                })

    # Recomendaciones de series (por género del primer favorito)
    recomendaciones_series = []
    if series_favoritas.exists():
        show_id = series_favoritas.first().show_id
        show_resp = requests.get(f"https://api.tvmaze.com/shows/{show_id}")
        if show_resp.status_code == 200:
            show_data = show_resp.json()
            if show_data.get("genres"):
                genre = show_data["genres"][0]
                genre_resp = requests.get(f"https://api.tvmaze.com/search/shows?q={genre}")
                if genre_resp.status_code == 200:
                    for item in genre_resp.json()[:5]:
                        show = item["show"]
                        recomendaciones_series.append({
                            "titulo": show["name"],
                            "imagen": show["image"]["medium"] if show.get("image") else "",
                            "resumen": show.get("summary", ""),
                        })

    return render(request, "core/favoritos.html", {
        "libros_favoritos": libros_favoritos,
        "series_favoritas": series_favoritas,
        "recomendaciones_libros": recomendaciones_libros,
        "recomendaciones_series": recomendaciones_series,
    })