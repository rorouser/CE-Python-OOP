# Memoria del Proceso de Despliegue - TaskMaster

## Resumen del Despliegue

Aplicación Django desplegada en **Render** con base de datos MySQL en **Aiven**.

- **URL de producción:** https://ce-python-oop.onrender.com
- **Base de datos:** MySQL en Aiven (cloud)
- **Servidor web:** Gunicorn
- **Archivos estáticos:** WhiteNoise

---

## 1. Preparación del Proyecto

### 1.1 Dependencias de Producción

Se agregaron las siguientes dependencias al `requirements.txt`:
```txt
Django==4.2.11
pymysql==1.1.0
python-decouple==3.8
whitenoise==6.6.0
gunicorn==25.0.1
python-dotenv==1.2.1
```

**Explicación:**
- `gunicorn`: Servidor WSGI para producción (reemplaza al servidor de desarrollo)
- `whitenoise`: Servir archivos estáticos sin necesidad de nginx
- `python-decouple`: Gestión de variables de entorno

### 1.2 Configuración de Settings.py

**Cambios principales:**
```python
# Eliminamos la carga condicional de archivos .env
# Ya que Render inyecta las variables directamente

SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,.onrender.com',
    cast=Csv()
)

# WhiteNoise para archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Después de SecurityMiddleware
    # ... resto de middleware
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Base de datos MySQL en Aiven
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='25022'),
        'OPTIONS': {
            'ssl': {'ssl-mode': 'preferred'}
        }
    }
}
```

---

## 2. Configuración de Base de Datos (Aiven)

### 2.1 Creación del Servicio MySQL

1. Cuenta creada en [Aiven](https://aiven.io)
2. Servicio MySQL creado en el plan gratuito
3. Región seleccionada: Más cercana al servidor de Render


### 2.2 Certificado SSL

Aiven requiere SSL. El certificado `ca.pem` fue descargado, pero **NO se sube a producción** ya que:
- En desarrollo local: se usa el certificado descargado
- En Render: la conexión SSL se maneja con `'ssl-mode': 'preferred'`

---

## 3. Configuración de Render

### 3.1 Creación del Web Service

1. Conectado repositorio de GitHub a Render
2. Tipo de servicio: **Web Service**
3. Runtime: **Python 3**

### 3.2 Configuración del Servicio

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Explicación:**
- `pip install -r requirements.txt`: Instala dependencias
- `collectstatic --noinput`: Recopila archivos estáticos para WhiteNoise
- `migrate`: Ejecuta migraciones de base de datos

**Start Command:**
```bash
gunicorn app.wsgi:application
```

**Explicación:**
- `app.wsgi:application`: Apunta al archivo WSGI de Django
- Gunicorn sirve la aplicación en producción

### 3.3 Variables de Entorno Configuradas

En Render → Settings → Environment:


**Importante:**
- `DEBUG=False` en producción por seguridad
- `ALLOWED_HOSTS=.onrender.com` permite cualquier subdominio de render.com

---

## 4. Proceso de Despliegue

### 4.1 Primer Despliegue

**Problemas encontrados:**

#### Error 1: Archivos .env no encontrados
```
FileNotFoundError: prod.env not found
```

**Solución:** 
Eliminamos la lógica de carga condicional de archivos `.env` porque Render inyecta las variables directamente.

#### Error 2: Directorio staticfiles no existe
```
UserWarning: No directory at: /opt/render/project/src/staticfiles/
```

**Solución:** 
Agregamos `collectstatic --noinput` al Build Command.

#### Error 3: Error 500 en /login/
```
GET /login/?next=/ HTTP/1.1" 500
```

**Causa:** Combinación de problemas anteriores más configuración incorrecta de `ALLOWED_HOSTS`.

**Solución:** Ajustamos settings.py para leer variables de entorno directamente.

### 4.2 Despliegue Exitoso

Después de los ajustes:
```
==> Build successful 🎉
==> Deploying...
==> Running 'gunicorn app.wsgi:application --bind 0.0.0.0:$PORT'
==> Your service is live 🎉
```

---

## 5. Arquitectura Final
```
┌─────────────────┐
│   Render.com    │
│   (Gunicorn)    │
│   Puerto 10000  │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│  Django 4.2.11  │
│  + WhiteNoise   │
└────────┬────────┘
         │
         │ MySQL
         │ SSL/TLS
         │
┌────────▼────────┐
│  Aiven MySQL    │
│  Puerto 25022   │
└─────────────────┘
```

**URL:** https://ce-python-oop.onrender.com