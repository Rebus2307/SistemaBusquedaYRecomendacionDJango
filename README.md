# 📚🔎 Sistema de Búsqueda y Recomendación Django 🎬✨

Este proyecto es una aplicación web desarrollada con **Django** que permite a los usuarios buscar y recibir recomendaciones de **libros** y **series**, así como guardar sus favoritos. Fue creado como parte de la materia de Ingeniería de Software en **ESCOM**.

---

## 🚀 ¿Qué hace este sistema?

- 🔐 Registro y autenticación de usuarios.
- 👤 Edición de perfil y foto de usuario.
- 📚 Búsqueda de libros (usando la API de OpenLibrary).
- 🎬 Búsqueda de series (usando la API de TVMaze).
- ⭐ Guardar libros y series como favoritos.
- 🤖 Recomendaciones personalizadas según tus favoritos.
- 🛡️ Panel de administración para gestionar usuarios (solo administradores).

---

## 🧰 Requisitos

- [Docker](https://www.docker.com/) 🐳
- [Docker Compose](https://docs.docker.com/compose/) ⚙️

---

## ⚡ Instalación y ejecución

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/SistemaBusquedaYRecomendacionDJango.git
   cd SistemaBusquedaYRecomendacionDJango
   ```

2. **Ejecuta el proyecto con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Accede a la aplicación:**
   - Abre tu navegador y entra a: [http://localhost:8000/login/](http://localhost:8000/login/)

---

## 📝 Notas

- El sistema crea la base de datos y las migraciones automáticamente al iniciar.
- Puedes crear un usuario administrador para acceder al panel de usuarios.
- Las imágenes y archivos estáticos se gestionan automáticamente en los contenedores.

---

## 👨‍💻 Autor

Proyecto realizado para la materia de Ingeniería de Software en **ESCOM**.

---

¡Disfruta explorando y recomendando libros y series!