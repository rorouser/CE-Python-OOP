from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

import models
import dtos
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventMaster API")


@app.get("/")
def root():
    return {"message": "Bienvenido a EventMaster API"}

@app.post("/recintos/", response_model=dtos.RecintoOut, status_code=201)
def crear_recinto(recinto: dtos.RecintoCreate, db: Session = Depends(get_db)):
    db_recinto = models.Recinto(**recinto.model_dump())
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto


@app.get("/recintos/", response_model=List[dtos.RecintoOut])
def listar_recintos(db: Session = Depends(get_db)):
    return db.query(models.Recinto).all()


@app.get("/recintos/{id}", response_model=dtos.RecintoOut)
def obtener_recinto(id: int, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return recinto


@app.put("/recintos/{id}", response_model=dtos.RecintoOut)
def actualizar_recinto(id: int, datos: dtos.RecintoUpdate, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(recinto, campo, valor)
    db.commit()
    db.refresh(recinto)
    return recinto


@app.delete("/recintos/{id}", status_code=204)
def eliminar_recinto(id: int, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    db.delete(recinto)
    db.commit()
