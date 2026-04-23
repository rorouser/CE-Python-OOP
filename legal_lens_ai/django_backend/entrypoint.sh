#!/bin/sh
set -e

echo "[entrypoint] Esperando a PostgreSQL en ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
    sleep 0.5
done
echo "[entrypoint] PostgreSQL listo."

echo "[entrypoint] Aplicando migraciones..."
python manage.py migrate --noinput

echo "[entrypoint] Recolectando estaticos..."
python manage.py collectstatic --noinput || true

# Crear superusuario si no existe (solo en dev)
if [ "$DJANGO_DEBUG" = "1" ]; then
    echo "[entrypoint] Asegurando superusuario admin/admin (modo desarrollo)..."
    python manage.py shell <<'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@legallens.local", "admin")
    print("Superusuario admin creado (admin/admin).")
else:
    print("Superusuario admin ya existe.")
PYEOF
fi

echo "[entrypoint] Levantando Django runserver en 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000
