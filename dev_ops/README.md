# 🛴 ScooterFlow API

API REST para la gestión de flotas de patinetes eléctricos y zonas de operación.
Construida con **FastAPI + PostgreSQL + SQLAlchemy + Alembic**, orquestada con **Docker Compose** y con CI automático via **GitHub Actions**.

---

## 🚀 Arranque en un solo comando

```bash
docker-compose up --build
```

La API quedará disponible en **http://localhost:8000**  
Documentación interactiva (Swagger): **http://localhost:8000/docs**

> El contenedor `api` espera automáticamente a que PostgreSQL esté listo (healthcheck) antes de arrancar y ejecutar las migraciones.

---

## 🗂️ Estructura del proyecto

```
scooterflow/
├── app/
│   ├── main.py          # Endpoints FastAPI
│   ├── models.py        # Modelos SQLAlchemy (Zone, Scooter)
│   ├── schemas.py       # Esquemas Pydantic (validación)
│   └── database.py      # Engine + SessionLocal + Base
├── migrations/
│   ├── env.py           # Configuración Alembic
│   └── versions/
│       ├── 001_initial.py          # Migración 1: tablas base
│       └── 002_add_puntuacion.py   # Migración 2: campo puntuacion_usuario
├── tests/
│   ├── conftest.py      # Fixtures pytest (SQLite en memoria)
│   └── test_api.py      # 7 tests de la API
├── .github/workflows/
│   └── ci.yml           # Pipeline CI/CD GitHub Actions
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## 📦 Modelos de datos

### Zone (Zona)
| Campo            | Tipo    | Descripción                   |
|------------------|---------|-------------------------------|
| id               | int PK  | Identificador                 |
| nombre           | string  | Ej: "Centro Histórico"        |
| codigo_postal    | string  | Código postal de la zona      |
| limite_velocidad | int     | Velocidad máxima (km/h)       |

### Scooter (Patinete)
| Campo             | Tipo   | Descripción                              |
|-------------------|--------|------------------------------------------|
| id                | int PK | Identificador                            |
| numero_serie      | string | Único                                    |
| modelo            | string | Modelo del patinete                      |
| bateria           | float  | 0–100 (validado por Pydantic)            |
| estado            | enum   | disponible / en_uso / mantenimiento / sin_bateria |
| zona_id           | int FK | Relación con Zone                        |
| puntuacion_usuario| float? | Añadido en migración 2                   |

---

## 🔌 Endpoints principales

| Método | Ruta                            | Descripción                                      |
|--------|---------------------------------|--------------------------------------------------|
| POST   | `/zonas/`                       | Crear una zona                                   |
| GET    | `/zonas/`                       | Listar zonas                                     |
| GET    | `/zonas/{id}`                   | Obtener zona por ID                              |
| POST   | `/patinetes/`                   | Crear patinete (batería 0-100, zona debe existir)|
| GET    | `/patinetes/`                   | Listar patinetes                                 |
| GET    | `/patinetes/{id}`               | Obtener patinete por ID                          |
| POST   | `/zonas/{id}/mantenimiento`     | Pasa a mantenimiento todos los patinetes con batería < 15% |

---

## 🧪 Tests

Los tests usan **SQLite en memoria** (sin necesitar Postgres):

```bash
# Sin Docker
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -v

# Con Docker
docker-compose exec api pytest tests/ -v
```

Cobertura de tests:
1. Crear patinete vinculado a una zona ✅
2. Validación batería > 100 → error 422 ✅
3. Validación batería < 0 → error 422 ✅
4. Lógica de mantenimiento automático ✅
5. Borde 14% → pasa a mantenimiento ✅
6. Borde 15% → NO pasa a mantenimiento ✅
7. Zona inexistente → 404 ✅

---

## 🗄️ Migraciones Alembic

```bash
# Aplicar todas las migraciones
docker-compose exec api alembic upgrade head

# Ver historial
docker-compose exec api alembic history

# Crear nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripcion"
```

---

## ⚙️ Variables de entorno

| Variable      | Valor por defecto                                    |
|---------------|------------------------------------------------------|
| DATABASE_URL  | `postgresql://scooter:scooter@db:5432/scooterflow`   |
