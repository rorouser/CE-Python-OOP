from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.models import ScooterStatus

app = FastAPI(
    title="ScooterFlow API",
    description="API de gestión de flota de patinetes eléctricos",
    version="1.0.0",
)


@app.post("/zonas/", response_model=schemas.ZoneRead, status_code=status.HTTP_201_CREATED)
def create_zona(zona: schemas.ZoneCreate, db: Session = Depends(get_db)):
    db_zona = models.Zone(**zona.model_dump())
    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)
    return db_zona


@app.get("/zonas/", response_model=List[schemas.ZoneRead])
def list_zonas(db: Session = Depends(get_db)):
    return db.query(models.Zone).all()


@app.get("/zonas/{zona_id}", response_model=schemas.ZoneRead)
def get_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(models.Zone).filter(models.Zone.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona


@app.post("/patinetes/", response_model=schemas.ScooterRead, status_code=status.HTTP_201_CREATED)
def create_patinete(patinete: schemas.ScooterCreate, db: Session = Depends(get_db)):
    zona = db.query(models.Zone).filter(models.Zone.id == patinete.zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    db_patinete = models.Scooter(**patinete.model_dump())
    db.add(db_patinete)
    db.commit()
    db.refresh(db_patinete)
    return db_patinete


@app.get("/patinetes/", response_model=List[schemas.ScooterRead])
def list_patinetes(db: Session = Depends(get_db)):
    return db.query(models.Scooter).all()


@app.get("/patinetes/{patinete_id}", response_model=schemas.ScooterRead)
def get_patinete(patinete_id: int, db: Session = Depends(get_db)):
    patinete = db.query(models.Scooter).filter(models.Scooter.id == patinete_id).first()
    if not patinete:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    return patinete

@app.post("/zonas/{zona_id}/mantenimiento", response_model=schemas.MantenimientoResponse)
def mantenimiento_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(models.Zone).filter(models.Zone.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    patinetes_bajos = (
        db.query(models.Scooter)
        .filter(models.Scooter.zona_id == zona_id, models.Scooter.bateria < 15)
        .all()
    )

    for p in patinetes_bajos:
        p.estado = ScooterStatus.mantenimiento

    db.commit()

    return schemas.MantenimientoResponse(
        zona_id=zona_id,
        patinetes_actualizados=len(patinetes_bajos),
        mensaje=f"{len(patinetes_bajos)} patinete(s) cambiados a mantenimiento.",
    )
