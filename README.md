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

## 💻​ Capturas

![Login](https://github.com/user-attachments/assets/d86c0ad9-eab0-4a44-9252-31d295a7ae77)
![Register](https://github.com/user-attachments/assets/da819bed-e69b-449a-8409-46b1f16e4050)
![Dashboard](https://github.com/user-attachments/assets/0f3a935d-951d-414f-b890-e41af174de6d)
![BuscarLibros](https://github.com/user-attachments/assets/7cf72481-07a4-49be-afc7-5babc2ee53bc)
![FavoritosYRecomendaciones](https://github.com/user-attachments/assets/4998718f-1891-412e-9a43-a836ab5fe872)

---

## 👨‍💻 Autor

Proyecto realizado para la materia de Ingeniería de Software en **ESCOM**.

---

¡Disfruta explorando y recomendando libros y series!
