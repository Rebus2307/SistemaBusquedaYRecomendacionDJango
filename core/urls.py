from django.urls import path
from core.views import register_view, login_view, dashboard_view, logout_view, perfil_view, eliminar_cuenta_view, buscar_libros_view, buscar_series_view, favoritos_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
    path('eliminar-cuenta/', eliminar_cuenta_view, name='eliminar_cuenta'),
    path('buscar-libros/', buscar_libros_view, name='buscar_libros'),
    path('buscar-series/', buscar_series_view, name='buscar_series'),
    path('favoritos/', favoritos_view, name='favoritos'),
]
