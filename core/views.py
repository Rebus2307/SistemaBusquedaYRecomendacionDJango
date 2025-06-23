from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django import forms

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
            print("❌ Errores del formulario:", form.errors)  # 👈 Esto ayuda a depurar
    else:
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})
    # 👆 Siempre retorna el formulario con errores si POST no es válido


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
