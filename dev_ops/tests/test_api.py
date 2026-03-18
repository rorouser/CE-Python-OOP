"""
Batería de tests – ScooterFlow API
Tarea 4: al menos 5 tests con pytest.
"""


# ── Test 1: crear patinete vinculado a una zona ────────────────────────────────

def test_crear_patinete_vinculado_a_zona(client, zona_base):
    """Un patinete se crea correctamente y queda vinculado a la zona."""
    zona_id = zona_base["id"]

    response = client.post(
        "/patinetes/",
        json={
            "numero_serie": "SC-001",
            "modelo": "Xiaomi Pro 2",
            "bateria": 80,
            "estado": "disponible",
            "zona_id": zona_id,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["numero_serie"] == "SC-001"
    assert data["zona_id"] == zona_id
    assert data["bateria"] == 80


# ── Test 2: validación batería > 100 → 422 ────────────────────────────────────

def test_validacion_bateria_mayor_100(client, zona_base):
    """La API rechaza (422) un patinete con batería de 150%."""
    response = client.post(
        "/patinetes/",
        json={
            "numero_serie": "SC-BAD",
            "modelo": "Modelo X",
            "bateria": 150,          # ← inválido
            "estado": "disponible",
            "zona_id": zona_base["id"],
        },
    )
    assert response.status_code == 422


# ── Test 3: validación batería < 0 → 422 ──────────────────────────────────────

def test_validacion_bateria_negativa(client, zona_base):
    """La API rechaza (422) un patinete con batería negativa."""
    response = client.post(
        "/patinetes/",
        json={
            "numero_serie": "SC-NEG",
            "modelo": "Modelo Y",
            "bateria": -5,           # ← inválido
            "estado": "disponible",
            "zona_id": zona_base["id"],
        },
    )
    assert response.status_code == 422


# ── Test 4: lógica de mantenimiento automático ────────────────────────────────

def test_mantenimiento_cambia_estado_patinetes_bajos(client, zona_base):
    """
    Al llamar a POST /zonas/{id}/mantenimiento,
    los patinetes con batería < 15% cambian a estado 'mantenimiento'.
    """
    zona_id = zona_base["id"]

    # Patinete con batería baja (debe cambiar)
    client.post(
        "/patinetes/",
        json={"numero_serie": "SC-LOW", "modelo": "A", "bateria": 10, "zona_id": zona_id},
    )
    # Patinete con batería alta (no debe cambiar)
    client.post(
        "/patinetes/",
        json={"numero_serie": "SC-HIGH", "modelo": "B", "bateria": 80, "zona_id": zona_id},
    )

    response = client.post(f"/zonas/{zona_id}/mantenimiento")
    assert response.status_code == 200
    data = response.json()
    assert data["patinetes_actualizados"] == 1

    # Verificar estado en la BD
    patinetes = client.get("/patinetes/").json()
    estados = {p["numero_serie"]: p["estado"] for p in patinetes}
    assert estados["SC-LOW"] == "mantenimiento"
    assert estados["SC-HIGH"] == "disponible"


# ── Test 5: mantenimiento con batería exactamente en 14% (borde inferior) ─────

def test_mantenimiento_borde_14_porciento(client, zona_base):
    """Un patinete con exactamente 14% de batería SÍ debe pasar a mantenimiento."""
    zona_id = zona_base["id"]
    client.post(
        "/patinetes/",
        json={"numero_serie": "SC-BORDE", "modelo": "C", "bateria": 14, "zona_id": zona_id},
    )

    response = client.post(f"/zonas/{zona_id}/mantenimiento")
    assert response.json()["patinetes_actualizados"] == 1


# ── Test 6: mantenimiento con batería exactamente en 15% (borde superior) ─────

def test_mantenimiento_borde_15_porciento_no_cambia(client, zona_base):
    """Un patinete con exactamente 15% de batería NO debe pasar a mantenimiento."""
    zona_id = zona_base["id"]
    client.post(
        "/patinetes/",
        json={"numero_serie": "SC-15", "modelo": "D", "bateria": 15, "zona_id": zona_id},
    )

    response = client.post(f"/zonas/{zona_id}/mantenimiento")
    assert response.json()["patinetes_actualizados"] == 0


# ── Test 7: zona no existente devuelve 404 ────────────────────────────────────

def test_zona_no_encontrada(client):
    """Crear un patinete en una zona que no existe devuelve 404."""
    response = client.post(
        "/patinetes/",
        json={"numero_serie": "SC-404", "modelo": "E", "bateria": 50, "zona_id": 9999},
    )
    assert response.status_code == 404
