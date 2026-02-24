# FastAPI EventMaster 🎟️

API REST para gestión de recintos y venta de entradas de eventos.

## Stack
- **Framework:** FastAPI
- **Base de Datos:** PostgreSQL (Aiven)
- **ORM:** SQLAlchemy
- **Despliegue:** Railway

## Configuración local

1. Clona el repositorio.
2. Copia `.env.example` a `.env` y añade tu `DATABASE_URL` de Aiven:
   ```
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/db?sslmode=require
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Arranca el servidor:
   ```bash
   uvicorn main:app --reload
   ```
6. Datos de prueba
   Para poblar la base de datos con datos de ejemplo, ejecuta:
   ```bash
   python seed.py
   ```
   
   Esto insertará 4 recintos (Madrid, Barcelona, Sevilla, Bilbao) y 5 eventos listos para probar. Los datos anteriores se borran antes de insertar, así que puedes ejecutarlo varias veces sin duplicados.
   > ⚠️ Asegúrate de tener el `.env` configurado y la API corriendo al menos una vez antes de ejecutar el seed, para que las tablas estén creadas.
   
5. Abre la documentación interactiva en `http://localhost:8000/docs`.

## Despliegue en Railway

1. Sube el código a GitHub.
2. En Railway, crea un nuevo proyecto desde el repo.
3. Añade la variable de entorno `DATABASE_URL` en el panel de Railway.
4. Railway detecta automáticamente FastAPI y despliega con uvicorn.

## Endpoints

### Recintos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/recintos/` | Crear recinto |
| GET | `/recintos/` | Listar recintos |
| GET | `/recintos/{id}` | Obtener recinto |
| PUT | `/recintos/{id}` | Actualizar recinto |
| DELETE | `/recintos/{id}` | Eliminar recinto |

### Eventos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/eventos/` | Crear evento (precio ≥ 0) |
| GET | `/eventos/?ciudad=Madrid` | Listar eventos (filtro ciudad opcional) |
| GET | `/eventos/{id}` | Obtener evento |
| PUT | `/eventos/{id}` | Actualizar evento |
| DELETE | `/eventos/{id}` | Eliminar evento |
| PATCH | `/eventos/{id}/comprar` | Comprar tickets |

### Ejemplo compra de tickets
```json
PATCH /eventos/1/comprar
{ "cantidad": 10 }
```
Devuelve `400` si no hay aforo suficiente.
