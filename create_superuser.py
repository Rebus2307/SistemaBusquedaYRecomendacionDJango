import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from core.models import Usuario

email = "rebus@gmail.com"
nombre = "Rebus"
password = "23072003"

if not Usuario.objects.filter(email=email).exists():
    Usuario.objects.create_superuser(email=email, nombre=nombre, password=password)
    print("✅ Superusuario creado: rebus@gmail.com / 23072003")
else:
    print("ℹ️ El superusuario ya existe: rebus@gmail.com")
