# TaskMaster - Gestor de Tareas y Proyectos

Sistema de gestión de tareas y proyectos desarrollado con Django 4.2.11 y MySQL.

## Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.12 (si quieres ejecutar sin Docker)
- Cuenta en Aiven con base de datos MySQL configurada

## Configuración Inicial

### 1. Clonar el repositorio
```bash
git clone https://github.com/rorouser/CE-Python-OOP.git
cd task_master
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:
```env
DJANGO_SECRET_KEY=clave-secreta-para-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=tu-password-aiven
DB_HOST=mysql-xxxxx.aivencloud.com
DB_PORT=25022
```

### 3. Configurar certificado SSL de Aiven

Descarga el certificado `ca.pem` desde tu panel de Aiven y colócalo en la raíz del proyecto (mismo nivel que `manage.py`).

## Ejecución con Docker (Recomendado)

### 1. Construir y levantar los contenedores
```bash
docker-compose up --build
```

### 2. Ejecutar migraciones

En otra terminal:
```bash
docker-compose exec web python manage.py migrate
```

### 3. Crear superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. (Opcional) Poblar base de datos con datos de prueba
```bash
docker-compose exec web python populate_tasks.py
```

### 5. Acceder a la aplicación

- Aplicación: http://localhost:8081
- Panel admin: http://localhost:8081/admin

## Ejecución sin Docker

### 1. Crear entorno virtual
```bash
python -m venv .venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo
```bash
python manage.py runserver 8081
```

### 7. Acceder a la aplicación

- Aplicación: http://localhost:8081
- Panel admin: http://localhost:8081/admin

## Comandos Útiles

### Docker
```bash
# Desplegar con Docker Compose
docker-compose up --build

# Detener contenedores
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar contenedores
docker-compose restart

# Ejecutar comandos Django
docker-compose exec web python manage.py <comando>

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate
```

### Sin Docker
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell de Django
python manage.py shell

# Colectar archivos estáticos
python manage.py collectstatic
```