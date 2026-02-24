from database import SessionLocal
from models import Recinto, Evento
from datetime import datetime

db = SessionLocal()

db.query(Evento).delete()
db.query(Recinto).delete()
db.commit()

recintos = [
    Recinto(nombre="Palacio de los Deportes", ciudad="Madrid", capacidad=15000),
    Recinto(nombre="Palau Sant Jordi", ciudad="Barcelona", capacidad=17000),
    Recinto(nombre="Estadio de la Cartuja", ciudad="Sevilla", capacidad=60000),
    Recinto(nombre="BEC Bilbao Exhibition Centre", ciudad="Bilbao", capacidad=5000),
]

db.add_all(recintos)
db.commit()
for r in recintos:
    db.refresh(r)

print("Recintos insertados:")
for r in recintos:
    print(f"   [{r.id}] {r.nombre} - {r.ciudad} (aforo: {r.capacidad})")

eventos = [
    Evento(
        nombre="Concierto Bad Bunny",
        fecha=datetime(2025, 6, 15, 21, 0),
        precio=85.0,
        tickets_vendidos=200,
        recinto_id=recintos[0].id,
    ),
    Evento(
        nombre="Festival Primavera Sound",
        fecha=datetime(2025, 5, 29, 18, 0),
        precio=120.0,
        tickets_vendidos=5000,
        recinto_id=recintos[1].id,
    ),
    Evento(
        nombre="Partido Selección España",
        fecha=datetime(2025, 9, 10, 20, 45),
        precio=60.0,
        tickets_vendidos=45000,
        recinto_id=recintos[2].id,
    ),
    Evento(
        nombre="Stand-up Comedy Night",
        fecha=datetime(2025, 7, 20, 20, 0),
        precio=35.0,
        tickets_vendidos=100,
        recinto_id=recintos[3].id,
    ),
    Evento(
        nombre="Coldplay World Tour",
        fecha=datetime(2025, 8, 3, 21, 0),
        precio=150.0,
        tickets_vendidos=14000,
        recinto_id=recintos[0].id,
    ),
]

db.add_all(eventos)
db.commit()

print("\nEventos insertados:")
for e in eventos:
    db.refresh(e)
    print(f"   [{e.id}] {e.nombre} - {e.fecha.strftime('%d/%m/%Y')} - {e.precio}€ (vendidos: {e.tickets_vendidos})")

db.close()
print("\nDatos de prueba cargados correctamente.")
